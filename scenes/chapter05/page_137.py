from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "137"
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
def dashed(m, n=40, r=0.55):
    return DashedVMobject(m, num_dashes=n, dashed_ratio=r)


class Page_137(Chapter5Scene):
    PAGE_NO = "137"

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

    # A - MAP definition, eq 5.79
    def scene_a(self, audio):
        items = self.heading_in(audio, "MAP Estimation")
        n0 = self.note_in(audio, "Choose the point of maximal posterior probability:", 2.3, 24)
        e1 = Mx(r"\boldsymbol{\theta}_{\mathrm{MAP}}", r"=", r"\arg\max_{\boldsymbol{\theta}}\,p(\boldsymbol{\theta}\mid\boldsymbol{x})", size=36)
        fit(e1, 5.9); e1.move_to([-0.3, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=1.6)
        e2 = Mx(r"=", r"\arg\max_{\boldsymbol{\theta}}", r"\log p(\boldsymbol{x}\mid\boldsymbol{\theta})", r"+", r"\log p(\boldsymbol{\theta})", size=36)
        fit(e2, 5.9); e2.move_to([-0.3, 0.55, 0])
        n79 = T("(5.79)", 28).move_to([3.3, 0.55, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=2.0)
        self.play(FadeIn(n79), run_time=0.25)
        b1 = SurroundingRectangle(e2[2], color=K, buff=0.1, stroke_width=4)
        b2 = SurroundingRectangle(e2[4], color=K, buff=0.1, stroke_width=4)
        l1 = T("log-likelihood", 20).next_to(b1, DOWN, buff=0.12)
        l2 = T("prior", 20).next_to(b2, DOWN, buff=0.12)
        with audio.cue("grow", pan=-0.3): self.play(Create(b1), FadeIn(l1), run_time=0.7)
        with audio.cue("grow", pan=0.3): self.play(Create(b2), FadeIn(l2), run_time=0.7)
        ax = self.axes([-3, 4, 1], [0, 0.7, 1], 5.4, 1.4, [0, -1.75, 0])
        post = ax.plot(gauss(0.8, 0.7), x_range=[-3, 4], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=0.3): self.play(Create(post), run_time=1.3)
        pk = gauss(0.8, 0.7)(0.8)
        dot = Dot(ax.c2p(0.8, pk), radius=0.11, color=K).set_z_index(5)
        vl = DashedLine(ax.c2p(0.8, 0), ax.c2p(0.8, pk), color=K, stroke_width=3)
        lab = Mx(r"\boldsymbol{\theta}_{\mathrm{MAP}}", size=26).next_to(ax.c2p(0.8, 0), DOWN, buff=0.08)
        with audio.cue("grow"): self.play(GrowFromCenter(dot), Create(vl), FadeIn(lab), run_time=0.7)
        n1 = self.note_in(audio, "Maximal probability density when theta is continuous.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, e1, e2, n79, b1, b2, l1, l2, ax, post, dot, vl, lab, n1]

    # B - weight decay example
    def scene_b(self, audio):
        items = self.heading_in(audio, "MAP and Weight Decay")
        r1, t1 = self.card(r"Linear regression with a Gaussian prior on $\boldsymbol{w}$", 2.1, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        e = Mx(r"p(\boldsymbol{w})=\mathcal{N}\left(\boldsymbol{w};\boldsymbol{0},\tfrac{1}{\lambda}\boldsymbol{I}^{2}\right)", size=38)
        fit(e, 5.8); e.move_to([0, 1.1, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.8)
        r2, t2 = self.card(r"Log-prior term in 5.79 $\propto$ weight decay penalty $\lambda\boldsymbol{w}^{\top}\boldsymbol{w}$", 0.2, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        ax = self.axes([-3, 3, 1], [0, 9, 3], 4.2, 1.5, [-0.8, -1.35, 0])
        par = ax.plot(lambda x: x * x, x_range=[-3, 3], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(par), run_time=1.2)
        pl = Mx(r"\lambda\boldsymbol{w}^{\top}\boldsymbol{w}", size=30).move_to([2.2, -0.9, 0])
        with audio.cue("grow"): self.play(FadeIn(pl), run_time=0.6)
        r3, t3 = self.card(r"Plus a term independent of $\boldsymbol{w}$: no effect on learning", -2.55, 22, 0.75)
        with audio.cue("grow", pan=-0.3): self.play(Create(r3), Write(t3), run_time=1.2)
        r4, t4 = self.card(r"MAP with a Gaussian prior $=$ weight decay", -3.4, 26, 0.75)
        with audio.cue("grow", pan=0.3): self.play(Create(r4), Write(t4), run_time=1.2)
        self.wait(1.4)
        return items + [r1, t1, e, r2, t2, ax, par, pl, r3, t3, r4, t4]

    # C - variance and bias
    def scene_c(self, audio):
        items = self.heading_in(audio, "Variance and Bias")
        n0 = self.note_in(audio, "The prior brings information not found in the data:", 2.3, 24)
        ax = self.axes([-3.5, 3.5, 1], [0, 0.9, 1], 5.4, 2.0, [0, 0.7, 0])
        ml = dashed(ax.plot(gauss(0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=5), 60, 0.5)
        mp = ax.plot(gauss(0.5, 0.5), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        tv = DashedVMobject(Line(ax.c2p(0, 0), ax.c2p(0, 0.88), color=K, stroke_width=3), num_dashes=22, dashed_ratio=0.25)
        tl = T("true value", 20).next_to(ax.c2p(0, 0), DOWN, buff=0.1)
        with audio.cue("draw"): self.play(Create(ax), Create(tv), FadeIn(tl), run_time=0.9)
        with audio.cue("slide", pan=-0.3): self.play(Create(ml), run_time=1.3)
        with audio.cue("slide", pan=0.3): self.play(Create(mp), run_time=1.3)
        l1 = Line([-3.6, -1.15, 0], [-3.0, -1.15, 0], color=K, stroke_width=6)
        l1 = dashed(l1, 5, 0.55)
        t1 = T("ML estimate", 22).next_to(l1, RIGHT, buff=0.15)
        l2 = Line([0.0, -1.15, 0], [0.6, -1.15, 0], color=K, stroke_width=7)
        t2 = T("MAP estimate", 22).next_to(l2, RIGHT, buff=0.15)
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(t1), FadeIn(l2), FadeIn(t2), run_time=0.8)
        r1, t3 = self.card(r"Reduces the variance of the point estimate", -2.0, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t3), run_time=1.2)
        r2, t4 = self.card(r"At the price of increased bias", -3.0, 26, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t4), run_time=1.2)
        self.wait(1.4)
        return items + [n0, ax, ml, mp, tv, tl, l1, t1, l2, t2, r1, t3, r2, t4]

    # D - regularization as MAP
    def scene_d(self, audio):
        items = self.heading_in(audio, "Regularization as MAP")
        r1, t1 = self.card(r"Weight-decay regularized ML is a MAP approximation", 2.1, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"Holds when the extra objective term corresponds to $\log p(\boldsymbol{\theta})$", 1.15, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        e = Mx(r"\log p(\boldsymbol{x}\mid\boldsymbol{\theta})", r"+", r"\log p(\boldsymbol{\theta})", size=36)
        fit(e, 5.0); e.move_to([0, 0.1, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.5)
        b = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(b), run_time=0.5)
        n0 = self.note_in(audio, "Not all regularization penalties correspond to MAP inference:", -0.9, 22)
        r3, t3 = self.card(r"Some terms are not the logarithm of a probability distribution", -1.85, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r3), Write(t3), run_time=1.3)
        r4, t4 = self.card(r"Others depend on the data, which a prior is not allowed to do", -2.85, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r4), Write(t4), run_time=1.3)
        self.wait(1.4)
        return items + [r1, t1, r2, t2, e, b, n0, r3, t3, r4, t4]

    # E - mixture prior and section 5.7
    def scene_e(self, audio):
        items = self.heading_in(audio, "Richer Priors")
        n0 = self.note_in(audio, "MAP can design complicated yet interpretable penalties:", 2.3, 22)
        ax = self.axes([-4, 4, 1], [0, 0.5, 1], 5.4, 1.5, [0, 0.95, 0])
        c1 = lambda x: 0.5 * gauss(-1.5, 0.6)(x)
        c2 = lambda x: 0.5 * gauss(1.5, 0.8)(x)
        d1 = dashed(ax.plot(c1, x_range=[-4, 4], color=K, stroke_width=5), 40, 0.5)
        d2 = dashed(ax.plot(c2, x_range=[-4, 4], color=K, stroke_width=5), 40, 0.5)
        mix = ax.plot(lambda x: c1(x) + c2(x), x_range=[-4, 4], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(d1), run_time=1.0)
        with audio.cue("slide", pan=0.3): self.play(Create(d2), run_time=1.0)
        with audio.cue("slide"): self.play(Create(mix), run_time=1.3)
        ml = T("mixture of Gaussians as the prior", 22).move_to([0, -0.2, 0])
        with audio.cue("type", glyphs=32): self.play(Write(ml), run_time=1.0)
        cite = T("Nowlan and Hinton, 1992", 22).move_to([0, -0.7, 0])
        with audio.cue("grow"): self.play(FadeIn(cite), run_time=0.5)
        r1, t1 = self.card(r"\textbf{5.7} \ Supervised Learning Algorithms", -1.7, 30, 1.0)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Learn to associate an input $\boldsymbol{x}$ with an output $\boldsymbol{y}$", -2.75, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        n1 = self.note_in(audio, "Outputs may need a human supervisor to provide them.", -3.45, 22)
        self.wait(1.4)
        return items + [n0, ax, d1, d2, mix, ml, cite, r1, t1, r2, t2, n1]

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
    Page_137().render()
