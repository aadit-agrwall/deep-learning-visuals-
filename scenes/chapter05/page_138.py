from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "138"
PAGE_SRC = Path(f"assets/bookpage/page_{PAGE}.png")
BAND_DIR = Path(f"assets/bookpage/page_{PAGE}_bands")
CUE_FILE = f"/tmp/p{PAGE}_cues.json"
WHITE_BG = "#FFFFFF"; K = "#000000"; MIN_SECONDS = 62.0


class _Ctx:
    def __init__(self, owner, entry, ctx):
        self.o, self.e, self.c = owner, entry, ctx
    def __enter__(self):
        self.e["t"] = self.o.now(); self.o.flush()
        return self.c.__enter__()
    def __exit__(self, *exc):
        self.e["end"] = self.o.now(); self.o.flush()
        return self.c.__exit__(*exc)


class CueLogger:
    def __init__(self, scene, real):
        self._s, self._r, self.log = scene, real, []
    def now(self):
        try: return float(self._s.renderer.time)
        except Exception: return float(self._s.time)
    def flush(self):
        _json.dump(self.log, open(CUE_FILE, "w"))
    def cue(self, name, *a, **k):
        e = {"t": self.now(), "end": self.now(), "name": name,
             "glyphs": k.get("glyphs", 0), "pan": k.get("pan", 0.0)}
        self.log.append(e)
        return _Ctx(self, e, self._r.cue(name, *a, **k))
    def __getattr__(self, n): return getattr(self._r, n)


class Collapse(Animation):
    def __init__(self, mobject, point, spin=0.0, reverse=False, **kwargs):
        self.point = np.array(point, dtype=float); self.spin = spin; self.reverse = reverse
        self.cur_s = 1.0; self.cur_a = 0.0
        super().__init__(mobject, **kwargs)
        if reverse: self._apply(1.0)
    def _apply(self, t):
        s = max(1 - 0.985 * t, 1e-3); a = self.spin * t
        self.mobject.scale(s / self.cur_s, about_point=self.point)
        self.mobject.rotate(a - self.cur_a, about_point=self.point)
        self.cur_s, self.cur_a = s, a
    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha); self._apply(1 - t if self.reverse else t)


class ZoomPulse(Animation):
    def __init__(self, mobject, point, s0, s1, **kwargs):
        self.point = np.array(point, dtype=float); self.s0, self.s1, self.cur = s0, s1, 1.0
        super().__init__(mobject, **kwargs)
    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha); s = max(self.s0 + (self.s1 - self.s0) * t, 1e-3)
        self.mobject.scale(s / self.cur, about_point=self.point); self.cur = s


def build_bands():
    if not PAGE_SRC.exists(): raise FileNotFoundError(f"Missing page image: {PAGE_SRC}")
    image = Image.open(PAGE_SRC).convert("RGB"); w, h = image.size
    image = image.crop((6, 6, w - 6, h - 6)); w, h = image.size
    arr = np.asarray(image)
    ink = (arr[:, 14:-14].min(axis=2) < 235).any(axis=1); ink[:3] = False; ink[-6:] = False
    BAND_DIR.mkdir(parents=True, exist_ok=True)
    for old in BAND_DIR.glob("band_*.png"): old.unlink()
    bands, y = [], 0
    while y < h:
        if not ink[y]: y += 1; continue
        s = y
        while y < h and ink[y]: y += 1
        top, bottom = max(0, s - 2), min(h, y + 2)
        p = BAND_DIR / f"band_{len(bands):03d}.png"
        image.crop((0, top, w, bottom)).save(p); bands.append((str(p), top, bottom))
    if not bands: raise ValueError("No text strips detected")
    return w, h, bands


def fit(mob, width):
    if mob.width > width: mob.scale_to_fit_width(width)
    return mob
def T(text, size=30, bold=False):
    return Tex((r"\textbf{" + text + "}") if bold else text, color=K, font_size=size)
def Mx(*parts, size=40):
    return MathTex(*parts, color=K, font_size=size)
def gauss(mu, s):
    return lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
def dashed(m, n=40, r=0.55):
    return DashedVMobject(m, num_dashes=n, dashed_ratio=r)


class Page_138(Chapter5Scene):
    PAGE_NO = "138"

    def make_page(self, width, height, bands):
        aspect = width / height
        ph = min(config.frame_height - 1.3, (config.frame_width - 0.4) / aspect); pw = ph * aspect
        sc = pw / width; c = np.array([0.0, 0.1, 0.0])
        paper = Rectangle(width=pw, height=ph, stroke_width=0, fill_color=WHITE_BG, fill_opacity=1).move_to(c)
        paper.set_z_index(0); top = c[1] + ph / 2; strips = []
        for path, t, b in bands:
            s = ImageMobject(path); s.scale_to_fit_width(pw)
            s.move_to([c[0], top - ((t + b) / 2) * sc, 0]); s.set_z_index(1); strips.append(s)
        return paper, strips

    def page_motion(self, paper, strips, point, reverse=False, run=2.0):
        pt = np.array(point, dtype=float)
        order = sorted(strips, key=lambda s: np.linalg.norm(s.get_center() - pt), reverse=not reverse)
        anims = [Collapse(s, pt, PI * 0.5, reverse=reverse, rate_func=smooth, remover=not reverse, run_time=run) for s in order]
        return AnimationGroup(LaggedStart(*anims, lag_ratio=0.03),
                              Collapse(paper, pt, PI * 0.5, reverse=reverse, rate_func=smooth, remover=not reverse, run_time=run * 1.6))

    def next_scene(self, audio, items):
        with audio.cue("wipe"):
            self.play(*[FadeOut(i) for i in items if i is not None], run_time=0.7)
        self.wait(0.2)

    def heading_in(self, audio, text):
        h = T(text, 40, True); fit(h, 7.6); h.to_edge(UP, buff=0.5)
        with audio.cue("type", glyphs=len(text)): self.play(Write(h), run_time=1.2)
        u = Line(h.get_left(), h.get_right(), color=K, stroke_width=4).next_to(h, DOWN, buff=0.12)
        with audio.cue("draw"): self.play(Create(u), run_time=0.5)
        return [h, u]

    def note_in(self, audio, text, y, size=30):
        n = T(text, size); fit(n, 7.4); n.move_to([0, y, 0])
        with audio.cue("type", glyphs=len(text)): self.play(Write(n), run_time=1.3)
        return n

    def card(self, text, y, size=26, h=0.9, w=7.2, x=0.0):
        r = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=K,
                             stroke_width=3, fill_opacity=0).move_to([x, y, 0])
        t = Tex(text, color=K, font_size=size); fit(t, w - 0.4); t.move_to(r)
        return r, t

    def axes(self, xr, yr, xl, yl, pos):
        return Axes(x_range=xr, y_range=yr, x_length=xl, y_length=yl, tips=False,
                    axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to(pos)

    # A - estimating p(y|x) by maximum likelihood
    def scene_a(self, audio):
        items = self.heading_in(audio, "Probabilistic Learning")
        n0 = self.note_in(audio, "Most algorithms in this book estimate a distribution:", 2.3, 24)
        e1 = Mx(r"p(y\mid\boldsymbol{x})", size=52).move_to([0, 1.3, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=1.3)
        bx = SurroundingRectangle(e1, color=K, buff=0.15, stroke_width=4)
        with audio.cue("grow"): self.play(Create(bx), run_time=0.5)
        r1, t1 = self.card(r"Maximum likelihood finds the best $\boldsymbol{\theta}$", 0.0, 26, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        ar = Arrow([0, -0.5, 0], [0, -1.05, 0], color=K, buff=0, stroke_width=5, tip_length=0.18)
        with audio.cue("slide"): self.play(GrowArrow(ar), run_time=0.5)
        e2 = Mx(r"p(y\mid\boldsymbol{x};\boldsymbol{\theta})", size=44).move_to([0, -1.6, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=1.3)
        r2, t2 = self.card(r"A parametric family of distributions", -2.7, 26, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        self.wait(1.4)
        return items + [n0, e1, bx, r1, t1, ar, e2, r2, t2]

    # B - linear regression as a Gaussian family, eq 5.80
    def scene_b(self, audio):
        items = self.heading_in(audio, "Linear Regression Family")
        n0 = self.note_in(audio, "We have already seen linear regression corresponds to:", 2.3, 22)
        e = Mx(r"p(y\mid\boldsymbol{x};\boldsymbol{\theta})", r"=",
               r"\mathcal{N}(y;\boldsymbol{\theta}^{\top}\boldsymbol{x},\boldsymbol{I})", size=38)
        fit(e, 5.8); e.move_to([-0.3, 1.4, 0])
        n80 = T("(5.80)", 28).move_to([3.3, 1.4, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.0)
        self.play(FadeIn(n80), run_time=0.25)
        box = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        ax = self.axes([-3.5, 3.5, 1], [0, 0.5, 1], 5.2, 1.6, [0, -0.35, 0])
        bell = ax.plot(gauss(0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=0.3): self.play(Create(bell), run_time=1.3)
        mline = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.4), color=K, stroke_width=3)
        mlab = Mx(r"\boldsymbol{\theta}^{\top}\boldsymbol{x}", size=28).next_to(ax.c2p(0, 0), DOWN, buff=0.1)
        with audio.cue("grow"): self.play(Create(mline), FadeIn(mlab), run_time=0.7)
        r1, t1 = self.card(r"Mean is any real number: every value is valid", -2.4, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        n1 = self.note_in(audio, "Real-valued outputs: a normal distribution fits.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, e, n80, box, ax, bell, mline, mlab, r1, t1, n1]

    # C - classification with two classes
    def scene_c(self, audio):
        items = self.heading_in(audio, "Two Classes")
        n0 = self.note_in(audio, "Generalize to classification: class 0 and class 1.", 2.3, 24)
        r0 = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2, stroke_color=K, stroke_width=3).move_to([-2.0, 1.1, 0])
        t0 = T("class 0", 28).move_to(r0)
        r1 = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2, stroke_color=K, stroke_width=3).move_to([2.0, 1.1, 0])
        t1 = T("class 1", 28).move_to(r1)
        with audio.cue("grow", pan=-0.4): self.play(Create(r0), Write(t0), run_time=0.9)
        with audio.cue("grow", pan=0.4): self.play(Create(r1), Write(t1), run_time=0.9)
        e = Mx(r"p(y=0)", r"+", r"p(y=1)", r"=", r"1", size=40)
        fit(e, 5.4); e.move_to([0, -0.15, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.6)
        b = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(b), run_time=0.5)
        n1 = self.note_in(audio, "Specify only one: it determines the other.", -0.95, 24)
        nl = NumberLine(x_range=[0, 1, 0.5], length=5.0, color=K, stroke_width=4, include_ticks=True, tick_size=0.12).move_to([0, -2.0, 0])
        z = Mx(r"0", size=28).next_to(nl.n2p(0), DOWN, buff=0.15)
        o = Mx(r"1", size=28).next_to(nl.n2p(1), DOWN, buff=0.15)
        with audio.cue("draw"): self.play(Create(nl), FadeIn(z), FadeIn(o), run_time=0.9)
        seg = Line(nl.n2p(0), nl.n2p(1), color=K, stroke_width=10)
        with audio.cue("slide"): self.play(Create(seg), run_time=0.8)
        n2 = self.note_in(audio, "A binary variable's mean must lie between 0 and 1.", -3.1, 22)
        self.wait(1.4)
        return items + [n0, r0, t0, r1, t1, e, b, n1, nl, z, o, seg, n2]

    # D - sigmoid and logistic regression, eq 5.81
    def scene_d(self, audio):
        items = self.heading_in(audio, "Logistic Regression")
        n0 = self.note_in(audio, r"Squash the linear output into $(0,1)$ with the sigmoid:", 2.3, 22)
        e = Mx(r"p(y=1\mid\boldsymbol{x};\boldsymbol{\theta})", r"=",
               r"\sigma(\boldsymbol{\theta}^{\top}\boldsymbol{x})", size=38)
        fit(e, 5.8); e.move_to([-0.3, 1.4, 0])
        n81 = T("(5.81)", 28).move_to([3.3, 1.4, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.0)
        self.play(FadeIn(n81), run_time=0.25)
        box = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        ax = self.axes([-6, 6, 2], [0, 1.1, 1], 5.2, 2.0, [0, -0.5, 0])
        sg = ax.plot(sigmoid, x_range=[-6, 6], color=K, stroke_width=7)
        top = dashed(Line(ax.c2p(-6, 1), ax.c2p(6, 1), color=K, stroke_width=3), 20, 0.5)
        half = dashed(Line(ax.c2p(-6, 0.5), ax.c2p(6, 0.5), color=K, stroke_width=3), 20, 0.3)
        with audio.cue("draw"): self.play(Create(ax), Create(top), Create(half), run_time=0.9)
        with audio.cue("slide", pan=0.3): self.play(Create(sg), run_time=1.4)
        l1 = Mx(r"1", size=24).next_to(ax.c2p(-6, 1), LEFT, buff=0.1)
        l0 = Mx(r"0", size=24).next_to(ax.c2p(-6, 0), LEFT, buff=0.1)
        lh = Mx(r"0.5", size=24).next_to(ax.c2p(-6, 0.5), LEFT, buff=0.1)
        xl = Mx(r"\boldsymbol{\theta}^{\top}\boldsymbol{x}", size=26).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(l0), FadeIn(lh), FadeIn(xl), run_time=0.6)
        r1, t1 = self.card(r"Known as \textbf{logistic regression}", -2.45, 28, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        n1 = self.note_in(audio, "A strange name: used for classification, not regression.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, e, n81, box, ax, sg, top, half, l1, l0, lh, xl, r1, t1, n1]

    # E - no closed form, gradient descent
    def scene_e(self, audio):
        items = self.heading_in(audio, "Searching for Weights")
        r1, t1 = self.card(r"Linear regression: solve the normal equations", 2.1, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"Logistic regression: no closed-form solution", 1.15, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        ax = self.axes([-3, 3, 1], [0, 9, 3], 4.6, 1.9, [0, -0.7, 0])
        bowl = ax.plot(lambda x: x * x, x_range=[-3, 3], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(bowl), run_time=1.2)
        xs = [-2.4, -1.5, -0.8, -0.3, 0.0]
        pts = [Dot(ax.c2p(x, x * x), radius=0.09, color=K).set_z_index(5) for x in xs]
        steps = [Arrow(pts[i].get_center(), pts[i + 1].get_center(), color=K, buff=0.1,
                       stroke_width=3, tip_length=0.15) for i in range(len(pts) - 1)]
        with audio.cue("grow"): self.play(GrowFromCenter(pts[0]), run_time=0.4)
        for i in range(len(steps)):
            with audio.cue("slide", pan=-0.2 + 0.1 * i):
                self.play(GrowArrow(steps[i]), GrowFromCenter(pts[i + 1]), run_time=0.55)
        gl = T("gradient descent", 22).move_to([2.1, -0.4, 0])
        ml = T("minimum", 20).next_to(ax.c2p(0, 0), DOWN, buff=0.1)
        with audio.cue("type", glyphs=26): self.play(FadeIn(gl), FadeIn(ml), run_time=0.6)
        r3, t3 = self.card(r"Minimize the negative log-likelihood", -2.5, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r3), Write(t3), run_time=1.2)
        n1 = self.note_in(audio, "Same strategy fits essentially any supervised problem.", -3.35, 22)
        self.wait(1.4)
        return items + [r1, t1, r2, t2, ax, bowl] + pts + steps + [gl, ml, r3, t3, n1]

    def construct(self):
        self.camera.background_color = WHITE_BG; config.background_color = WHITE_BG
        audio = CueLogger(self, ASMRSync(self, self.PAGE_NO))
        w, h, bands = build_bands()
        paper, strips = self.make_page(w, h, bands); pc = paper.get_center()
        with audio.cue("grow"): self.play(FadeIn(paper), *[FadeIn(s) for s in strips], run_time=0.6)
        self.wait(3.4)
        with audio.cue("zoom"): self.play(self.page_motion(paper, strips, pc, reverse=False))
        dot = Dot(pc, radius=0.07, color=K)
        with audio.cue("grow"): self.play(GrowFromCenter(dot), run_time=0.3)
        with audio.cue("zoom"):
            self.play(Flash(pc, color=K, flash_radius=0.8, line_length=0.3, run_time=0.7), FadeOut(dot, scale=4), run_time=0.7)
        for scene in (self.scene_a, self.scene_b, self.scene_c, self.scene_d, self.scene_e):
            self.next_scene(audio, scene(audio))
        paper2, strips2 = self.make_page(w, h, bands); pc2 = paper2.get_center()
        self.add(paper2, *strips2)
        with audio.cue("zoom"): self.play(self.page_motion(paper2, strips2, pc2, reverse=True))
        self.wait(0.8); allm = [paper2, *strips2]
        with audio.cue("zoom"):
            self.play(*[ZoomPulse(m, pc2, 1.0, 1.04, run_time=1.2, rate_func=smooth) for m in allm])
            self.play(*[ZoomPulse(m, pc2, 1.0, 1 / 1.04, run_time=1.2, rate_func=smooth) for m in allm])
        self.wait(1.5)
        try: now = self.renderer.time
        except Exception: now = self.time
        if now < MIN_SECONDS: self.wait(MIN_SECONDS - now + 0.2)
        audio.finish()


if __name__ == "__main__":
    Page_138().render()
