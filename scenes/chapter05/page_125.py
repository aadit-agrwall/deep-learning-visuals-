"""Page 125 - unbiased sample variance (5.40-5.44), variance and standard error
(5.45). The book page opens the video, its text zooms OUT and away, the animation
plays, and the text zooms back IN at the end. Sound: ASMRSync cues only."""

from manim import *
import numpy as np
from pathlib import Path
from PIL import Image

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.asmr_sync import ASMRSync

PAGE_SRC = Path("assets/bookpage/page_125.png")
BAND_DIR = Path("assets/bookpage/page_125_bands")


def shrink(mob, width):
    """Only ever shrink a mobject to fit; never enlarge it."""
    if mob.width > width:
        mob.scale(width / mob.width)
    return mob


class ZoomFade(Animation):
    """Scale a mobject about a point while fading it (images or shapes).
    s0 -> s1 is the scale change, a0 -> a1 the opacity change (None = leave alone)."""

    def __init__(self, mobject, point, s0, s1, a0=None, a1=None, **kwargs):
        self.point = np.array(point, dtype=float)
        self.s0, self.s1, self.a0, self.a1 = s0, s1, a0, a1
        self.cur = 1.0
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha)
        s = max(self.s0 + (self.s1 - self.s0) * t, 1e-3)
        self.mobject.scale(s / self.cur, about_point=self.point)
        self.cur = s
        if self.a0 is not None:
            a = self.a0 + (self.a1 - self.a0) * t
            self.mobject.fade(1 - max(0.0, min(1.0, a)))


def build_bands():
    """Cut the book page into text-line strips (opaque, on white)."""
    if not PAGE_SRC.exists():
        raise FileNotFoundError(f"Missing {PAGE_SRC}. Copy the page 125 image there first.")
    im = Image.open(PAGE_SRC).convert("RGB")
    w, h = im.size
    im = im.crop((6, 6, w - 6, h - 6))
    w, h = im.size
    arr = np.asarray(im)
    ink = (arr[:, 14:-14].min(axis=2) < 235).any(axis=1)
    ink[:3] = False
    ink[-6:] = False
    BAND_DIR.mkdir(parents=True, exist_ok=True)
    for old in BAND_DIR.glob("band_*.png"):
        old.unlink()
    bands = []
    y = 0
    while y < h:
        if not ink[y]:
            y += 1
            continue
        y0 = y
        while y < h and ink[y]:
            y += 1
        a, b = max(0, y0 - 2), min(h, y + 2)
        path = BAND_DIR / f"band_{len(bands):02d}.png"
        im.crop((0, a, w, b)).save(path)
        bands.append((str(path), a, b))
    return w, h, bands


class Page_125(Chapter5Scene):
    PAGE_NO = "125"
    RNG_SEED = 125

    def make_page(self, w, h, bands):
        aspect = w / h
        PH = min(config.frame_height - 1.3, (config.frame_width - 0.4) / aspect)
        PW = PH * aspect
        s = PW / w
        center = np.array([0.0, 0.1, 0.0])
        paper = Rectangle(width=PW, height=PH, stroke_width=0, fill_color=WHITE, fill_opacity=1)
        paper.move_to(center).set_z_index(0)
        top = center[1] + PH / 2
        imgs = []
        for path, a, b in bands:
            m = ImageMobject(path)
            m.scale_to_fit_width(PW)
            m.move_to([center[0], top - (a + b) / 2 * s, 0])
            m.set_z_index(1)
            imgs.append(m)
        return paper, imgs

    def zoom_out_text(self, bands, center):
        return LaggedStart(*[ZoomFade(b, center, 1.0, 0.12, 1.0, 0.0,
                                      rate_func=rush_into, remover=True, run_time=1.2)
                             for b in bands], lag_ratio=0.04)

    def zoom_in_text(self, bands, center):
        return LaggedStart(*[ZoomFade(b, center, 0.12, 1.0, 0.0, 1.0,
                                      rate_func=smooth, run_time=1.4)
                             for b in bands], lag_ratio=0.04)

    def eq_rows(self, audio, specs, ys, width=6.4, run=1.8):
        objs = []
        for (tex, tag, size, col), y in zip(specs, ys):
            f = self.formula(tex, size, col)
            shrink(f, width)
            f.move_to([-0.3, y, 0])
            parts = [f]
            if tag:
                parts.append(self.txt(tag, 22, pal.TEXT_DIM).move_to([3.5, y, 0]))
            g = VGroup(*parts)
            objs.append(g)
            with audio.cue("draw"):
                self.play(Write(f), *[FadeIn(p) for p in parts[1:]], run_time=run)
        return objs

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)
        w, h, band_info = build_bands()

        # 0. The book page opens; its text zooms out and away. (~9 s)
        paper, bands = self.make_page(w, h, band_info)
        pc = paper.get_center()
        with audio.cue("grow"):
            self.play(FadeIn(paper), *[FadeIn(b) for b in bands], run_time=1.4)
        self.wait(1.6)
        with audio.cue("wipe"):
            self.play(self.zoom_out_text(bands, pc))
        self.wait(0.4)
        with audio.cue("wipe"):
            self.dust_wipe([paper], run_time=2.4)

        # 1. Unbiased sample variance (5.40). (~14 s)
        title1 = self.txt("Unbiased sample variance", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        eq1 = self.formula(r"\tilde{\sigma}_m^2=\frac{1}{m-1}\sum_{i=1}^{m}\left(x^{(i)}-\hat{\mu}_m\right)^2",
                           36, pal.FORMULA)
        self.fit_width(eq1, 6.8)
        eq1.move_to(UP * 2.5)
        num1 = self.txt("(5.40)", 22, pal.TEXT_DIM).next_to(eq1, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq1), FadeIn(num1), run_time=2.0)
        cardA = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.18,
                                 color=pal.ERROR).move_to(LEFT * 2.0 + UP * 0.3)
        fa = self.formula(r"\frac{1}{m}", 38, pal.ERROR).move_to(cardA.get_center() + UP * 0.28)
        ta = shrink(self.txt("sample variance", 22, pal.ERROR), 3.0).move_to(cardA.get_center() + DOWN * 0.5)
        cardB = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.18,
                                 color=pal.OUTPUT).move_to(RIGHT * 2.0 + UP * 0.3)
        fb = self.formula(r"\frac{1}{m-1}", 38, pal.OUTPUT).move_to(cardB.get_center() + UP * 0.28)
        tb = shrink(self.txt("unbiased version", 22, pal.OUTPUT), 3.0).move_to(cardB.get_center() + DOWN * 0.5)
        with audio.cue("grow", pan=-0.4):
            self.play(GrowFromCenter(cardA), Write(fa), FadeIn(ta), run_time=1.4, rate_func=smooth)
        with audio.cue("grow", pan=0.4):
            self.play(GrowFromCenter(cardB), Write(fb), FadeIn(tb), run_time=1.4, rate_func=smooth)
        arr1 = Arrow(cardA.get_right(), cardB.get_left(), buff=0.1, color=pal.FORMULA, stroke_width=4)
        with audio.cue("slide", profile="transfer"):
            self.play(GrowArrow(arr1), run_time=1.0)
        res1 = self.formula(r"\mathbb{E}[\tilde{\sigma}_m^2]=\sigma^2", 38, pal.OUTPUT).move_to(DOWN * 1.2)
        with audio.cue("draw"):
            self.play(Write(res1), run_time=1.4)
        note1 = self.txt("Divide by m minus 1 instead of m.\nThis estimator is unbiased.", 26, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title1, eq1, num1, cardA, fa, ta, cardB, fb, tb, arr1, res1, note1], run_time=2.4)

        # 2. Take the expectation (5.41-5.42). (~13 s)
        title2 = self.txt("Taking the expectation", 31, pal.TEXT, BOLD)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        objs2 = self.eq_rows(audio, [
            (r"\mathbb{E}[\tilde{\sigma}_m^2]=\mathbb{E}\left[\frac{1}{m-1}\sum_{i=1}^{m}\left(x^{(i)}-\hat{\mu}_m\right)^2\right]",
             "(5.41)", 28, pal.FORMULA),
            (r"=\frac{m}{m-1}\mathbb{E}[\hat{\sigma}_m^2]", "(5.42)", 38, pal.FORMULA),
        ], [1.8, 0.1], width=6.5, run=2.2)
        box2 = SurroundingRectangle(objs2[1][0], color=pal.OUTPUT, buff=0.18)
        with audio.cue("settle"):
            self.play(Create(box2), run_time=0.8)
        note2 = self.txt("The factor m over m minus 1 comes out front.\nWhat remains is the biased sample variance.", 25, pal.TEXT)
        self.fit_width(note2, 7.7)
        note2.move_to(DOWN * 2.3)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=2.0)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title2, *objs2, box2, note2], run_time=2.4)

        # 3. The factors cancel (5.43-5.44). (~16 s)
        title3 = self.txt("The factors cancel", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        objs3 = self.eq_rows(audio, [
            (r"=\frac{m}{m-1}\left(\frac{m-1}{m}\sigma^2\right)", "(5.43)", 36, pal.FORMULA),
            (r"=\sigma^2", "(5.44)", 40, pal.OUTPUT),
        ], [2.4, 1.4], run=1.8)
        box3 = SurroundingRectangle(objs3[1][0], color=pal.OUTPUT, buff=0.18)
        with audio.cue("settle"):
            self.play(Create(box3), run_time=0.8)
        H = 1.6
        base_y = -1.5
        floor3 = Line(LEFT * 3.2, RIGHT * 3.2, color=pal.TEXT_DIM, stroke_width=2).move_to([0, base_y, 0])
        true_bar = Rectangle(width=1.5, height=H, color=pal.OUTPUT, fill_color=pal.OUTPUT,
                             fill_opacity=0.3).move_to([-1.7, base_y + H / 2, 0])
        tlab = self.formula(r"\sigma^2", 30, pal.OUTPUT).move_to([-1.7, base_y + H + 0.35, 0])
        eh = H * 3 / 4
        est_bar = Rectangle(width=1.5, height=eh, color=pal.ERROR, fill_color=pal.ERROR,
                            fill_opacity=0.3).move_to([1.7, base_y + eh / 2, 0])
        elab = self.formula(r"\mathbb{E}[\hat{\sigma}_m^2]", 28, pal.ERROR).move_to([1.7, base_y + eh + 0.35, 0])
        with audio.cue("grow", pan=-0.3):
            self.play(Create(floor3), GrowFromEdge(true_bar, DOWN), FadeIn(tlab),
                      run_time=1.4, rate_func=smooth)
        with audio.cue("grow", pan=0.3):
            self.play(GrowFromEdge(est_bar, DOWN), FadeIn(elab), run_time=1.4, rate_func=smooth)
        new_bar = Rectangle(width=1.5, height=H, color=pal.OUTPUT, fill_color=pal.OUTPUT,
                            fill_opacity=0.3).move_to([1.7, base_y + H / 2, 0])
        new_lab = self.formula(r"\mathbb{E}[\tilde{\sigma}_m^2]", 28, pal.OUTPUT).move_to([1.7, base_y + H + 0.35, 0])
        fac = self.formula(r"\times\frac{m}{m-1}", 30, pal.FORMULA).move_to([0, base_y + H * 0.45, 0])
        with audio.cue("slide", profile="converge"):
            self.play(FadeIn(fac), Transform(est_bar, new_bar), Transform(elab, new_lab),
                      run_time=2.2, rate_func=smooth)
        note3 = self.txt("Multiplying by m over m minus 1 lifts\nthe expectation to exactly sigma squared.", 25, pal.TEXT)
        self.fit_width(note3, 7.7)
        note3.move_to(DOWN * 2.75)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, *objs3, box3, floor3, true_bar, tlab, est_bar, elab, fac, note3], run_time=2.4)

        # 4. Two estimators: one biased, one not. (~14 s)
        title4 = self.txt("Two estimators", 31, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        line4 = NumberLine(x_range=[0, 1, 0.1], length=6.0, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 1.5)
        with audio.cue("draw"):
            self.play(Create(line4), run_time=1.0)
        dot_u = Dot(line4.n2p(0.62), radius=0.14, color=pal.OUTPUT)
        lab_u = self.formula(r"\sigma^2=\mathbb{E}[\tilde{\sigma}_m^2]", 26, pal.OUTPUT).next_to(dot_u, UP, buff=0.2)
        dot_b = Dot(line4.n2p(0.38), radius=0.14, color=pal.ERROR)
        lab_b = self.formula(r"\mathbb{E}[\hat{\sigma}_m^2]", 26, pal.ERROR).next_to(dot_b, DOWN, buff=0.2)
        with audio.cue("grow", pan=0.3):
            self.play(FadeIn(dot_u, scale=0.4), FadeIn(lab_u), run_time=1.0)
        with audio.cue("grow", pan=-0.3):
            self.play(FadeIn(dot_b, scale=0.4), FadeIn(lab_b), run_time=1.0)
        t4 = self.txt("One estimator is biased,\nthe other is not.", 27, pal.TEXT)
        self.fit_width(t4, 7.6)
        t4.move_to(DOWN * 0.7)
        with audio.cue("type", glyphs=len(t4.text)):
            self.type_in(t4, run_time=1.6)
        note4 = self.txt("Unbiased is desirable, but not always the best.\nBiased estimators can have other important properties.", 24, pal.FORMULA)
        self.fit_width(note4, 7.8)
        note4.move_to(DOWN * 2.5)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=2.2)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title4, line4, dot_u, lab_u, dot_b, lab_b, t4, note4], run_time=2.4)

        # 5. 5.4.3 Variance and standard error (5.45). (~17 s)
        title5 = self.txt("5.4.3 Variance and standard error", 28, pal.TEXT, BOLD)
        self.fit_width(title5, 7.8)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        objs5 = self.eq_rows(audio, [
            (r"\mathrm{Var}(\hat{\theta})", "(5.45)", 40, pal.FORMULA),
            (r"\mathrm{SE}(\hat{\theta})=\sqrt{\mathrm{Var}(\hat{\theta})}", None, 36, pal.DISTRIBUTION),
        ], [2.5, 1.5], run=1.6)
        line5 = NumberLine(x_range=[0, 1, 0.1], length=6.2, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.3)
        tick5 = Line(line5.n2p(0.5) + UP * 0.3, line5.n2p(0.5) + DOWN * 0.3, color=pal.OUTPUT, stroke_width=5)
        tlab5 = self.formula(r"\theta", 28, pal.OUTPUT).next_to(tick5, UP, buff=0.55)
        with audio.cue("draw"):
            self.play(Create(line5), Create(tick5), FadeIn(tlab5), run_time=1.0)
        rng = np.random.default_rng(125)
        vals = np.clip(0.5 + rng.normal(0, 0.09, 8), 0.1, 0.9)
        dots5 = VGroup(*[Dot(line5.n2p(v) + UP * (0.2 * ((i % 3) - 1) + 0.0), radius=0.1, color=pal.INPUT)
                         for i, v in enumerate(vals)])
        for i, d in enumerate(dots5):
            with audio.cue("grow", pan=-0.5 + 0.14 * i):
                self.play(FadeIn(d, scale=0.4), run_time=0.5)
        mu5, sd5 = float(vals.mean()), float(vals.std())
        spread = DoubleArrow(line5.n2p(mu5 - sd5) + DOWN * 0.8, line5.n2p(mu5 + sd5) + DOWN * 0.8, buff=0,
                             color=pal.FORMULA, stroke_width=4, tip_length=0.15)
        selab = self.formula(r"\mathrm{SE}", 28, pal.FORMULA).next_to(spread, DOWN, buff=0.12)
        with audio.cue("settle"):
            self.play(GrowFromCenter(spread), FadeIn(selab), run_time=1.0)
        note5 = self.txt("How much the estimate varies as we resample\nthe dataset from the data-generating process.", 24, pal.TEXT)
        self.fit_width(note5, 7.8)
        note5.move_to(DOWN * 2.75)
        with audio.cue("type", glyphs=len(note5.text)):
            self.type_in(note5, run_time=2.0)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title5, *objs5, line5, tick5, tlab5, dots5, spread, selab, note5], run_time=2.4)

        # 6. Low variance is desirable. (~14 s)
        title6 = self.txt("We want low variance too", 30, pal.TEXT, BOLD)
        self.fit_width(title6, 7.8)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        hi_line = NumberLine(x_range=[0, 1, 0.1], length=6.0, include_numbers=False,
                             color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 1.5)
        lo_line = NumberLine(x_range=[0, 1, 0.1], length=6.0, include_numbers=False,
                             color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.4)
        hi_tick = Line(hi_line.n2p(0.5) + UP * 0.25, hi_line.n2p(0.5) + DOWN * 0.25, color=pal.OUTPUT, stroke_width=4)
        lo_tick = Line(lo_line.n2p(0.5) + UP * 0.25, lo_line.n2p(0.5) + DOWN * 0.25, color=pal.OUTPUT, stroke_width=4)
        hi_lab = self.txt("high variance", 24, pal.ERROR).move_to(UP * 2.35)
        lo_lab = self.txt("low variance", 24, pal.OUTPUT).move_to(UP * 0.45)
        with audio.cue("draw"):
            self.play(Create(hi_line), Create(lo_line), Create(hi_tick), Create(lo_tick),
                      FadeIn(hi_lab), FadeIn(lo_lab), run_time=1.6)
        rng6 = np.random.default_rng(1250)
        hv = np.clip(0.5 + rng6.normal(0, 0.17, 7), 0.06, 0.94)
        lv = np.clip(0.5 + rng6.normal(0, 0.04, 7), 0.06, 0.94)
        hi_dots = VGroup(*[Dot(hi_line.n2p(v) + UP * 0.18 * ((i % 3) - 1), radius=0.1, color=pal.ERROR)
                           for i, v in enumerate(hv)])
        lo_dots = VGroup(*[Dot(lo_line.n2p(v) + UP * 0.18 * ((i % 3) - 1), radius=0.1, color=pal.OUTPUT)
                           for i, v in enumerate(lv)])
        with audio.cue("grow", pan=-0.3):
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in hi_dots], lag_ratio=0.15), run_time=1.8)
        with audio.cue("grow", pan=0.3):
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in lo_dots], lag_ratio=0.15), run_time=1.8)
        note6 = self.txt("We want low bias and relatively low variance.\nA finite sample leaves the estimate uncertain.", 24, pal.TEXT)
        self.fit_width(note6, 7.8)
        note6.move_to(DOWN * 2.5)
        with audio.cue("type", glyphs=len(note6.text)):
            self.type_in(note6, run_time=2.2)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, hi_line, lo_line, hi_tick, lo_tick, hi_lab, lo_lab,
                            hi_dots, lo_dots, note6], run_time=2.4)

        # 7. The book page returns; its text zooms back in. (~10 s)
        paper2, bands2 = self.make_page(w, h, band_info)
        pc2 = paper2.get_center()
        with audio.cue("grow"):
            self.play(FadeIn(paper2), run_time=1.2)
        with audio.cue("type", glyphs=max(60, len(bands2) * 14)):
            self.play(self.zoom_in_text(bands2, pc2))
        self.wait(0.6)
        everything = [paper2, *bands2]
        with audio.cue("zoom"):
            self.play(*[ZoomFade(m, pc2, 1.0, 1.04, run_time=1.2, rate_func=smooth) for m in everything])
            self.wait(0.6)
            self.play(*[ZoomFade(m, pc2, 1.0, 1 / 1.04, run_time=1.2, rate_func=smooth) for m in everything])
        self.wait(1.5)
        audio.finish()


if __name__ == "__main__":
    Page_125().render()
