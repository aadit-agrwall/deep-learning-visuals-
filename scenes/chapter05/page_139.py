from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "139"
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
def dashed(m, n=40, r=0.55):
    return DashedVMobject(m, num_dashes=n, dashed_ratio=r)


class Page_139(Chapter5Scene):
    PAGE_NO = "139"

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

    # A - SVM as a linear classifier
    def scene_a(self, audio):
        items = self.heading_in(audio, "Support Vector Machines")
        n0 = self.note_in(audio, "Like logistic regression: driven by a linear function", 2.35, 22)
        e = Mx(r"\boldsymbol{w}^{\top}\boldsymbol{x}+b", size=44).move_to([0, 1.55, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.3)
        # 2D class picture: separating line, margin lines, points
        ax = self.axes([-3, 3, 1], [-2, 2, 1], 4.8, 2.4, [0, -0.35, 0])
        sep = Line(ax.c2p(-2.6, -1.8), ax.c2p(2.6, 1.8), color=K, stroke_width=6)
        m1 = dashed(Line(ax.c2p(-2.9, -1.0), ax.c2p(1.6, 2.0), color=K, stroke_width=4), 18, 0.5)
        m2 = dashed(Line(ax.c2p(-1.6, -2.0), ax.c2p(2.9, 1.0), color=K, stroke_width=4), 18, 0.5)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(sep), Create(m1), Create(m2), run_time=1.3)
        pos = [(-1.6, 1.2), (-0.6, 1.6), (-2.0, 0.2), (-1.0, 0.7)]
        neg = [(1.6, -1.2), (0.7, -1.7), (2.1, -0.2), (1.1, -0.7)]
        pd = VGroup(*[Dot(ax.c2p(*p), radius=0.1, color=K) for p in pos])
        nd = VGroup(*[Square(side_length=0.18, color=K, stroke_width=3).move_to(ax.c2p(*p)) for p in neg])
        with audio.cue("grow", pan=-0.3): self.play(LaggedStart(*[GrowFromCenter(d) for d in pd], lag_ratio=0.15), run_time=1.0)
        with audio.cue("grow", pan=0.3): self.play(LaggedStart(*[GrowFromCenter(d) for d in nd], lag_ratio=0.15), run_time=1.0)
        lp = Mx(r"+", size=36).move_to(ax.c2p(-2.5, 1.7)); ln = Mx(r"-", size=36).move_to(ax.c2p(2.5, -1.7))
        with audio.cue("grow"): self.play(FadeIn(lp), FadeIn(ln), run_time=0.5)
        r1, t1 = self.card(r"Outputs only a class identity, no probabilities", -2.35, 22, 0.75)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        n1 = self.note_in(audio, r"Positive class if $\boldsymbol{w}^{\top}\boldsymbol{x}+b>0$, negative if $<0$.", -3.25, 22)
        self.wait(1.4)
        return items + [n0, e, ax, sep, m1, m2, pd, nd, lp, ln, r1, t1, n1]

    # B - kernel trick and eq 5.82
    def scene_b(self, audio):
        items = self.heading_in(audio, "The Kernel Trick")
        n0 = self.note_in(audio, "Many algorithms use only dot products between examples:", 2.35, 22)
        e = Mx(r"\boldsymbol{w}^{\top}\boldsymbol{x}+b", r"=", r"b+\sum_{i=1}^{m}\alpha_i\,\boldsymbol{x}^{\top}\boldsymbol{x}^{(i)}", size=38)
        fit(e, 5.8); e.move_to([-0.3, 1.4, 0])
        n82 = T("(5.82)", 28).move_to([3.3, 1.4, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.2)
        self.play(FadeIn(n82), run_time=0.25)
        box = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        specs = [(r"\boldsymbol{x}^{(i)}", "training example", -2.4),
                 (r"\boldsymbol{\alpha}", "vector of coefficients", 0.0),
                 (r"\boldsymbol{x}^{\top}\boldsymbol{x}^{(i)}", "dot product", 2.4)]
        boxes, texs, caps = [], [], []
        for lb, cp, x in specs:
            r = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.2, stroke_color=K,
                                 stroke_width=3, fill_opacity=0).move_to([x, 0.0, 0])
            tx = Mx(lb, size=28).move_to(r)
            c = T(cp, 18).move_to([x, -0.65, 0])
            boxes.append(r); texs.append(tx); caps.append(c)
        for i in range(3):
            with audio.cue("grow", pan=-0.4 + 0.4 * i): self.play(Create(boxes[i]), Write(texs[i]), FadeIn(caps[i]), run_time=0.8)
        r1, t1 = self.card(r"The linear SVM function re-written as a sum of dot products", -1.7, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        n1 = self.note_in(audio, "Dot products between examples are all we need.", -2.75, 24)
        self.wait(1.4)
        return items + [n0, e, n82, box] + boxes + texs + caps + [r1, t1, n1]

    # C - feature map and kernel
    def scene_c(self, audio):
        items = self.heading_in(audio, "Feature Map and Kernel")
        n0 = self.note_in(audio, r"Replace $\boldsymbol{x}$ with the output of a feature function:", 2.35, 22)
        e1 = Mx(r"\boldsymbol{x}", r"\;\longrightarrow\;", r"\phi(\boldsymbol{x})", size=44)
        e1.move_to([0, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=1.5)
        b1 = SurroundingRectangle(e1[2], color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow"): self.play(Create(b1), run_time=0.5)
        n1 = self.note_in(audio, "and the dot product with a function called a kernel:", 0.65, 22)
        e2 = Mx(r"k(\boldsymbol{x},\boldsymbol{x}^{(i)})", r"=", r"\phi(\boldsymbol{x})\cdot\phi(\boldsymbol{x}^{(i)})", size=38)
        fit(e2, 5.8); e2.move_to([0, -0.3, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=2.0)
        b2 = SurroundingRectangle(e2[0], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(b2), run_time=0.5)
        r1, t1 = self.card(r"The $\cdot$ is an inner product, analogous to $\phi(\boldsymbol{x})^{\top}\phi(\boldsymbol{x}^{(i)})$", -1.35, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Infinite-dimensional spaces: inner products by integration", -2.35, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        n2 = self.note_in(audio, "A full development is beyond the scope of this book.", -3.25, 22)
        self.wait(1.4)
        return items + [n0, e1, b1, n1, e2, b2, r1, t1, r2, t2, n2]

    # D - kernel prediction function, eq 5.83
    def scene_d(self, audio):
        items = self.heading_in(audio, "Kernel Predictions")
        n0 = self.note_in(audio, "Replace dot products with kernel evaluations:", 2.35, 24)
        e = Mx(r"f(\boldsymbol{x})", r"=", r"b+\sum_{i}\alpha_i\,k(\boldsymbol{x},\boldsymbol{x}^{(i)})", size=38)
        fit(e, 5.8); e.move_to([-0.3, 1.4, 0])
        n83 = T("(5.83)", 28).move_to([3.3, 1.4, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.0)
        self.play(FadeIn(n83), run_time=0.25)
        box = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        # chain: x -> phi(x) -> f(x)
        specs = [(r"\boldsymbol{x}", -2.6), (r"\phi(\boldsymbol{x})", 0.0), (r"f(\boldsymbol{x})", 2.6)]
        boxes, texs = [], []
        for lb, x in specs:
            r = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.2, stroke_color=K,
                                 stroke_width=3, fill_opacity=0).move_to([x, -0.1, 0])
            boxes.append(r); texs.append(Mx(lb, size=28).move_to(r))
        a1 = Arrow([-1.65, -0.1, 0], [-1.0, -0.1, 0], color=K, buff=0, stroke_width=4, tip_length=0.18)
        a2 = Arrow([1.0, -0.1, 0], [1.65, -0.1, 0], color=K, buff=0, stroke_width=4, tip_length=0.18)
        with audio.cue("grow", pan=-0.4): self.play(Create(boxes[0]), Write(texs[0]), run_time=0.7)
        with audio.cue("slide"): self.play(GrowArrow(a1), run_time=0.4)
        with audio.cue("grow"): self.play(Create(boxes[1]), Write(texs[1]), run_time=0.7)
        with audio.cue("slide"): self.play(GrowArrow(a2), run_time=0.4)
        with audio.cue("grow", pan=0.4): self.play(Create(boxes[2]), Write(texs[2]), run_time=0.7)
        l1 = T("nonlinear", 20).move_to([-1.3, 0.55, 0])
        l2 = T("linear", 20).move_to([1.3, 0.55, 0])
        with audio.cue("type", glyphs=15): self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        r1, t1 = self.card(r"Nonlinear in $\boldsymbol{x}$; linear between $\phi(\boldsymbol{x})$ and $f(\boldsymbol{x})$", -1.55, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Also linear between $\boldsymbol{\alpha}$ and $f(\boldsymbol{x})$", -2.5, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        n1 = self.note_in(audio, r"Equivalent to applying $\phi$ first, then a linear model.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, e, n83, box] + boxes + texs + [a1, a2, l1, l2, r1, t1, r2, t2, n1]

    # E - why the kernel trick is powerful
    def scene_e(self, audio):
        items = self.heading_in(audio, "Why It Is Powerful")
        n0 = self.note_in(audio, "Reason one: nonlinear models with convex optimization.", 2.35, 22)
        # left: nonlinear data in 1D; right: linearly separable after phi
        ax1 = self.axes([-3, 3, 1], [0, 1, 1], 3.0, 0.2, [-2.0, 1.3, 0])
        ax2 = self.axes([-3, 3, 1], [0, 3, 1], 3.0, 1.6, [2.0, 0.9, 0])
        with audio.cue("draw"): self.play(Create(ax1), Create(ax2), run_time=0.8)
        xs_in = [-0.4, -0.15, 0.1, 0.35]; xs_out = [-2.3, -1.8, 1.8, 2.3]
        d_in = [Dot(ax1.c2p(x, 0), radius=0.09, color=K) for x in xs_in]
        d_out = [Square(side_length=0.17, color=K, stroke_width=3).move_to(ax1.c2p(x, 0)) for x in xs_out]
        with audio.cue("grow", pan=-0.4): self.play(*[GrowFromCenter(d) for d in d_in + d_out], run_time=0.8)
        arr = Arrow([-0.3, 1.1, 0], [0.3, 1.1, 0], color=K, buff=0, stroke_width=4, tip_length=0.18)
        pl = Mx(r"\phi", size=30).next_to(arr, UP, buff=0.05)
        with audio.cue("slide"): self.play(GrowArrow(arr), FadeIn(pl), run_time=0.6)
        p_in = [Dot(ax2.c2p(x, x * x / 3), radius=0.09, color=K) for x in xs_in]
        p_out = [Square(side_length=0.17, color=K, stroke_width=3).move_to(ax2.c2p(x, x * x / 3)) for x in xs_out]
        with audio.cue("grow", pan=0.4): self.play(*[GrowFromCenter(d) for d in p_in + p_out], run_time=0.8)
        cut = dashed(Line(ax2.c2p(-3, 0.85), ax2.c2p(3, 0.85), color=K, stroke_width=4), 16, 0.5)
        with audio.cue("slide", pan=0.3): self.play(Create(cut), run_time=0.8)
        r1, t1 = self.card(r"$\phi$ fixed: optimize only $\boldsymbol{\alpha}$, linear in a new space", -0.35, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Convex optimization: guaranteed to converge efficiently", -1.35, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        n1 = self.note_in(audio, "Reason two: the kernel function k often has a cheaper form,", -2.45, 22)
        n2 = self.note_in(audio, "so we avoid computing phi explicitly.", -3.1, 22)
        self.wait(1.4)
        return items + [n0, ax1, ax2] + d_in + d_out + [arr, pl] + p_in + p_out + [cut, r1, t1, r2, t2, n1, n2]

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
    Page_139().render()
