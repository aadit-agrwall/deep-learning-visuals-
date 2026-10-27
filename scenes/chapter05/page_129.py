from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "129"
PAGE_SRC = Path(f"assets/bookpage/page_{PAGE}.png")
BAND_DIR = Path(f"assets/bookpage/page_{PAGE}_bands")
CUE_FILE = f"/tmp/p{PAGE}_cues.json"
WHITE_BG = "#FFFFFF"; K = "#000000"; MIN_SECONDS = 62.0


class _Ctx:
    """Context manager that records start AND end time of a cue."""
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


class Page_129(Chapter5Scene):
    PAGE_NO = "129"

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

    def verdict_card(self, left, verdict, y, yes=True):
        r = RoundedRectangle(width=7.0, height=0.95, corner_radius=0.2, stroke_color=K,
                             stroke_width=3, fill_opacity=0).move_to([0, y, 0])
        t = Tex(left, color=K, font_size=30); fit(t, 4.8)
        t.move_to(r.get_left() + RIGHT * (t.width / 2 + 0.3))
        if yes:
            b = RoundedRectangle(width=1.1, height=0.6, corner_radius=0.15, stroke_color=K,
                                 stroke_width=3, fill_opacity=0)
            w = Tex(r"\textbf{" + verdict + "}", color=K, font_size=30)
        else:
            b = RoundedRectangle(width=1.1, height=0.6, corner_radius=0.15, stroke_color=K,
                                 stroke_width=3, fill_color=K, fill_opacity=1)
            w = Tex(r"\textbf{" + verdict + "}", color=WHITE_BG, font_size=30)
        b.move_to([2.6, y, 0]); w.move_to(b)
        return VGroup(r, t, b, w)

    # ---------------------------------------------------------
    # A - almost sure convergence
    # ---------------------------------------------------------
    def scene_a(self, audio):
        items = self.heading_in(audio, "Almost Sure Convergence")
        n1 = self.note_in(audio, r"A sequence of random variables $\mathbf{x}^{(1)},\mathbf{x}^{(2)},\ldots$", 2.05, 28)
        n2 = self.note_in(audio, r"converges to a value $\boldsymbol{x}$ when", 1.45, 28)
        eq = Mx(r"p\left(\lim_{m\to\infty}\mathbf{x}^{(m)}=\boldsymbol{x}\right)=1", size=42)
        fit(eq, 6.6); eq.move_to([0, 0.6, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.5)
        box = SurroundingRectangle(eq, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)

        ax = Axes(x_range=[0, 14, 2], y_range=[-1, 1, 1], x_length=5.6, y_length=2.0, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.45, 0])
        xl = Mx(r"\boldsymbol{x}", size=34).next_to(ax.c2p(14, 0), RIGHT, buff=0.12)
        ml = Mx("m", size=32).next_to(ax.c2p(14, 0), UP, buff=0.15)
        with audio.cue("draw"): self.play(Create(ax), Write(xl), Write(ml), run_time=1.0)
        dots = VGroup(*[Dot(ax.c2p(m, 0.9 * (-1) ** m / m), radius=0.07, color=K) for m in range(1, 14)])
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), run_time=2.4)
        n3 = self.note_in(audio, r"The sequence settles on $\boldsymbol{x}$ with probability 1.", -3.15, 28)
        self.wait(1.5)
        return items + [n1, n2, eq, box, ax, xl, ml, dots, n3]

    # ---------------------------------------------------------
    # B - unbiased, not consistent
    # ---------------------------------------------------------
    def scene_b(self, audio):
        items = self.heading_in(audio, "Unbiased but Not Consistent")
        n1 = self.note_in(audio, r"Estimate the mean $\mu$ of $\mathcal{N}(x;\mu,\sigma^2)$ from $m$ samples", 2.05, 26)
        n2 = self.note_in(audio, "Use only the first sample as the estimator:", 1.45, 26)
        eq = Mx(r"\hat\theta_m=x^{(1)}", size=42); eq.move_to([0, 0.75, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.2)

        ax = Axes(x_range=[0, 40, 10], y_range=[-1.5, 1.5, 1], x_length=5.6, y_length=2.4, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.2, 0])
        truth = DashedLine(ax.c2p(0, 0), ax.c2p(40, 0), color=K, stroke_width=5)
        tl = Mx(r"\theta", size=36).next_to(ax.c2p(40, 0), RIGHT, buff=0.12)
        ml = Mx("m", size=32).next_to(ax, DOWN, buff=0.15)
        with audio.cue("draw"): self.play(Create(ax), Create(truth), Write(tl), Write(ml), run_time=1.1)

        runs = []
        for o in (0.95, -0.55, 0.3, -1.05):
            runs.append(Line(ax.c2p(1, o), ax.c2p(40, o), color=K, stroke_width=4))
        with audio.cue("slide", pan=0.2):
            self.play(LaggedStart(*[Create(r) for r in runs], lag_ratio=0.35), run_time=2.2)
        n3 = self.note_in(audio, r"It never settles on $\theta$, however large $m$ grows.", -3.3, 28)
        self.wait(1.5)
        return items + [n1, n2, eq, ax, truth, tl, ml, n3] + runs

    # ---------------------------------------------------------
    # C - verdict cards
    # ---------------------------------------------------------
    def scene_c(self, audio):
        items = self.heading_in(audio, "Why Unbiased Is Not Enough")
        specs = [(r"Unbiased: $\mathbb{E}(\hat\theta_m)=\theta$", "Yes", True, 1.8, -0.3),
                 (r"Asymptotically unbiased", "Yes", True, 0.5, 0.0),
                 (r"Consistent: $\hat\theta_m\to\theta$ as $m\to\infty$", "No", False, -0.8, 0.3)]
        for left, verdict, yes, y, pan in specs:
            g = self.verdict_card(left, verdict, y, yes)
            with audio.cue("grow", pan=pan): self.play(GrowFromCenter(g), run_time=0.8)
            self.wait(0.5)
            items.append(g)
        n1 = self.note_in(audio, "Consistency means the bias diminishes as data grows.", -2.1, 27)
        n2 = self.note_in(audio, "The reverse is not true.", -2.75, 30)
        self.wait(1.6)
        return items + [n1, n2]

    # ---------------------------------------------------------
    # D - maximum likelihood setup
    # ---------------------------------------------------------
    def scene_d(self, audio):
        items = self.heading_in(audio, "5.5 Maximum Likelihood")
        n1 = self.note_in(audio, "The most common principle for deriving estimators.", 2.05, 28)
        eq = Mx(r"\mathbb{X}=\{\boldsymbol{x}^{(1)},\ldots,\boldsymbol{x}^{(m)}\}", size=40)
        fit(eq, 6.0); eq.move_to([0, 1.2, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.3)
        n2 = self.note_in(audio, r"drawn independently from the unknown $p_{\mathrm{data}}(\mathbf{x})$", 0.5, 26)
        n3 = self.note_in(audio, r"Model: $p_{\mathrm{model}}(\mathbf{x};\boldsymbol{\theta})$ indexed by $\boldsymbol{\theta}$", -0.2, 26)

        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.7, 0.35], x_length=5.6, y_length=1.5, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -2.1, 0])
        pm = lambda mu, s: (lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)))
        cdata = ax.plot(pm(0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=6)
        cm0 = DashedVMobject(ax.plot(pm(1.4, 0.6), x_range=[-3.5, 3.5], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        cm1 = DashedVMobject(ax.plot(pm(0.15, 1.05), x_range=[-3.5, 3.5], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        ld = Mx(r"p_{\mathrm{data}}", size=28).move_to(ax.c2p(-2.5, 0.42))
        lm = Mx(r"p_{\mathrm{model}}", size=28).move_to(ax.c2p(2.6, 0.42))
        with audio.cue("draw"): self.play(Create(ax), Create(cdata), Write(ld), run_time=1.3)
        rng = np.random.default_rng(129)
        dots = VGroup(*[Dot(ax.c2p(float(np.clip(x, -3.2, 3.2)), 0.02), radius=0.07, color=K)
                        for x in rng.normal(0, 1, 14)])
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=2.0)
        with audio.cue("slide", pan=0.3): self.play(Create(cm0), Write(lm), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Transform(cm0, cm1), run_time=1.6)
        self.wait(1.4)
        return items + [n1, eq, n2, n3, ax, cdata, cm0, ld, lm, dots]

    # ---------------------------------------------------------
    # E - equations 5.56, 5.57
    # ---------------------------------------------------------
    def scene_e(self, audio):
        items = self.heading_in(audio, "Maximum Likelihood Estimator")
        l1 = Mx(r"\boldsymbol{\theta}_{\mathrm{ML}}=\underset{\boldsymbol{\theta}}{\arg\max}\;p_{\mathrm{model}}(\mathbb{X};\boldsymbol{\theta})", size=38)
        fit(l1, 5.9); l1.move_to([-0.35, 1.9, 0])
        n1 = T("(5.56)", 28).move_to([3.3, 1.9, 0])
        with audio.cue("draw"): self.play(Write(l1), run_time=1.5)
        self.play(FadeIn(n1), run_time=0.25)
        l2 = Mx(r"=\underset{\boldsymbol{\theta}}{\arg\max}\prod_{i=1}^{m}p_{\mathrm{model}}(\boldsymbol{x}^{(i)};\boldsymbol{\theta})", size=38)
        fit(l2, 5.9); l2.move_to([-0.35, 0.6, 0])
        n2 = T("(5.57)", 28).move_to([3.3, 0.6, 0])
        with audio.cue("draw"): self.play(Write(l2), run_time=1.5)
        self.play(FadeIn(n2), run_time=0.25)
        box = SurroundingRectangle(l2, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)

        t1 = self.note_in(audio, "A product of many probabilities is prone to underflow:", -0.7, 26)
        pr = Mx(r"0.1\times0.1\times0.1\times\cdots\times0.1\;\to\;0", size=34)
        fit(pr, 6.8); pr.move_to([0, -1.5, 0])
        with audio.cue("draw"): self.play(Write(pr), run_time=1.4)
        t2 = self.note_in(audio, r"Taking the logarithm does not change the $\arg\max$,", -2.4, 26)
        t3 = self.note_in(audio, "but conveniently transforms the product.", -3.0, 26)
        self.wait(1.6)
        return items + [l1, n1, l2, n2, box, t1, pr, t2, t3]

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
    Page_129().render()
