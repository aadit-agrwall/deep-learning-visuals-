from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "132"
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


class Page_132(Chapter5Scene):
    PAGE_NO = "132"

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

    # A - equation 5.66
    def scene_a(self, audio):
        items = self.heading_in(audio, "Log-Likelihood versus MSE")
        n0 = self.note_in(audio, r"$\hat y^{(i)}$ is the linear regression output on input $\boldsymbol{x}^{(i)}$.", 2.25, 24)
        n1 = self.note_in(audio, "Compare the log-likelihood with the mean squared error:", 1.6, 26)
        eq = Mx(r"\mathrm{MSE}_{\mathrm{train}}=\frac{1}{m}\sum_{i=1}^{m}\left\|\hat y^{(i)}-y^{(i)}\right\|^2", size=40)
        fit(eq, 5.7); eq.move_to([-0.35, 0.2, 0])
        n66 = T("(5.66)", 28).move_to([3.3, 0.2, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.8)
        self.play(FadeIn(n66), run_time=0.25)
        box = SurroundingRectangle(eq, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        r, t = self.card(r"Log-likelihood term: $\sum_i \left\|\hat y^{(i)}-y^{(i)}\right\|^2$", -1.4, 26, 0.95)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.3)
        n2 = self.note_in(audio, "The same squared-error sum appears in both.", -2.7, 28)
        self.wait(1.5)
        return items + [n0, n1, eq, n66, box, r, t, n2]

    # B - same optimum, different values
    def scene_b(self, audio):
        items = self.heading_in(audio, "Same Optimum, Different Values")
        n0 = self.note_in(audio, r"Maximizing the log-likelihood over $\boldsymbol{w}$", 2.3, 28)
        n1 = self.note_in(audio, "gives the same estimate as minimizing the MSE.", 1.7, 28)
        ax = Axes(x_range=[0, 2, 1], y_range=[0, 1, 1], x_length=5.6, y_length=2.6, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.5, 0])
        nll = ax.plot(lambda x: 0.45 * (x - 1) ** 2 + 0.3, x_range=[0, 2], color=K, stroke_width=7)
        mse = DashedVMobject(ax.plot(lambda x: 0.7 * (x - 1) ** 2 + 0.1, x_range=[0, 2], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        with audio.cue("draw"): self.play(Create(ax), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Create(nll), run_time=1.4)
        with audio.cue("slide", pan=0.3): self.play(Create(mse), run_time=1.4)
        l1 = T(r"$-$log-likelihood (solid)", 22).move_to(ax.c2p(1.55, 0.92))
        l2 = T("MSE (dashed)", 22).move_to(ax.c2p(0.45, 0.92))
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        vline = DashedLine(ax.c2p(1, 0), ax.c2p(1, 0.95), color=K, stroke_width=3)
        d1 = Dot(ax.c2p(1, 0.3), radius=0.1, color=K).set_z_index(5)
        d2 = Dot(ax.c2p(1, 0.1), radius=0.1, color=K).set_z_index(5)
        wl = Mx(r"\boldsymbol{w}", size=34).next_to(ax.c2p(1, 0), DOWN, buff=0.15)
        with audio.cue("grow"): self.play(Create(vline), GrowFromCenter(d1), GrowFromCenter(d2), Write(wl), run_time=0.9)
        self.play(Flash(ax.c2p(1, 0.1), color=K, flash_radius=0.5, line_length=0.2, run_time=0.6))
        n2 = self.note_in(audio, "Different values, but the same location of the optimum.", -3.15, 26)
        self.wait(1.5)
        return items + [n0, n1, ax, nll, mse, l1, l2, vline, d1, d2, wl, n2]

    # C - properties, consistency
    def scene_c(self, audio):
        items = self.heading_in(audio, "5.5.2 Properties of ML")
        n0 = self.note_in(audio, "The best estimator asymptotically, as $m\\to\\infty$,", 2.3, 28)
        n1 = self.note_in(audio, "in terms of its rate of convergence.", 1.7, 28)
        r, t = self.card(r"\textbf{Consistency}: the estimate converges to the true $\theta$", 0.6, 26, 0.95)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.3)

        ax = Axes(x_range=[0, 60, 10], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.0, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.5, 0])
        truth = DashedLine(ax.c2p(0, 0.6), ax.c2p(60, 0.6), color=K, stroke_width=4)
        tl = Mx(r"\theta", size=36).next_to(ax.c2p(60, 0.6), RIGHT, buff=0.12)
        xl = Mx("m", size=32).next_to(ax.c2p(60, 0), DOWN, buff=0.12)
        with audio.cue("draw"): self.play(Create(ax), Create(truth), Write(tl), Write(xl), run_time=1.1)
        rng = np.random.default_rng(132)
        dots = VGroup()
        for m in range(1, 61):
            est = float(np.clip(0.6 + rng.normal(0, 0.4 / np.sqrt(m)), 0.04, 0.97))
            dots.add(Dot(ax.c2p(m, est), radius=0.05, color=K))
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.03), run_time=2.4)
        n2 = self.note_in(audio, "Under appropriate conditions, as follows:", -3.0, 28)
        self.wait(1.4)
        return items + [n0, n1, r, t, ax, truth, tl, xl, dots, n2]

    # D - the two conditions
    def scene_d(self, audio):
        items = self.heading_in(audio, "Conditions for Consistency")
        r1, t1 = self.card(r"1. $p_{\mathrm{data}}$ lies within the model family", 2.0, 26, 0.9)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        fam = Circle(radius=0.75, color=K, stroke_width=4).move_to([-1.6, 0.6, 0])
        fl = Mx(r"p_{\mathrm{model}}(\cdot;\boldsymbol{\theta})", size=26).next_to(fam, UP, buff=0.1)
        pd = Dot([-1.6, 0.6, 0], radius=0.1, color=K)
        pdl = Mx(r"p_{\mathrm{data}}", size=26).next_to(pd, DOWN, buff=0.12)
        out = Dot([1.9, 0.6, 0], radius=0.1, color=K)
        outl = Mx(r"p_{\mathrm{data}}", size=26).next_to(out, DOWN, buff=0.12)
        cross = Tex(r"$\times$", color=K, font_size=60).next_to(out, UP, buff=0.1)
        with audio.cue("draw"): self.play(Create(fam), Write(fl), run_time=1.0)
        with audio.cue("grow"): self.play(GrowFromCenter(pd), Write(pdl), run_time=0.7)
        with audio.cue("grow", pan=0.3): self.play(GrowFromCenter(out), Write(outl), Write(cross), run_time=0.9)

        r2, t2 = self.card(r"2. $p_{\mathrm{data}}$ matches exactly one $\boldsymbol{\theta}$", -0.9, 26, 0.9)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        th1 = Mx(r"\boldsymbol{\theta}_1", size=30).move_to([-2.4, -2.0, 0])
        th2 = Mx(r"\boldsymbol{\theta}_2", size=30).move_to([-2.4, -2.9, 0])
        tgt = Mx(r"p_{\mathrm{data}}", size=30).move_to([1.2, -2.45, 0])
        a1 = Arrow(th1.get_right(), tgt.get_left() + UP * 0.1, color=K, buff=0.12, stroke_width=4)
        a2 = Arrow(th2.get_right(), tgt.get_left() + DOWN * 0.1, color=K, buff=0.12, stroke_width=4)
        with audio.cue("slide", pan=-0.3): self.play(Write(th1), Write(th2), Write(tgt), run_time=0.9)
        with audio.cue("slide", pan=0.3): self.play(GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        xl = Tex(r"ambiguous $\boldsymbol{\theta}$", color=K, font_size=26).next_to(tgt, RIGHT, buff=0.25)
        with audio.cue("type", glyphs=14): self.play(Write(xl), run_time=0.8)
        self.wait(1.5)
        return items + [r1, t1, fam, fl, pd, pdl, out, outl, cross, r2, t2, th1, th2, tgt, a1, a2, xl]

    # E - statistical efficiency
    def scene_e(self, audio):
        items = self.heading_in(audio, "Statistical Efficiency")
        r, t = self.card(r"Consistent estimators can differ in \textbf{efficiency}", 2.1, 26, 0.9)
        with audio.cue("grow"): self.play(Create(r), Write(t), run_time=1.3)
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.2, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, 0.35, 0])
        eff = ax.plot(lambda x: 0.9 / x, x_range=[1.0, 20], color=K, stroke_width=7)
        oth = DashedVMobject(ax.plot(lambda x: 1.9 / (x + 0.9), x_range=[1.0, 20], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        xl = Mx("m", size=32).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
        yl = T("error", 24).next_to(ax.y_axis.get_end(), LEFT, buff=0.1)
        with audio.cue("draw"): self.play(Create(ax), Write(xl), Write(yl), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Create(oth), run_time=1.3)
        with audio.cue("slide", pan=0.3): self.play(Create(eff), run_time=1.3)
        l1 = T("more efficient", 22).move_to(ax.c2p(9.5, 0.12))
        l2 = T("less efficient (dashed)", 22).move_to(ax.c2p(12.5, 0.45))
        with audio.cue("grow"): self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        n1 = self.note_in(audio, "Lower error for a fixed number of samples $m$.", -1.2, 26)
        n2 = self.note_in(audio, "Studied in the parametric case, e.g. linear regression:", -1.85, 24)
        eq = Mx(r"\mathbb{E}\left[\left(\hat\theta_m-\theta\right)^2\right]", size=40).move_to([0, -2.75, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.4)
        box = SurroundingRectangle(eq, color=K, buff=0.16, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        self.wait(1.5)
        return items + [r, t, ax, eff, oth, xl, yl, l1, l2, n1, n2, eq, box]

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
    Page_132().render()
