from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "133"
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


class Page_133(Chapter5Scene):
    PAGE_NO = "133"

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

    # A - Cramer-Rao lower bound
    def scene_a(self, audio):
        items = self.heading_in(audio, r"Cram\'er--Rao Lower Bound")
        n0 = self.note_in(audio, r"The parametric MSE decreases as $m$ increases:", 2.3, 26)
        eq = Mx(r"\mathbb{E}\left[\left(\hat\theta_m-\theta\right)^2\right]\;\downarrow", size=40)
        fit(eq, 5.8); eq.move_to([0, 1.5, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.4)

        ax = Axes(x_range=[0, 20, 5], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.2, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.5, 0])
        oth = DashedVMobject(ax.plot(lambda x: 1.7 / (x + 0.9), x_range=[1.0, 20], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        ml = ax.plot(lambda x: 0.9 / x, x_range=[1.0, 20], color=K, stroke_width=7)
        xl = Mx("m", size=32).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
        yl = T("MSE", 24).next_to(ax.y_axis.get_end(), LEFT, buff=0.1)
        with audio.cue("draw"): self.play(Create(ax), Write(xl), Write(yl), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Create(oth), run_time=1.3)
        with audio.cue("slide", pan=0.3): self.play(Create(ml), run_time=1.3)
        l1 = T("maximum likelihood", 22).move_to(ax.c2p(13.5, 0.2))
        l2 = T("other consistent estimator", 22).move_to(ax.c2p(12.5, 0.55))
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        n1 = self.note_in(audio, "For large $m$, no consistent estimator", -2.35, 26)
        n2 = self.note_in(audio, "has a lower MSE than maximum likelihood.", -2.95, 26)
        self.wait(1.5)
        return items + [n0, eq, ax, oth, ml, xl, yl, l1, l2, n1, n2]

    # B - why ML is preferred, regularization
    def scene_b(self, audio):
        items = self.heading_in(audio, "Why Maximum Likelihood?")
        r1, t1 = self.card(r"\textbf{Consistency}: converges to the true value", 2.0, 26, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"\textbf{Efficiency}: lowest MSE for large $m$", 0.85, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        ar = Arrow([0, 0.3, 0], [0, -0.35, 0], color=K, buff=0, stroke_width=5)
        with audio.cue("slide"): self.play(GrowArrow(ar), run_time=0.6)
        r3, t3 = self.card(r"Preferred estimator for machine learning", -0.95, 26, 0.9)
        with audio.cue("grow"): self.play(Create(r3), Write(t3), run_time=1.2)
        box = SurroundingRectangle(VGroup(r3), color=K, buff=0.08, stroke_width=5)
        with audio.cue("grow"): self.play(Create(box), run_time=0.5)
        n1 = self.note_in(audio, "With few examples, overfitting appears.", -2.0, 26)
        n2 = self.note_in(audio, "Weight decay gives a biased version with less variance.", -2.7, 24)
        self.wait(1.5)
        return items + [r1, t1, r2, t2, ar, r3, t3, box, n1, n2]

    # C - frequentist vs Bayesian
    def scene_c(self, audio):
        items = self.heading_in(audio, "5.6 Bayesian Statistics")
        n0 = self.note_in(audio, "Consider all possible values of $\\boldsymbol{\\theta}$.", 2.25, 28)
        r1, t1 = self.card(r"\textbf{Frequentist}: $\boldsymbol{\theta}$ is fixed but unknown", 1.2, 26, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"the estimate $\hat{\boldsymbol{\theta}}$ is a random variable", 0.15, 26, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        r3, t3 = self.card(r"\textbf{Bayesian}: the data is observed, not random", -1.25, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r3), Write(t3), run_time=1.2)
        r4, t4 = self.card(r"$\boldsymbol{\theta}$ is uncertain, so a random variable", -2.3, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r4), Write(t4), run_time=1.2)
        n1 = self.note_in(audio, "Probability reflects degrees of certainty.", -3.2, 26)
        self.wait(1.5)
        return items + [n0, r1, t1, r2, t2, r3, t3, r4, t4, n1]

    # D - the prior
    def scene_d(self, audio):
        items = self.heading_in(audio, "The Prior Distribution")
        n0 = self.note_in(audio, r"Before seeing data, our knowledge of $\boldsymbol{\theta}$ is", 2.3, 26)
        eq = Mx(r"p(\boldsymbol{\theta})", size=46).move_to([0, 1.5, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.2)

        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.9, 0.5], x_length=5.6, y_length=2.0, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.4, 0])
        flat = Line(ax.c2p(-2.5, 0.25), ax.c2p(2.5, 0.25), color=K, stroke_width=7)
        e1 = Line(ax.c2p(-2.5, 0), ax.c2p(-2.5, 0.25), color=K, stroke_width=4)
        e2 = Line(ax.c2p(2.5, 0), ax.c2p(2.5, 0.25), color=K, stroke_width=4)
        peak = DashedVMobject(ax.plot(lambda x: np.exp(-x ** 2 / (2 * 0.6 ** 2)) / (0.6 * np.sqrt(2 * np.pi)),
                                      x_range=[-3.5, 3.5], color=K, stroke_width=5),
                              num_dashes=40, dashed_ratio=0.55)
        th = Mx(r"\boldsymbol{\theta}", size=30).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
        with audio.cue("draw"): self.play(Create(ax), Write(th), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Create(flat), Create(e1), Create(e2), run_time=1.2)
        l1 = T("broad, high entropy (uniform)", 22).move_to(ax.c2p(-1.6, 0.62))
        with audio.cue("grow"): self.play(FadeIn(l1), run_time=0.5)
        with audio.cue("slide", pan=0.3): self.play(Create(peak), run_time=1.3)
        l2 = T("prefers simpler solutions", 22).move_to(ax.c2p(1.9, 0.78))
        with audio.cue("grow"): self.play(FadeIn(l2), run_time=0.5)
        n1 = self.note_in(audio, "Often broad, to reflect a high degree of uncertainty.", -2.1, 24)
        n2 = self.note_in(audio, "Or a preference for small coefficients.", -2.75, 26)
        self.wait(1.5)
        return items + [n0, eq, ax, flat, e1, e2, peak, th, l1, l2, n1, n2]

    # E - Bayes rule (5.67)
    def scene_e(self, audio):
        items = self.heading_in(audio, "Bayes' Rule")
        n0 = self.note_in(audio, "Combine the data likelihood with the prior:", 2.3, 28)
        eq = Mx(r"p\left(\boldsymbol{\theta}\mid x^{(1)},\ldots,x^{(m)}\right)", "=",
                r"\frac{p\left(x^{(1)},\ldots,x^{(m)}\mid\boldsymbol{\theta}\right)\,p(\boldsymbol{\theta})}{p\left(x^{(1)},\ldots,x^{(m)}\right)}", size=34)
        fit(eq, 5.9); eq.move_to([-0.35, 0.9, 0])
        n67 = T("(5.67)", 28).move_to([3.3, 0.9, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=2.2)
        self.play(FadeIn(n67), run_time=0.25)
        box = SurroundingRectangle(eq[0], color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        t1 = self.note_in(audio, r"Left: belief about $\boldsymbol{\theta}$ after seeing the data.", -0.5, 26)
        t2 = self.note_in(audio, r"Top: likelihood of the data times the prior.", -1.2, 26)
        r, t = self.card(r"Data updates our belief about $\boldsymbol{\theta}$", -2.4, 28, 0.95)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.3)
        self.wait(1.6)
        return items + [n0, eq, n67, box, t1, t2, r, t]

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
    Page_133().render()
