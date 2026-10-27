from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "134"
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


class Page_134(Chapter5Scene):
    PAGE_NO = "134"

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

    # A - prior becomes posterior
    def scene_a(self, audio):
        items = self.heading_in(audio, "Prior to Posterior")
        n0 = self.note_in(audio, "The prior is relatively uniform or Gaussian, with high entropy.", 2.3, 24)
        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 1.4, 0.5], x_length=5.8, y_length=2.8, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, 0.1, 0])
        g = lambda mu, s: (lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)))
        prior = DashedVMobject(ax.plot(g(0, 1.5), x_range=[-3.5, 3.5], color=K, stroke_width=5),
                               num_dashes=40, dashed_ratio=0.55)
        post = ax.plot(g(0.8, 0.35), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        th = Mx(r"\boldsymbol{\theta}", size=30).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
        with audio.cue("draw"): self.play(Create(ax), Write(th), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Create(prior), run_time=1.3)
        l1 = T("prior: high entropy", 22).move_to(ax.c2p(-2.0, 0.4))
        with audio.cue("grow"): self.play(FadeIn(l1), run_time=0.5)
        dots = VGroup(*[Dot(ax.c2p(float(x), 0.03), radius=0.06, color=K)
                        for x in np.random.default_rng(134).normal(0.8, 0.4, 10)])
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), run_time=1.6)
        with audio.cue("slide", pan=0.3): self.play(Create(post), run_time=1.5)
        l2 = T("posterior: concentrated", 22).move_to(ax.c2p(2.2, 1.1))
        with audio.cue("grow"): self.play(FadeIn(l2), run_time=0.5)
        n1 = self.note_in(audio, "Observing data makes the posterior lose entropy,", -2.3, 26)
        n2 = self.note_in(audio, "concentrating around a few likely values.", -2.95, 26)
        self.wait(1.5)
        return items + [n0, ax, prior, post, th, l1, l2, dots, n1, n2]

    # B - point estimate vs full distribution
    def scene_b(self, audio):
        items = self.heading_in(audio, "Two Differences from ML")
        n0 = self.note_in(audio, "First difference: what we predict with.", 2.3, 28)
        r1, t1 = self.card(r"\textbf{Maximum likelihood}: a point estimate of $\boldsymbol{\theta}$", 1.35, 26, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        ax1 = NumberLine(x_range=[-3, 3, 1], length=5.0, color=K, stroke_width=3,
                         include_numbers=False).move_to([0, 0.35, 0])
        pt = Dot(ax1.n2p(0.8), radius=0.13, color=K).set_z_index(5)
        with audio.cue("draw"): self.play(Create(ax1), GrowFromCenter(pt), run_time=0.9)
        r2, t2 = self.card(r"\textbf{Bayesian}: a full distribution over $\boldsymbol{\theta}$", -0.7, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        ax2 = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 1], x_length=5.0, y_length=1.2, tips=False,
                   axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -2.1, 0])
        bell = ax2.plot(lambda x: np.exp(-(x - 0.8) ** 2 / (2 * 0.6 ** 2)), x_range=[-3, 3], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax2), run_time=0.7)
        with audio.cue("slide", pan=0.3): self.play(Create(bell), run_time=1.3)
        n1 = self.note_in(audio, "Every plausible value contributes to the prediction.", -3.2, 24)
        self.wait(1.5)
        return items + [n0, r1, t1, ax1, pt, r2, t2, ax2, bell, n1]

    # C - equation 5.68
    def scene_c(self, audio):
        items = self.heading_in(audio, "The Predictive Distribution")
        n0 = self.note_in(audio, r"After $m$ examples, predict the next sample $x^{(m+1)}$:", 2.3, 26)
        eq = Mx(r"p\left(x^{(m+1)}\mid x^{(1)},\ldots,x^{(m)}\right)=",
                r"\int p\left(x^{(m+1)}\mid\boldsymbol{\theta}\right)",
                r"p\left(\boldsymbol{\theta}\mid x^{(1)},\ldots,x^{(m)}\right)d\boldsymbol{\theta}", size=30)
        fit(eq, 5.9); eq.move_to([-0.35, 0.9, 0])
        n68 = T("(5.68)", 28).move_to([3.3, 0.9, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=2.4)
        self.play(FadeIn(n68), run_time=0.25)
        box = SurroundingRectangle(eq[2], color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        t1 = self.note_in(audio, r"Each $\boldsymbol{\theta}$ with positive density contributes,", -0.6, 26)
        t2 = self.note_in(audio, "weighted by the posterior density itself.", -1.25, 26)
        r, t = self.card(r"Remaining uncertainty enters the prediction", -2.5, 26, 0.95)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.3)
        self.wait(1.6)
        return items + [n0, eq, n68, box, t1, t2, r, t]

    # D - integrate over uncertainty
    def scene_d(self, audio):
        items = self.heading_in(audio, "Integrate Over Uncertainty")
        r1, t1 = self.card(r"\textbf{Frequentist}: evaluate the variance of the estimator", 2.0, 24, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        n1 = self.note_in(audio, "How the estimate changes with alternative samplings.", 1.1, 24)
        r2, t2 = self.card(r"\textbf{Bayesian}: simply integrate over the uncertainty", -0.2, 24, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        ig = Mx(r"\int\cdots\,d\boldsymbol{\theta}", size=54).move_to([-1.9, -1.7, 0])
        with audio.cue("draw"): self.play(Write(ig), run_time=1.0)
        ar = Arrow(ig.get_right() + RIGHT * 0.1, [1.0, -1.7, 0], color=K, buff=0.05, stroke_width=5)
        with audio.cue("slide"): self.play(GrowArrow(ar), run_time=0.7)
        pr = T("protects against overfitting", 26).move_to([2.2, -1.7, 0])
        fit(pr, 2.9)
        with audio.cue("type", glyphs=28): self.play(Write(pr), run_time=1.1)
        n2 = self.note_in(audio, "Just the laws of probability: simple to justify.", -2.6, 26)
        n3 = self.note_in(audio, "A point estimate is a rather ad hoc summary.", -3.2, 26)
        self.wait(1.5)
        return items + [r1, t1, n1, r2, t2, ig, ar, pr, n2, n3]

    # E - prior influence and trade-off
    def scene_e(self, audio):
        items = self.heading_in(audio, "Prior Influence and Cost")
        n0 = self.note_in(audio, "The prior shifts probability mass toward preferred regions.", 2.3, 24)
        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 1.2, 1], x_length=5.4, y_length=1.8, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, 0.9, 0])
        g = lambda mu, s: (lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)))
        c0 = ax.plot(g(1.5, 0.7), x_range=[-3.5, 3.5], color=K, stroke_width=6)
        c1 = ax.plot(g(0.4, 0.7), x_range=[-3.5, 3.5], color=K, stroke_width=6)
        with audio.cue("draw"): self.play(Create(ax), Create(c0), run_time=1.1)
        with audio.cue("slide", pan=-0.3): self.play(Transform(c0, c1), run_time=1.5)
        n1 = self.note_in(audio, "Often a preference for simpler or smoother models.", -0.3, 26)
        r1, t1 = self.card(r"Critics: the prior brings subjective human judgment", -1.3, 24, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"Limited data: generalizes much better", -2.35, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        r3, t3 = self.card(r"Large data: high computational cost", -3.4, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r3), Write(t3), run_time=1.2)
        self.wait(1.5)
        return items + [n0, ax, c0, n1, r1, t1, r2, t2, r3, t3]

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
    Page_134().render()
