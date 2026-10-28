from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "135"
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


class Page_135(Chapter5Scene):
    PAGE_NO = "135"

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

    # A - the linear model, eq 5.69 and 5.70
    def scene_a(self, audio):
        items = self.heading_in(audio, "The Linear Model")
        n0 = self.note_in(audio, r"Predict a scalar $y\in\mathbb{R}$ from an input $\boldsymbol{x}\in\mathbb{R}^n$:", 2.3, 24)
        e1 = Mx(r"\hat{y}", r"=", r"\boldsymbol{w}^{\top}\boldsymbol{x}", size=48).move_to([-0.3, 1.3, 0])
        n69 = T("(5.69)", 28).move_to([3.1, 1.3, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=1.5)
        self.play(FadeIn(n69), run_time=0.25)
        labels = [r"\boldsymbol{x}", r"\boldsymbol{w}^{\top}", r"\hat{y}"]
        caps = ["input", "weights", "prediction"]
        xs = [-2.6, 0.0, 2.6]
        boxes, texs, capt = [], [], []
        for lb, cp, x in zip(labels, caps, xs):
            r = RoundedRectangle(width=1.7, height=0.8, corner_radius=0.2, stroke_color=K,
                                 stroke_width=3, fill_opacity=0).move_to([x, 0.0, 0])
            t = Mx(lb, size=30).move_to(r)
            c = T(cp, 20).move_to([x, -0.65, 0])
            boxes.append(r); texs.append(t); capt.append(c)
        arrs = [Arrow([-1.75, 0, 0], [-0.95, 0, 0], color=K, buff=0.0, stroke_width=4, tip_length=0.2),
                Arrow([0.95, 0, 0], [1.75, 0, 0], color=K, buff=0.0, stroke_width=4, tip_length=0.2)]
        for i in range(3):
            with audio.cue("grow", pan=-0.3 + 0.3 * i): self.play(Create(boxes[i]), Write(texs[i]), FadeIn(capt[i]), run_time=0.8)
            if i < 2:
                with audio.cue("slide", pan=-0.2 + 0.3 * i): self.play(GrowArrow(arrs[i]), run_time=0.5)
        n1 = self.note_in(audio, r"Over all $m$ training samples at once:", -1.05, 24)
        e2 = Mx(r"\hat{\boldsymbol{y}}^{(\mathrm{train})}", r"=", r"\boldsymbol{X}^{(\mathrm{train})}", r"\boldsymbol{w}", size=40)
        fit(e2, 5.4); e2.move_to([-0.3, -1.9, 0])
        n70 = T("(5.70)", 28).move_to([3.1, -1.9, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=1.8)
        self.play(FadeIn(n70), run_time=0.25)
        box = SurroundingRectangle(e2[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        n2 = self.note_in(audio, "One matrix product predicts the whole training set.", -3.0, 24)
        self.wait(1.4)
        return items + [n0, e1, n69] + boxes + texs + capt + arrs + [n1, e2, n70, box, n2]

    # B - Gaussian likelihood, eq 5.71 and 5.72
    def scene_b(self, audio):
        items = self.heading_in(audio, "Gaussian Likelihood")
        n0 = self.note_in(audio, r"Model $\boldsymbol{y}^{(\mathrm{train})}$ as a Gaussian conditional distribution:", 2.3, 22)
        e1 = Mx(r"p\left(\boldsymbol{y}^{(\mathrm{train})}\mid\boldsymbol{X}^{(\mathrm{train})},\boldsymbol{w}\right)",
                r"=",
                r"\mathcal{N}\left(\boldsymbol{y}^{(\mathrm{train})};\boldsymbol{X}^{(\mathrm{train})}\boldsymbol{w},\boldsymbol{I}\right)", size=30)
        fit(e1, 5.9); e1.move_to([-0.3, 1.5, 0])
        n71 = T("(5.71)", 28).move_to([3.3, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=2.2)
        self.play(FadeIn(n71), run_time=0.25)
        box = SurroundingRectangle(e1[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        e2 = Mx(r"\propto\exp\left(-\tfrac{1}{2}\left(\boldsymbol{y}^{(\mathrm{train})}-\boldsymbol{X}^{(\mathrm{train})}\boldsymbol{w}\right)^{\top}\left(\boldsymbol{y}^{(\mathrm{train})}-\boldsymbol{X}^{(\mathrm{train})}\boldsymbol{w}\right)\right)", size=30)
        fit(e2, 5.9); e2.move_to([-0.3, 0.4, 0])
        n72 = T("(5.72)", 28).move_to([3.3, 0.4, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=2.4)
        self.play(FadeIn(n72), run_time=0.25)
        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.5, 1], x_length=5.0, y_length=1.4, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.55, 0])
        bell = ax.plot(gauss(0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.7)
        with audio.cue("slide", pan=0.3): self.play(Create(bell), run_time=1.3)
        mline = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.4), color=K, stroke_width=3)
        mlab = Mx(r"\boldsymbol{X}\boldsymbol{w}", size=28).next_to(ax.c2p(0, 0), DOWN, buff=0.1)
        with audio.cue("grow"): self.play(Create(mline), FadeIn(mlab), run_time=0.7)
        wid = DoubleArrow(ax.c2p(-1, 0.24), ax.c2p(1, 0.24), color=K, buff=0, stroke_width=3, tip_length=0.15)
        wl = T("variance one", 20).move_to(ax.c2p(2.3, 0.3))
        with audio.cue("grow"): self.play(Create(wid), FadeIn(wl), run_time=0.7)
        n1 = self.note_in(audio, "Follows the standard MSE formulation.", -3.1, 24)
        self.wait(1.4)
        return items + [n0, e1, n71, box, e2, n72, ax, bell, mline, mlab, wid, wl, n1]

    # C - notation and the idea of a prior
    def scene_c(self, audio):
        items = self.heading_in(audio, "Notation and the Prior")
        n0 = self.note_in(audio, "To reduce the notational burden, we simply write:", 2.3, 24)
        e = Mx(r"\left(\boldsymbol{X}^{(\mathrm{train})},\boldsymbol{y}^{(\mathrm{train})}\right)",
               r"\;\longrightarrow\;",
               r"(\boldsymbol{X},\boldsymbol{y})", size=36)
        fit(e, 6.2); e.move_to([0, 1.3, 0])
        with audio.cue("draw"): self.play(Write(e[0]), run_time=1.3)
        with audio.cue("slide"): self.play(Write(e[1]), run_time=0.6)
        with audio.cue("draw"): self.play(Write(e[2]), run_time=0.9)
        box = SurroundingRectangle(e[2], color=K, buff=0.12, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.5)
        r1, t1 = self.card(r"The posterior over $\boldsymbol{w}$ first needs a prior", 0.1, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"The prior reflects our naive belief about $\boldsymbol{w}$", -0.9, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        r3, t3 = self.card(r"In practice: a fairly broad distribution", -1.9, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r3), Write(t3), run_time=1.2)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.3, 1], x_length=4.4, y_length=0.8, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([-0.9, -3.0, 0])
        broad = ax.plot(gauss(0, 1.8), x_range=[-4, 4], color=K, stroke_width=6)
        lab = T("high uncertainty", 22).move_to([2.3, -2.9, 0])
        with audio.cue("draw"): self.play(Create(ax), run_time=0.5)
        with audio.cue("slide", pan=0.3): self.play(Create(broad), FadeIn(lab), run_time=1.2)
        self.wait(1.4)
        return items + [n0, e, box, r1, t1, r2, t2, r3, t3, ax, broad, lab]

    # D - Gaussian prior, eq 5.73
    def scene_d(self, audio):
        items = self.heading_in(audio, "The Gaussian Prior")
        n0 = self.note_in(audio, "For real-valued parameters, a Gaussian is a common prior:", 2.35, 22)
        e = Mx(r"p(\boldsymbol{w})", r"=", r"\mathcal{N}(\boldsymbol{w};\boldsymbol{\mu}_0,\boldsymbol{\Lambda}_0)",
               r"\propto\exp\left(-\tfrac{1}{2}(\boldsymbol{w}-\boldsymbol{\mu}_0)^{\top}\boldsymbol{\Lambda}_0^{-1}(\boldsymbol{w}-\boldsymbol{\mu}_0)\right)", size=30)
        fit(e, 5.9); e.move_to([-0.3, 1.5, 0])
        n73 = T("(5.73)", 28).move_to([3.3, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.6)
        self.play(FadeIn(n73), run_time=0.25)
        box = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        ax = Axes(x_range=[-3.5, 4.5, 1], y_range=[0, 0.5, 1], x_length=4.8, y_length=1.5, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.1, 0])
        bell = ax.plot(gauss(0.5, 1.0), x_range=[-3.5, 4.5], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=0.3): self.play(Create(bell), run_time=1.3)
        mline = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 0.4), color=K, stroke_width=3)
        mlab = Mx(r"\boldsymbol{\mu}_0", size=28).next_to(ax.c2p(0.5, 0), DOWN, buff=0.1)
        wid = DoubleArrow(ax.c2p(-0.5, 0.24), ax.c2p(1.5, 0.24), color=K, buff=0, stroke_width=3, tip_length=0.15)
        wl = Mx(r"\boldsymbol{\Lambda}_0", size=28).next_to(wid, UP, buff=0.55).shift(RIGHT * 1.7)
        with audio.cue("grow"): self.play(Create(mline), FadeIn(mlab), run_time=0.7)
        with audio.cue("grow"): self.play(Create(wid), FadeIn(wl), run_time=0.7)
        r1, t1 = self.card(r"$\boldsymbol{\mu}_0$: prior mean vector", -1.85, 22, 0.8, 3.5, -1.85)
        r2, t2 = self.card(r"$\boldsymbol{\Lambda}_0$: covariance matrix", -1.85, 22, 0.8, 3.5, 1.85)
        with audio.cue("grow", pan=-0.4): self.play(Create(r1), Write(t1), run_time=1.0)
        with audio.cue("grow", pan=0.4): self.play(Create(r2), Write(t2), run_time=1.0)
        r3, t3 = self.card(r"Typically diagonal: $\boldsymbol{\Lambda}_0=\mathrm{diag}(\boldsymbol{\lambda}_0)$", -2.95, 24, 0.8)
        with audio.cue("grow"): self.play(Create(r3), Write(t3), run_time=1.2)
        self.wait(1.4)
        return items + [n0, e, n73, box, ax, bell, mline, mlab, wid, wl, r1, t1, r2, t2, r3, t3]

    # E - posterior, eq 5.74
    def scene_e(self, audio):
        items = self.heading_in(audio, "The Posterior")
        n0 = self.note_in(audio, "With the prior specified, we determine the posterior:", 2.3, 24)
        e = Mx(r"p(\boldsymbol{w}\mid\boldsymbol{X},\boldsymbol{y})", r"\propto",
               r"p(\boldsymbol{y}\mid\boldsymbol{X},\boldsymbol{w})", r"p(\boldsymbol{w})", size=36)
        fit(e, 5.9); e.move_to([-0.3, 1.5, 0])
        n74 = T("(5.74)", 28).move_to([3.3, 1.5, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.2)
        self.play(FadeIn(n74), run_time=0.25)
        l0 = T("posterior", 20).next_to(e[0], DOWN, buff=0.2)
        l1 = T("likelihood", 20).next_to(e[2], DOWN, buff=0.2)
        l2 = T("prior", 20).next_to(e[3], DOWN, buff=0.2)
        with audio.cue("type", glyphs=26): self.play(FadeIn(l0), FadeIn(l1), FadeIn(l2), run_time=0.9)
        box = SurroundingRectangle(e[0], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.7, 1], x_length=5.4, y_length=1.9, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.75, 0])
        prior = DashedVMobject(ax.plot(gauss(0, 1.6), x_range=[-4, 4], color=K, stroke_width=5),
                               num_dashes=40, dashed_ratio=0.55)
        like = DashedVMobject(ax.plot(gauss(1.0, 0.8), x_range=[-4, 4], color=K, stroke_width=5),
                              num_dashes=70, dashed_ratio=0.3)
        post = ax.plot(gauss(0.7, 0.62), x_range=[-4, 4], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=-0.3): self.play(Create(prior), run_time=1.2)
        with audio.cue("slide", pan=0.0): self.play(Create(like), run_time=1.2)
        with audio.cue("slide", pan=0.3): self.play(Create(post), run_time=1.4)
        leg = []
        specs = [("dashed", "prior", -3.5), ("dotted", "likelihood", -1.2), ("solid", "posterior", 1.1)]
        for style, name, x0 in specs:
            ln = Line([x0, -2.45, 0], [x0 + 0.6, -2.45, 0], color=K, stroke_width=5)
            if style == "dashed": ln = DashedVMobject(ln, num_dashes=5, dashed_ratio=0.55)
            elif style == "dotted": ln = DashedVMobject(ln, num_dashes=8, dashed_ratio=0.3)
            tx = T(name, 22).next_to(ln, RIGHT, buff=0.15)
            leg += [ln, tx]
        with audio.cue("grow"): self.play(*[FadeIn(m) for m in leg], run_time=0.8)
        n1 = self.note_in(audio, "Prior times likelihood shapes the posterior over the parameters.", -3.2, 22)
        self.wait(1.4)
        return items + [n0, e, n74, l0, l1, l2, box, ax, prior, like, post] + leg + [n1]

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
    Page_135().render()
