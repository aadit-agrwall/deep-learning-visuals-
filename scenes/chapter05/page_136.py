from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "136"
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


class Page_136(Chapter5Scene):
    PAGE_NO = "136"

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

    # A - expanding the posterior, eq 5.75 and 5.76
    def scene_a(self, audio):
        items = self.heading_in(audio, "Expanding the Posterior")
        n0 = self.note_in(audio, "Multiply the likelihood by the prior:", 2.3, 26)
        e1 = Mx(r"\propto\exp\left(-\tfrac{1}{2}(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{w})^{\top}(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{w})\right)",
                r"\exp\left(-\tfrac{1}{2}(\boldsymbol{w}-\boldsymbol{\mu}_0)^{\top}\boldsymbol{\Lambda}_0^{-1}(\boldsymbol{w}-\boldsymbol{\mu}_0)\right)", size=28)
        fit(e1, 6.0); e1.move_to([-0.3, 1.5, 0])
        n75 = T("(5.75)", 28).move_to([3.3, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=2.4)
        self.play(FadeIn(n75), run_time=0.25)
        l1 = T("likelihood", 20).next_to(e1[0], DOWN, buff=0.15)
        l2 = T("prior", 20).next_to(e1[1], DOWN, buff=0.15)
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        ar = Arrow([-0.3, 0.55, 0], [-0.3, -0.05, 0], color=K, buff=0, stroke_width=5, tip_length=0.2)
        al = T("expand", 20).next_to(ar, RIGHT, buff=0.15)
        with audio.cue("slide"): self.play(GrowArrow(ar), FadeIn(al), run_time=0.7)
        e2 = Mx(r"\propto\exp\left(-\tfrac{1}{2}\left(-2\boldsymbol{y}^{\top}\boldsymbol{X}\boldsymbol{w}+\boldsymbol{w}^{\top}\boldsymbol{X}^{\top}\boldsymbol{X}\boldsymbol{w}+\boldsymbol{w}^{\top}\boldsymbol{\Lambda}_0^{-1}\boldsymbol{w}-2\boldsymbol{\mu}_0^{\top}\boldsymbol{\Lambda}_0^{-1}\boldsymbol{w}\right)\right)", size=28)
        fit(e2, 6.0); e2.move_to([-0.3, -0.7, 0])
        n76 = T("(5.76)", 28).move_to([3.3, -0.7, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=2.6)
        self.play(FadeIn(n76), run_time=0.25)
        box = SurroundingRectangle(e2, color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        r, t = self.card(r"Two terms linear in $\boldsymbol{w}$, two quadratic in $\boldsymbol{w}$", -2.0, 24, 0.8)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.2)
        n1 = self.note_in(audio, "Only the terms containing w matter.", -3.0, 24)
        self.wait(1.4)
        return items + [n0, e1, n75, l1, l2, ar, al, e2, n76, box, r, t, n1]

    # B - definitions of Lambda_m and mu_m
    def scene_b(self, audio):
        items = self.heading_in(audio, "Completing the Square")
        n0 = self.note_in(audio, "We now define two new variables:", 2.3, 26)
        e1 = Mx(r"\boldsymbol{\Lambda}_m=\left(\boldsymbol{X}^{\top}\boldsymbol{X}+\boldsymbol{\Lambda}_0^{-1}\right)^{-1}", size=38)
        fit(e1, 6.2); e1.move_to([0, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=1.8)
        e2 = Mx(r"\boldsymbol{\mu}_m=\boldsymbol{\Lambda}_m\left(\boldsymbol{X}^{\top}\boldsymbol{y}+\boldsymbol{\Lambda}_0^{-1}\boldsymbol{\mu}_0\right)", size=38)
        fit(e2, 6.2); e2.move_to([0, 0.55, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=1.8)
        b1 = SurroundingRectangle(e1, color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow", pan=-0.3): self.play(Create(b1), run_time=0.5)
        b2 = SurroundingRectangle(e2, color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow", pan=0.3): self.play(Create(b2), run_time=0.5)
        specs = [(r"\boldsymbol{X}^{\top}\boldsymbol{X}", "data", -2.5),
                 (r"\boldsymbol{\Lambda}_0^{-1}", "prior", 0.0),
                 (r"\boldsymbol{\Lambda}_m^{-1}", "posterior", 2.5)]
        boxes, texs, caps = [], [], []
        for lb, cp, x in specs:
            r = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.2, stroke_color=K,
                                 stroke_width=3, fill_opacity=0).move_to([x, -1.0, 0])
            tx = Mx(lb, size=30).move_to(r)
            c = T(cp, 20).move_to([x, -1.7, 0])
            boxes.append(r); texs.append(tx); caps.append(c)
        plus = Mx(r"+", size=36).move_to([-1.25, -1.0, 0])
        arr = Arrow([1.0, -1.0, 0], [1.55, -1.0, 0], color=K, buff=0, stroke_width=4, tip_length=0.18)
        with audio.cue("grow", pan=-0.4): self.play(Create(boxes[0]), Write(texs[0]), FadeIn(caps[0]), run_time=0.8)
        with audio.cue("slide"): self.play(Write(plus), run_time=0.4)
        with audio.cue("grow"): self.play(Create(boxes[1]), Write(texs[1]), FadeIn(caps[1]), run_time=0.8)
        with audio.cue("slide"): self.play(GrowArrow(arr), run_time=0.5)
        with audio.cue("grow", pan=0.4): self.play(Create(boxes[2]), Write(texs[2]), FadeIn(caps[2]), run_time=0.8)
        n1 = self.note_in(audio, "Precisions add: data and prior both contribute.", -2.6, 24)
        n2 = self.note_in(audio, r"$\boldsymbol{\mu}_m$ blends data with the prior mean $\boldsymbol{\mu}_0$.", -3.2, 24)
        self.wait(1.4)
        return items + [n0, e1, e2, b1, b2] + boxes + texs + caps + [plus, arr, n1, n2]

    # C - Gaussian posterior, eq 5.77 and 5.78
    def scene_c(self, audio):
        items = self.heading_in(audio, "A Gaussian Posterior")
        n0 = self.note_in(audio, "With the new variables the posterior is Gaussian:", 2.3, 24)
        e1 = Mx(r"p(\boldsymbol{w}\mid\boldsymbol{X},\boldsymbol{y})",
                r"\propto\exp\left(-\tfrac{1}{2}(\boldsymbol{w}-\boldsymbol{\mu}_m)^{\top}\boldsymbol{\Lambda}_m^{-1}(\boldsymbol{w}-\boldsymbol{\mu}_m)+\tfrac{1}{2}\boldsymbol{\mu}_m^{\top}\boldsymbol{\Lambda}_m^{-1}\boldsymbol{\mu}_m\right)", size=28)
        fit(e1, 6.0); e1.move_to([-0.3, 1.55, 0])
        n77 = T("(5.77)", 28).move_to([3.3, 1.55, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=2.4)
        self.play(FadeIn(n77), run_time=0.25)
        e2 = Mx(r"\propto\exp\left(-\tfrac{1}{2}(\boldsymbol{w}-\boldsymbol{\mu}_m)^{\top}\boldsymbol{\Lambda}_m^{-1}(\boldsymbol{w}-\boldsymbol{\mu}_m)\right)", size=30)
        fit(e2, 6.0); e2.move_to([-0.3, 0.55, 0])
        n78 = T("(5.78)", 28).move_to([3.3, 0.55, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=2.0)
        self.play(FadeIn(n78), run_time=0.25)
        box = SurroundingRectangle(e2, color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        r, t = self.card(r"Terms without $\boldsymbol{w}$ are omitted: normalization fixes them", -0.45, 22, 0.75)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.2)
        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.5, 1], x_length=5.0, y_length=1.1, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.9, 0])
        bell = ax.plot(gauss(0.3, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=0.3): self.play(Create(bell), run_time=1.2)
        mline = DashedLine(ax.c2p(0.3, 0), ax.c2p(0.3, 0.4), color=K, stroke_width=3)
        mlab = Mx(r"\boldsymbol{\mu}_m", size=26).next_to(ax.c2p(0.3, 0), DOWN, buff=0.08)
        wl = Mx(r"\boldsymbol{\Lambda}_m", size=26).move_to(ax.c2p(2.6, 0.3))
        with audio.cue("grow"): self.play(Create(mline), FadeIn(mlab), FadeIn(wl), run_time=0.7)
        n1 = self.note_in(audio, "Equation 3.23 shows how to normalize a Gaussian.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, e1, n77, e2, n78, box, r, t, ax, bell, mline, mlab, wl, n1]

    # D - intuition: weight decay
    def scene_d(self, audio):
        items = self.heading_in(audio, "Intuition: Weight Decay")
        r1, t1 = self.card(r"Set $\boldsymbol{\mu}_0=\boldsymbol{0}$ and $\boldsymbol{\Lambda}_0=\tfrac{1}{\alpha}\boldsymbol{I}$", 2.1, 26, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"$\boldsymbol{\mu}_m$ equals frequentist fit with penalty $\alpha\boldsymbol{w}^{\top}\boldsymbol{w}$", 1.15, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.7, 1], x_length=5.0, y_length=1.3, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.35, 0])
        narrow = ax.plot(gauss(0, 0.6), x_range=[-4, 4], color=K, stroke_width=7)
        broad = DashedVMobject(ax.plot(gauss(0, 1.8), x_range=[-4, 4], color=K, stroke_width=5),
                               num_dashes=40, dashed_ratio=0.55)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(narrow), run_time=1.2)
        with audio.cue("slide", pan=0.3): self.play(Create(broad), run_time=1.2)
        l1 = Line([-3.6, -1.35, 0], [-3.0, -1.35, 0], color=K, stroke_width=6)
        l1t = T(r"large $\alpha$: narrow prior", 20).next_to(l1, RIGHT, buff=0.15)
        l2 = DashedVMobject(Line([0.4, -1.35, 0], [1.0, -1.35, 0], color=K, stroke_width=5),
                            num_dashes=5, dashed_ratio=0.55)
        l2t = T(r"small $\alpha$: broad prior", 20).next_to(l2, RIGHT, buff=0.15)
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(l1t), FadeIn(l2), FadeIn(l2t), run_time=0.8)
        r3, t3 = self.card(r"Undefined at $\alpha=0$: no infinitely wide prior on $\boldsymbol{w}$", -2.15, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r3), Write(t3), run_time=1.3)
        r4, t4 = self.card(r"Bayes also gives a covariance: how likely every $\boldsymbol{w}$ is", -3.1, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r4), Write(t4), run_time=1.3)
        self.wait(1.4)
        return items + [r1, t1, r2, t2, ax, narrow, broad, l1, l1t, l2, l2t, r3, t3, r4, t4]

    # E - MAP estimation
    def scene_e(self, audio):
        items = self.heading_in(audio, "5.6.1 MAP Estimation")
        n0 = self.note_in(audio, "The full posterior is principled but often intractable.", 2.3, 24)
        r1, t1 = self.card(r"A point estimate is a tractable approximation", 1.4, 24, 0.75)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"Let the prior influence the choice of the point", 0.55, 24, 0.75)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        e = Mx(r"\boldsymbol{\theta}_{\mathrm{MAP}}=\arg\max_{\boldsymbol{\theta}}\,p(\boldsymbol{\theta}\mid\boldsymbol{x})", size=36)
        fit(e, 6.0); e.move_to([0, -0.35, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.6)
        ax = Axes(x_range=[-3, 4, 1], y_range=[0, 0.7, 1], x_length=5.4, y_length=1.2, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.95, 0])
        post = ax.plot(gauss(0.8, 0.7), x_range=[-3, 4], color=K, stroke_width=7)
        like = DashedVMobject(ax.plot(gauss(2.0, 0.9), x_range=[-3, 4], color=K, stroke_width=5),
                              num_dashes=60, dashed_ratio=0.5)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(post), run_time=1.2)
        with audio.cue("slide", pan=0.3): self.play(Create(like), run_time=1.2)
        peak = gauss(0.8, 0.7)(0.8)
        dot = Dot(ax.c2p(0.8, peak), radius=0.11, color=K).set_z_index(5)
        vl = DashedLine(ax.c2p(0.8, 0), ax.c2p(0.8, peak), color=K, stroke_width=3)
        ml = Tex("MAP", color=K, font_size=22).next_to(ax.c2p(0.8, 0), DOWN, buff=0.08)
        vl2 = DashedLine(ax.c2p(2.0, 0), ax.c2p(2.0, gauss(2.0, 0.9)(2.0)), color=K, stroke_width=3)
        ml2 = Tex("ML", color=K, font_size=22).next_to(ax.c2p(2.0, 0), DOWN, buff=0.08)
        with audio.cue("grow"): self.play(GrowFromCenter(dot), Create(vl), FadeIn(ml), run_time=0.7)
        with audio.cue("grow"): self.play(Create(vl2), FadeIn(ml2), run_time=0.6)
        pl = T("posterior", 20).move_to(ax.c2p(-1.9, 0.4))
        ll = T("likelihood", 20).move_to(ax.c2p(3.5, 0.45))
        with audio.cue("type", glyphs=18): self.play(FadeIn(pl), FadeIn(ll), run_time=0.6)
        n1 = self.note_in(audio, "The prior pulls the point away from the ML estimate.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, r1, t1, r2, t2, e, ax, post, like, dot, vl, ml, vl2, ml2, pl, ll, n1]

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
    Page_136().render()
