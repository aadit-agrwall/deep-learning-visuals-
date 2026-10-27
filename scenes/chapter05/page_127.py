"""Page 127 - Variance derivation, bias-variance trade-off, MSE, capacity.

Black and white only. All text and equations use LaTeX Computer Modern,
the same typeface as the book. Square 1:1, runs longer than 60 s.

Structure:
  0-4 s    the real book page, static
  4-7 s    page text lines are smoothly drawn into a single point
  then     5 scenes, separated by a simple fade
  end      page rebuilds itself out of a point
"""

from manim import *
import numpy as np
from pathlib import Path
from PIL import Image

from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE_SRC = Path("assets/bookpage/page_127.png")
BAND_DIR = Path("assets/bookpage/page_127_bands")

WHITE_BG = "#FFFFFF"
K = "#000000"
MIN_SECONDS = 62.0


# ------------------------------------------------------------------
# animations
# ------------------------------------------------------------------

import json as _json


class CueLogger:
    def __init__(self, scene, real):
        self._s, self._r, self.log = scene, real, []

    def cue(self, name, *a, **k):
        try:
            t = float(self._s.renderer.time)
        except Exception:
            t = float(self._s.time)
        self.log.append({"t": t, "name": name,
                         "glyphs": k.get("glyphs", 0), "pan": k.get("pan", 0.0)})
        _json.dump(self.log, open("/tmp/p127_cues.json", "w"))
        return self._r.cue(name, *a, **k)

    def __getattr__(self, n):
        return getattr(self._r, n)


class Collapse(Animation):
    """Smoothly shrink + gently twist a mobject into a point.
    reverse=True plays it backwards (point -> full size)."""

    def __init__(self, mobject, point, spin=0.0, reverse=False, **kwargs):
        self.point = np.array(point, dtype=float)
        self.spin = spin
        self.reverse = reverse
        self.cur_s = 1.0
        self.cur_a = 0.0
        super().__init__(mobject, **kwargs)
        if reverse:
            self._apply(1.0)

    def _apply(self, t):
        s = max(1 - 0.985 * t, 1e-3)
        a = self.spin * t
        self.mobject.scale(s / self.cur_s, about_point=self.point)
        self.mobject.rotate(a - self.cur_a, about_point=self.point)
        self.cur_s, self.cur_a = s, a

    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha)
        self._apply(1 - t if self.reverse else t)


class ZoomPulse(Animation):
    def __init__(self, mobject, point, s0, s1, **kwargs):
        self.point = np.array(point, dtype=float)
        self.s0, self.s1, self.cur = s0, s1, 1.0
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha)
        s = max(self.s0 + (self.s1 - self.s0) * t, 1e-3)
        self.mobject.scale(s / self.cur, about_point=self.point)
        self.cur = s


# ------------------------------------------------------------------
# page strips
# ------------------------------------------------------------------
def build_bands():
    if not PAGE_SRC.exists():
        raise FileNotFoundError(f"Missing page image: {PAGE_SRC}")
    image = Image.open(PAGE_SRC).convert("RGB")
    w, h = image.size
    image = image.crop((6, 6, w - 6, h - 6))
    w, h = image.size
    arr = np.asarray(image)
    ink = (arr[:, 14:-14].min(axis=2) < 235).any(axis=1)
    ink[:3] = False
    ink[-6:] = False
    BAND_DIR.mkdir(parents=True, exist_ok=True)
    for old in BAND_DIR.glob("band_*.png"):
        old.unlink()
    bands, y = [], 0
    while y < h:
        if not ink[y]:
            y += 1
            continue
        s = y
        while y < h and ink[y]:
            y += 1
        top, bottom = max(0, s - 2), min(h, y + 2)
        p = BAND_DIR / f"band_{len(bands):03d}.png"
        image.crop((0, top, w, bottom)).save(p)
        bands.append((str(p), top, bottom))
    if not bands:
        raise ValueError("No text strips detected in page_127.png")
    print(f"Detected {len(bands)} strips")
    return w, h, bands


# ------------------------------------------------------------------
# text helpers (LaTeX Computer Modern = book typeface)
# ------------------------------------------------------------------
def fit(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def T(text, size=30, bold=False):
    s = r"\textbf{" + text + "}" if bold else text
    return Tex(s, color=K, font_size=size)


def Mx(*parts, size=40):
    return MathTex(*parts, color=K, font_size=size)


class Page_127(Chapter5Scene):
    PAGE_NO = "127"

    # ------------------------------------------------------------
    def make_page(self, width, height, bands):
        aspect = width / height
        ph = min(config.frame_height - 1.3, (config.frame_width - 0.4) / aspect)
        pw = ph * aspect
        sc = pw / width
        c = np.array([0.0, 0.1, 0.0])
        paper = Rectangle(width=pw, height=ph, stroke_width=0,
                          fill_color=WHITE_BG, fill_opacity=1).move_to(c)
        paper.set_z_index(0)
        top = c[1] + ph / 2
        strips = []
        for path, t, b in bands:
            s = ImageMobject(path)
            s.scale_to_fit_width(pw)
            s.move_to([c[0], top - ((t + b) / 2) * sc, 0])
            s.set_z_index(1)
            strips.append(s)
        return paper, strips

    def page_motion(self, paper, strips, point, reverse=False, run=2.0):
        """Smooth, coherent swirl: every line twists the same way, outer lines
        lead on the way in, inner lines lead on the way out."""
        pt = np.array(point, dtype=float)
        order = sorted(strips, key=lambda s: np.linalg.norm(s.get_center() - pt),
                       reverse=not reverse)
        spin = PI * 0.5
        anims = [Collapse(s, pt, spin, reverse=reverse, rate_func=smooth,
                          remover=not reverse, run_time=run) for s in order]
        group = LaggedStart(*anims, lag_ratio=0.03)
        paper_anim = Collapse(paper, pt, spin, reverse=reverse, rate_func=smooth,
                              remover=not reverse, run_time=run * 1.6)
        return AnimationGroup(group, paper_anim)

    # ------------------------------------------------------------
    def next_scene(self, audio, items):
        items = [i for i in items if i is not None]
        with audio.cue("wipe"):
            self.play(*[FadeOut(i) for i in items], run_time=0.7)
        self.wait(0.2)

    def heading_in(self, audio, text):
        h = T(text, 40, True)
        fit(h, 7.6)
        h.to_edge(UP, buff=0.5)
        with audio.cue("type", glyphs=len(text)):
            self.play(Write(h), run_time=1.2)
        u = Line(h.get_left(), h.get_right(), color=K, stroke_width=4)
        u.next_to(h, DOWN, buff=0.12)
        with audio.cue("draw"):
            self.play(Create(u), run_time=0.5)
        return [h, u]

    def note_in(self, audio, text, y, size=30):
        n = T(text, size)
        fit(n, 7.4)
        n.move_to([0, y, 0])
        with audio.cue("type", glyphs=len(text)):
            self.play(Write(n), run_time=1.3)
        return n

    def label_axes(self, ax):
        for a in (ax.x_axis, ax.y_axis):
            a.set_color(K)

    # ------------------------------------------------------------
    # SCENE A - variance derivation (5.49 - 5.52)
    # ------------------------------------------------------------
    def scene_variance(self, audio):
        items = self.heading_in(audio, "Variance of the Estimator")

        l0 = Mx(r"\mathrm{Var}(\hat\theta_m)", "=",
                r"\mathrm{Var}\!\left(\frac{1}{m}\sum_{i=1}^{m}x^{(i)}\right)", size=36)
        fit(l0, 5.6)
        l0.move_to([-0.5, 2.1, 0])
        with audio.cue("draw"):
            self.play(Write(l0), run_time=1.4)
        items.append(l0)

        rows = [
            (r"=\frac{1}{m^2}\sum_{i=1}^{m}\mathrm{Var}\!\left(x^{(i)}\right)", "(5.49)", 1.0),
            (r"=\frac{1}{m^2}\sum_{i=1}^{m}\theta(1-\theta)", "(5.50)", -0.05),
            (r"=\frac{1}{m^2}\,m\,\theta(1-\theta)", "(5.51)", -1.0),
            (r"=\frac{1}{m}\,\theta(1-\theta)", "(5.52)", -1.9),
        ]
        last = None
        for tex, num, y in rows:
            r = Mx(tex, size=36)
            r.align_to(l0[1], LEFT)
            r.set_y(y)
            lab = T(num, 28).move_to([3.3, y, 0])
            with audio.cue("draw"):
                self.play(Write(r), run_time=1.1)
            self.play(FadeIn(lab), run_time=0.25)
            self.wait(0.35)
            items += [r, lab]
            last = r

        box = SurroundingRectangle(last, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"):
            self.play(Create(box), run_time=0.7)
        items.append(box)

        n = self.note_in(audio, r"The variance decreases as a function of $m$.", -3.1)
        items.append(n)
        self.wait(1.5)
        return items

    # ------------------------------------------------------------
    # SCENE B - variance shrinks as m grows
    # ------------------------------------------------------------
    def scene_shrink(self, audio):
        items = self.heading_in(audio, "More Examples, Less Variance")

        eq = Mx(r"\mathrm{Var}(\hat\theta_m)", "=",
                r"\frac{\theta(1-\theta)}{m}", size=40)
        fit(eq, 6.0)
        eq.move_to([0, 2.05, 0])
        with audio.cue("draw"):
            self.play(Write(eq), run_time=1.3)
        items.append(eq)

        ax = Axes(x_range=[0, 16, 4], y_range=[0, 0.27, 0.1], x_length=5.8, y_length=2.6,
                  tips=False,
                  axis_config={"color": K, "stroke_width": 2, "include_ticks": False}
                  ).move_to([0, -0.55, 0])
        curve = ax.plot(lambda x: 0.25 / x, x_range=[1, 16], color=K, stroke_width=6)
        xl = Mx("m", size=34).next_to(ax.x_axis.get_end(), DOWN, buff=0.25)
        yl = Mx(r"\mathrm{Var}", size=30).next_to(ax.y_axis.get_end(), LEFT, buff=0.15)
        with audio.cue("draw"):
            self.play(Create(ax), Write(xl), Write(yl), run_time=1.1)
        with audio.cue("slide", profile="transfer"):
            self.play(Create(curve), run_time=1.6)
        items += [ax, curve, xl, yl]

        for m in [1, 2, 4, 8, 16]:
            p = ax.c2p(m, 0.25 / m)
            d = Dot(p, radius=0.08, color=K)
            drop = Line(ax.c2p(m, 0), p, color=K, stroke_width=2)
            tick = T(str(m), 24).next_to(ax.c2p(m, 0), DOWN, buff=0.12)
            with audio.cue("grow"):
                self.play(Create(drop), GrowFromCenter(d), FadeIn(tick), run_time=0.55)
            items += [d, drop, tick]

        n = self.note_in(audio, "More examples in the dataset give lower estimator variance.", -3.25, 28)
        items.append(n)
        self.wait(1.5)
        return items

    # ------------------------------------------------------------
    # SCENE C - 5.4.4 trade-off text
    # ------------------------------------------------------------
    def scene_tradeoff(self, audio):
        items = self.heading_in(audio, "Trading Off Bias and Variance")

        def card(text, y):
            r = RoundedRectangle(width=7.0, height=0.95, corner_radius=0.2,
                                 stroke_color=K, stroke_width=3, fill_opacity=0
                                 ).move_to([0, y, 0])
            t = Tex(text, color=K, font_size=32)
            fit(t, 6.5)
            t.move_to(r)
            return r, t

        r1, t1 = card(r"\textbf{Bias}: expected deviation from the true value", 1.85)
        with audio.cue("grow", pan=-0.3):
            self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = card(r"\textbf{Variance}: deviation caused by a particular sample", 0.65)
        with audio.cue("grow", pan=0.3):
            self.play(Create(r2), Write(t2), run_time=1.3)
        items += [r1, t1, r2, t2]
        self.wait(0.4)

        q1 = self.note_in(audio, "One estimator has more bias, the other more variance.", -0.7, 28)
        q2 = self.note_in(audio, r"\textbf{How do we choose between them?}", -1.3, 32)
        a1 = self.note_in(audio, r"Most common: \textbf{cross-validation}", -2.2, 32)
        a2 = self.note_in(audio, r"Alternative: compare the \textbf{mean squared error} (MSE)", -2.85, 30)
        items += [q1, q2, a1, a2]
        self.wait(1.5)
        return items

    # ------------------------------------------------------------
    # SCENE D - MSE (5.53, 5.54)
    # ------------------------------------------------------------
    def scene_mse(self, audio):
        items = self.heading_in(audio, "Mean Squared Error")

        l1 = Mx(r"\mathrm{MSE}", "=",
                r"\mathbb{E}\!\left[(\hat\theta_m-\theta)^2\right]", size=42)
        fit(l1, 5.8)
        l1.move_to([-0.2, 1.7, 0])
        with audio.cue("draw"):
            self.play(Write(l1), run_time=1.4)
        n1 = T("(5.53)", 28).move_to([3.3, 1.7, 0])
        self.play(FadeIn(n1), run_time=0.25)

        l2 = Mx("=", r"\mathrm{Bias}(\hat\theta_m)^2+\mathrm{Var}(\hat\theta_m)", size=42)
        l2.align_to(l1[1], LEFT)
        l2.set_y(0.45)
        with audio.cue("draw"):
            self.play(Write(l2), run_time=1.4)
        n2 = T("(5.54)", 28).move_to([3.3, 0.45, 0])
        self.play(FadeIn(n2), run_time=0.25)
        items += [l1, n1, l2, n2]

        box = SurroundingRectangle(l2[1], color=K, buff=0.16, stroke_width=4)
        with audio.cue("grow"):
            self.play(Create(box), run_time=0.7)
        items.append(box)
        self.wait(0.4)

        lines = [
            (r"MSE measures the overall expected deviation", -1.05),
            (r"between the estimator and the true value of $\theta$.", -1.6),
            (r"Desirable estimators have \textbf{small MSE}:", -2.35),
            (r"both bias and variance are kept in check.", -2.9),
        ]
        for text, y in lines:
            items.append(self.note_in(audio, text, y, 30))
        self.wait(1.5)
        return items

    # ------------------------------------------------------------
    # SCENE E - capacity, underfitting, overfitting
    # ------------------------------------------------------------
    def scene_capacity(self, audio):
        items = self.heading_in(audio, "Capacity, Underfitting, Overfitting")

        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1.1, 1], x_length=6.0, y_length=3.2,
                  tips=False,
                  axis_config={"color": K, "stroke_width": 2, "include_ticks": False}
                  ).move_to([0, 0.2, 0])
        bias = DashedVMobject(
            ax.plot(lambda x: (1 - x) ** 2, x_range=[0, 1], color=K, stroke_width=5),
            num_dashes=36, dashed_ratio=0.55)
        var = DashedVMobject(
            ax.plot(lambda x: x ** 2, x_range=[0, 1], color=K, stroke_width=5),
            num_dashes=70, dashed_ratio=0.25)
        mse_f = lambda x: (1 - x) ** 2 + x ** 2
        mse = ax.plot(mse_f, x_range=[0, 1], color=K, stroke_width=7)

        bl = T(r"Bias$^2$", 26).move_to(ax.c2p(0.3, 0.92))
        vl = T("Variance", 26).move_to(ax.c2p(0.72, 0.92))
        ml = T("MSE", 26, True).move_to(ax.c2p(0.5, 0.78))
        ul = T("Underfitting", 26).next_to(ax.c2p(0.13, 0), DOWN, buff=0.2)
        ol = T("Overfitting", 26).next_to(ax.c2p(0.87, 0), DOWN, buff=0.2)
        cl = T(r"Capacity $\rightarrow$", 26).next_to(ax.c2p(0.5, 0), DOWN, buff=0.2)

        with audio.cue("draw"):
            self.play(Create(ax), run_time=1.0)
        with audio.cue("slide", pan=-0.4):
            self.play(Create(bias), FadeIn(bl), FadeIn(ul), run_time=1.3)
        with audio.cue("slide", pan=0.4):
            self.play(Create(var), FadeIn(vl), FadeIn(ol), run_time=1.3)
        with audio.cue("slide", profile="transfer"):
            self.play(Create(mse), FadeIn(ml), FadeIn(cl), run_time=1.4)

        best = ax.c2p(0.5, mse_f(0.5))
        guide = DashedLine(ax.c2p(0.5, 0), best, color=K, stroke_width=3)
        dot = Dot(best, radius=0.11, color=K).set_z_index(5)
        with audio.cue("grow"):
            self.play(Create(guide), GrowFromCenter(dot), run_time=0.7)
        self.play(Flash(best, color=K, flash_radius=0.6, line_length=0.25, run_time=0.7))

        n = self.note_in(audio, "Bias falls and variance rises as capacity grows.", -3.2, 28)
        self.wait(1.6)
        return items + [ax, bias, var, mse, bl, vl, ml, ul, ol, cl, guide, dot, n]

    # ------------------------------------------------------------
    def construct(self):
        self.camera.background_color = WHITE_BG
        config.background_color = WHITE_BG
        audio = CueLogger(self, ASMRSync(self, self.PAGE_NO))
        w, h, bands = build_bands()

        # ---- 0-4 s: the book page ----
        paper, strips = self.make_page(w, h, bands)
        pc = paper.get_center()
        with audio.cue("grow"):
            self.play(FadeIn(paper), *[FadeIn(s) for s in strips], run_time=0.6)
        self.wait(3.4)

        # ---- page text is smoothly drawn into a point ----
        with audio.cue("zoom"):
            self.play(self.page_motion(paper, strips, pc, reverse=False, run=2.0))
        dot = Dot(pc, radius=0.07, color=K)
        with audio.cue("grow"):
            self.play(GrowFromCenter(dot), run_time=0.3)
        with audio.cue("zoom"):
            self.play(Flash(pc, color=K, flash_radius=0.8, line_length=0.3, run_time=0.7),
                      FadeOut(dot, scale=4), run_time=0.7)

        # ---- scenes, separated by a simple fade ----
        for scene in (self.scene_variance, self.scene_shrink, self.scene_tradeoff,
                      self.scene_mse, self.scene_capacity):
            items = scene(audio)
            self.next_scene(audio, items)

        # ---- page rebuilds from a point ----
        paper2, strips2 = self.make_page(w, h, bands)
        pc2 = paper2.get_center()
        self.add(paper2, *strips2)
        with audio.cue("zoom"):
            self.play(self.page_motion(paper2, strips2, pc2, reverse=True, run=2.0))
        self.wait(0.8)
        allm = [paper2, *strips2]
        with audio.cue("zoom"):
            self.play(*[ZoomPulse(m, pc2, 1.0, 1.04, run_time=1.2, rate_func=smooth) for m in allm])
            self.play(*[ZoomPulse(m, pc2, 1.0, 1 / 1.04, run_time=1.2, rate_func=smooth) for m in allm])
        self.wait(1.5)

        # ---- guarantee > 60 s ----
        try:
            now = self.renderer.time
        except Exception:
            now = self.time
        if now < MIN_SECONDS:
            self.wait(MIN_SECONDS - now + 0.2)
        audio.finish()


if __name__ == "__main__":
    Page_127().render()
