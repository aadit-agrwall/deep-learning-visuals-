from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "131"
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


class Page_131(Chapter5Scene):
    PAGE_NO = "131"

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

    def card(self, text, y, size=26, h=0.9):
        r = RoundedRectangle(width=7.2, height=h, corner_radius=0.2, stroke_color=K,
                             stroke_width=3, fill_opacity=0).move_to([0, y, 0])
        t = Tex(text, color=K, font_size=size); fit(t, 6.8); t.move_to(r)
        return r, t

    # A - conditional MLE (5.62)
    def scene_a(self, audio):
        items = self.heading_in(audio, "Conditional Log-Likelihood")
        n0 = self.note_in(audio, r"Estimate $P(\mathbf{y}\mid\mathbf{x};\boldsymbol{\theta})$ to predict $\mathbf{y}$ given $\mathbf{x}$.", 2.25, 26)
        n1 = self.note_in(audio, "The basis of most supervised learning.", 1.6, 28)

        bx = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2, stroke_color=K, stroke_width=3).move_to([-2.4, 0.3, 0])
        tx = T(r"Inputs $\boldsymbol{X}$", 28).move_to(bx)
        by = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2, stroke_color=K, stroke_width=3).move_to([2.4, 0.3, 0])
        ty = T(r"Targets $\boldsymbol{Y}$", 28).move_to(by)
        with audio.cue("grow", pan=-0.3): self.play(Create(bx), Write(tx), run_time=0.9)
        ar = Arrow(bx.get_right(), by.get_left(), color=K, buff=0.1, stroke_width=5)
        with audio.cue("slide"): self.play(GrowArrow(ar), run_time=0.7)
        with audio.cue("grow", pan=0.3): self.play(Create(by), Write(ty), run_time=0.9)

        eq = Mx(r"\boldsymbol{\theta}_{\mathrm{ML}}=\underset{\boldsymbol{\theta}}{\arg\max}\;P(\boldsymbol{Y}\mid\boldsymbol{X};\boldsymbol{\theta})", size=40)
        fit(eq, 5.7); eq.move_to([-0.35, -1.3, 0])
        n62 = T("(5.62)", 28).move_to([3.3, -1.3, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.5)
        self.play(FadeIn(n62), run_time=0.25)
        box = SurroundingRectangle(eq, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        n2 = self.note_in(audio, "The conditional maximum likelihood estimator.", -2.7, 28)
        self.wait(1.5)
        return items + [n0, n1, bx, tx, ar, by, ty, eq, n62, box, n2]

    # B - i.i.d. decomposition (5.63)
    def scene_b(self, audio):
        items = self.heading_in(audio, "The i.i.d. Decomposition")
        n0 = self.note_in(audio, "If the examples are assumed to be i.i.d.,", 2.25, 28)
        l1 = Mx(r"P(\boldsymbol{Y}\mid\boldsymbol{X};\boldsymbol{\theta})=\prod_{i=1}^{m}P(\boldsymbol{y}^{(i)}\mid\boldsymbol{x}^{(i)};\boldsymbol{\theta})", size=36)
        fit(l1, 6.6); l1.move_to([0, 1.3, 0])
        with audio.cue("draw"): self.play(Write(l1), run_time=1.5)
        ar = Arrow([0, 0.65, 0], [0, -0.05, 0], color=K, buff=0, stroke_width=5)
        lg = T(r"take $\log$", 26).next_to(ar, RIGHT, buff=0.15)
        with audio.cue("slide"): self.play(GrowArrow(ar), FadeIn(lg), run_time=0.8)
        l2 = Mx(r"\boldsymbol{\theta}_{\mathrm{ML}}=\underset{\boldsymbol{\theta}}{\arg\max}\sum_{i=1}^{m}\log P(\boldsymbol{y}^{(i)}\mid\boldsymbol{x}^{(i)};\boldsymbol{\theta})", size=36)
        fit(l2, 5.9); l2.move_to([-0.35, -1.0, 0])
        n63 = T("(5.63)", 28).move_to([3.3, -1.0, 0])
        with audio.cue("draw"): self.play(Write(l2), run_time=1.6)
        self.play(FadeIn(n63), run_time=0.25)
        box = SurroundingRectangle(l2, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        n1 = self.note_in(audio, "The problem decomposes into a sum over examples.", -2.5, 26)
        self.wait(1.5)
        return items + [n0, l1, ar, lg, l2, n63, box, n1]

    # C - linear regression revisited
    def scene_c(self, audio):
        items = self.heading_in(audio, "Linear Regression Revisited")
        n0 = self.note_in(audio, r"Not one prediction $\hat y$, but a distribution $p(y\mid\boldsymbol{x})$.", 2.3, 26)

        ax = Axes(x_range=[0, 6, 1], y_range=[0, 4.4, 1], x_length=5.4, y_length=3.2, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.3, 0])
        xl = Mx(r"\boldsymbol{x}", size=34).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        yl = Mx("y", size=34).next_to(ax.y_axis.get_end(), LEFT, buff=0.15)
        with audio.cue("draw"): self.play(Create(ax), Write(xl), Write(yl), run_time=1.0)

        line = ax.plot(lambda x: 0.55 * x + 0.6, x_range=[0.2, 5.8], color=K, stroke_width=6)
        with audio.cue("slide", pan=-0.3): self.play(Create(line), run_time=1.3)

        rng = np.random.default_rng(131)
        pts = VGroup()
        for xv in np.linspace(0.5, 5.5, 22):
            yv = float(np.clip(0.55 * xv + 0.6 + rng.normal(0, 0.4), 0.1, 4.2))
            pts.add(Dot(ax.c2p(xv, yv), radius=0.06, color=K))
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in pts], lag_ratio=0.08), run_time=2.0)

        bumps = VGroup()
        for x0 in (1.5, 3.2, 4.9):
            mu = 0.55 * x0 + 0.6
            bumps.add(ParametricFunction(
                lambda t, x0=x0, mu=mu: ax.c2p(x0 + 0.85 * np.exp(-(t - mu) ** 2 / (2 * 0.4 ** 2)), t),
                t_range=[mu - 1.2, mu + 1.2], color=K, stroke_width=5))
        with audio.cue("slide", pan=0.3):
            self.play(LaggedStart(*[Create(b) for b in bumps], lag_ratio=0.3), run_time=1.8)
        n1 = self.note_in(audio, r"Same input $\boldsymbol{x}$, different values of $y$.", -2.7, 28)
        self.wait(1.4)
        return items + [n0, ax, xl, yl, line, pts, bumps, n1]

    # D - Gaussian model with fixed variance
    def scene_d(self, audio):
        items = self.heading_in(audio, "A Gaussian Conditional Model")
        n0 = self.note_in(audio, "To recover linear regression we define", 2.25, 28)
        eq = Mx(r"p(y\mid\boldsymbol{x})=\mathcal{N}\left(y;\,\hat y(\boldsymbol{x};\boldsymbol{w}),\,\sigma^2\right)", size=40)
        fit(eq, 6.4); eq.move_to([0, 1.4, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.6)
        box = SurroundingRectangle(eq, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)

        r1, t1 = self.card(r"$\hat y(\boldsymbol{x};\boldsymbol{w})$ predicts the \textbf{mean} of the Gaussian", 0.15)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"The variance $\sigma^2$ is a \textbf{fixed} constant", -0.95)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)

        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.7, 0.35], x_length=5.6, y_length=1.4, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -2.3, 0])
        g = lambda mu, s: (lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)))
        c0 = ax.plot(g(-1.0, 0.8), x_range=[-3.5, 3.5], color=K, stroke_width=6)
        c1 = ax.plot(g(1.0, 0.8), x_range=[-3.5, 3.5], color=K, stroke_width=6)
        mm = Mx(r"\hat y", size=32).next_to(ax.c2p(-1.0, 0), DOWN, buff=0.12)
        with audio.cue("draw"): self.play(Create(ax), Create(c0), Write(mm), run_time=1.2)
        with audio.cue("slide", pan=0.3): self.play(Transform(c0, c1), mm.animate.shift(RIGHT * 2.0), run_time=1.6)
        self.wait(1.4)
        return items + [n0, eq, box, r1, t1, r2, t2, ax, c0, mm]

    # E - equations 5.64, 5.65
    def scene_e(self, audio):
        items = self.heading_in(audio, "Log-Likelihood Becomes MSE")
        n0 = self.note_in(audio, "The conditional log-likelihood is given by", 2.3, 26)
        l1 = Mx(r"\sum_{i=1}^{m}\log p\left(y^{(i)}\mid\boldsymbol{x}^{(i)};\boldsymbol{\theta}\right)", size=38)
        fit(l1, 5.4); l1.move_to([-0.35, 1.45, 0])
        n64 = T("(5.64)", 28).move_to([3.3, 1.45, 0])
        with audio.cue("draw"): self.play(Write(l1), run_time=1.5)
        self.play(FadeIn(n64), run_time=0.25)

        l2 = Mx(r"=-m\log\sigma-\frac{m}{2}\log(2\pi)-",
                r"\sum_{i=1}^{m}\frac{\left\|\hat y^{(i)}-y^{(i)}\right\|^2}{2\sigma^2}", size=36)
        fit(l2, 5.9); l2.move_to([-0.35, 0.15, 0])
        n65 = T("(5.65)", 28).move_to([3.3, 0.15, 0])
        with audio.cue("draw"): self.play(Write(l2), run_time=2.0)
        self.play(FadeIn(n65), run_time=0.25)

        box = SurroundingRectangle(l2[1], color=K, buff=0.14, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.7)
        t1 = self.note_in(audio, "Only this term depends on the parameters:", -1.1, 26)
        t2 = self.note_in(audio, "the sum of squared errors, i.e. the MSE.", -1.75, 28)
        r, t = self.card(r"Maximum likelihood $=$ minimum mean squared error", -2.85, 26, 0.95)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.4)
        self.wait(1.6)
        return items + [n0, l1, n64, l2, n65, box, t1, t2, r, t]

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
    Page_131().render()
