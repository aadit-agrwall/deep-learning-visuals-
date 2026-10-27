"""Page 124 - bias of the sample mean (5.31-5.35), sample variance and its
bias (5.36-5.39). The book page opens the video, its text dissolves, the
animation plays, and the text returns at the end. Sound: ASMRSync cues only."""

from manim import *
import numpy as np
from pathlib import Path
from PIL import Image

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.asmr_sync import ASMRSync

PAGE_SRC = Path("assets/bookpage/page_124.png")
BAND_DIR = Path("assets/bookpage/page_124_bands")


def shrink(mob, width):
    """Only ever shrink a mobject to fit; never enlarge it."""
    if mob.width > width:
        mob.scale(width / mob.width)
    return mob


def build_bands():
    """Cut the book page into text-line strips (opaque, on white)."""
    if not PAGE_SRC.exists():
        raise FileNotFoundError(f"Missing {PAGE_SRC}. Copy the page 124 image there first.")
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


class Page_124(Chapter5Scene):
    PAGE_NO = "124"
    RNG_SEED = 124

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

    def eq_rows(self, audio, specs, ys, width=6.4, run=1.8):
        objs = []
        for (tex, tag, size, col), y in zip(specs, ys):
            f = self.formula(tex, size, col)
            shrink(f, width)
            f.move_to([-0.3, y, 0])
            t = self.txt(tag, 22, pal.TEXT_DIM).move_to([3.5, y, 0])
            objs.append(VGroup(f, t))
            with audio.cue("draw"):
                self.play(Write(f), FadeIn(t), run_time=run)
        return objs

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)
        w, h, band_info = build_bands()

        # 0. The book page opens, then its text dissolves away. (~9 s)
        paper, bands = self.make_page(w, h, band_info)
        with audio.cue("grow"):
            self.play(FadeIn(paper), *[FadeIn(b) for b in bands], run_time=1.4)
        self.wait(1.6)
        with audio.cue("wipe"):
            self.play(LaggedStart(*[FadeOut(b, shift=RIGHT * 0.5) for b in bands],
                                  lag_ratio=0.06, run_time=3.2))
        self.wait(0.5)
        with audio.cue("wipe"):
            self.dust_wipe([paper], run_time=2.4)

        # 1. Bias of the sample mean (5.31-5.33). (~13 s)
        title1 = self.txt("Bias of the sample mean", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        objs1 = self.eq_rows(audio, [
            (r"\mathrm{bias}(\hat{\mu}_m)=\mathbb{E}[\hat{\mu}_m]-\mu", "(5.31)", 34, pal.FORMULA),
            (r"=\mathbb{E}\left[\frac{1}{m}\sum_{i=1}^{m}x^{(i)}\right]-\mu", "(5.32)", 34, pal.FORMULA),
            (r"=\left(\frac{1}{m}\sum_{i=1}^{m}\mathbb{E}\left[x^{(i)}\right]\right)-\mu", "(5.33)", 34, pal.FORMULA),
        ], [1.9, 0.4, -1.1])
        hl1 = SurroundingRectangle(objs1[2][0], color=pal.OUTPUT, buff=0.15)
        with audio.cue("settle"):
            self.play(Create(hl1), run_time=0.8)
        note1 = self.txt("Again we calculate the expectation.\nIt moves inside the sum.", 26, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=1.6)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title1, *objs1, hl1, note1], run_time=2.4)

        # 2. The sample mean is unbiased (5.34-5.35). (~15 s)
        title2 = self.txt("The sample mean is unbiased", 30, pal.TEXT, BOLD)
        self.fit_width(title2, 7.8)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        objs2 = self.eq_rows(audio, [
            (r"=\left(\frac{1}{m}\sum_{i=1}^{m}\mu\right)-\mu", "(5.34)", 34, pal.FORMULA),
            (r"=\mu-\mu=0", "(5.35)", 38, pal.OUTPUT),
        ], [2.1, 0.8], run=2.0)
        box2 = SurroundingRectangle(objs2[1][0], color=pal.OUTPUT, buff=0.18)
        with audio.cue("settle"):
            self.play(Create(box2), run_time=0.8)
        line2 = NumberLine(x_range=[-1, 1, 0.5], length=5.6, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.7)
        zero2 = Line(line2.n2p(0) + UP * 0.3, line2.n2p(0) + DOWN * 0.3, color=pal.OUTPUT, stroke_width=5)
        zlab2 = self.formula(r"0", 30, pal.OUTPUT).next_to(zero2, DOWN, buff=0.12)
        with audio.cue("draw"):
            self.play(Create(line2), Create(zero2), FadeIn(zlab2), run_time=1.0)
        dot2 = Dot(line2.n2p(0.8), radius=0.13, color=pal.ERROR)
        blab2 = self.txt("bias", 24, pal.ERROR).next_to(dot2, UP, buff=0.15)
        with audio.cue("grow"):
            self.play(FadeIn(dot2, scale=0.4), FadeIn(blab2), run_time=0.8)
        with audio.cue("slide", profile="converge"):
            self.play(dot2.animate.move_to(line2.n2p(0)),
                      blab2.animate.next_to(line2.n2p(0), UP, buff=0.45),
                      run_time=2.4, rate_func=smooth)
        with audio.cue("settle"):
            self.play(dot2.animate.set_color(pal.OUTPUT), run_time=0.8)
        note2 = self.txt("An unbiased estimator of the\nGaussian mean parameter.", 26, pal.TEXT)
        self.fit_width(note2, 7.6)
        note2.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.6)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title2, *objs2, box2, line2, zero2, zlab2, dot2, blab2, note2], run_time=2.4)

        # 3. Two estimators of the Gaussian variance. (~14 s)
        title3 = self.txt("Estimating the variance", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        axes3 = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.5, 0.1], x_length=5.4, y_length=2.0,
                     axis_config={"color": pal.TEXT_DIM, "include_tip": False,
                                  "stroke_width": 1.5}).move_to(UP * 1.6)
        pdf = lambda t: float(np.exp(-0.5 * t * t) / np.sqrt(2 * np.pi))
        curve3 = axes3.plot(pdf, x_range=[-3.3, 3.3], color=pal.DISTRIBUTION, stroke_width=5)
        with audio.cue("draw"):
            self.play(Create(axes3), Create(curve3), run_time=1.8)
        sig3 = DoubleArrow(axes3.c2p(-1, 0.24), axes3.c2p(1, 0.24), buff=0,
                           color=pal.FORMULA, stroke_width=4, tip_length=0.15)
        siglab3 = self.formula(r"\sigma^2", 30, pal.FORMULA).next_to(sig3, UP, buff=0.08)
        with audio.cue("grow"):
            self.play(GrowFromCenter(sig3), FadeIn(siglab3), run_time=1.0)
        cardA = RoundedRectangle(width=3.5, height=1.2, corner_radius=0.18,
                                 color=pal.INPUT).move_to(LEFT * 2.0 + DOWN * 0.7)
        txtA = shrink(self.txt("estimator 1:\nsample variance", 22, pal.INPUT), 3.1).move_to(cardA)
        cardB = RoundedRectangle(width=3.5, height=1.2, corner_radius=0.18,
                                 color=pal.DISTRIBUTION).move_to(RIGHT * 2.0 + DOWN * 0.7)
        txtB = shrink(self.txt("estimator 2:\nanother candidate", 22, pal.DISTRIBUTION), 3.1).move_to(cardB)
        with audio.cue("grow", pan=-0.4):
            self.play(GrowFromCenter(cardA), FadeIn(txtA), run_time=1.3, rate_func=smooth)
        with audio.cue("grow", pan=0.4):
            self.play(GrowFromCenter(cardB), FadeIn(txtB), run_time=1.3, rate_func=smooth)
        note3 = self.txt("We compare two estimators of sigma squared.\nIs either one biased?", 25, pal.TEXT)
        self.fit_width(note3, 7.7)
        note3.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, axes3, curve3, sig3, siglab3, cardA, txtA, cardB, txtB, note3], run_time=2.4)

        # 4. The sample variance (5.36). (~16 s)
        title4 = self.txt("The sample variance", 31, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        eq4 = self.formula(r"\hat{\sigma}_m^2=\frac{1}{m}\sum_{i=1}^{m}\left(x^{(i)}-\hat{\mu}_m\right)^2",
                           36, pal.FORMULA)
        self.fit_width(eq4, 6.8)
        eq4.move_to(UP * 2.5)
        num4 = self.txt("(5.36)", 22, pal.TEXT_DIM).next_to(eq4, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq4), FadeIn(num4), run_time=2.0)
        line4 = NumberLine(x_range=[-3, 3, 1], length=6.0, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.7)
        samples = [-1.6, -0.6, 0.5, 1.0, 1.9]
        mean4 = float(np.mean(samples))
        dots4 = VGroup(*[Dot(line4.n2p(s), radius=0.11, color=pal.INPUT) for s in samples])
        mark4 = Triangle(color=pal.FORMULA, fill_color=pal.FORMULA, fill_opacity=1).scale(0.15)
        mark4.move_to(line4.n2p(mean4) + DOWN * 0.38)
        mlab4 = self.formula(r"\hat{\mu}_m", 28, pal.FORMULA).next_to(mark4, DOWN, buff=0.08)
        with audio.cue("grow"):
            self.play(Create(line4), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots4], lag_ratio=0.15),
                      FadeIn(mark4), FadeIn(mlab4), run_time=2.0)
        sq_y = -1.1
        connectors = VGroup()
        squares = VGroup()
        for s, d in zip(samples, dots4):
            side = 0.45 * abs(s - mean4)
            sq = Square(side_length=side, color=pal.ERROR, fill_color=pal.ERROR, fill_opacity=0.25)
            sq.move_to([line4.n2p(s)[0], sq_y, 0])
            squares.add(sq)
            connectors.add(DashedLine(d.get_center() + DOWN * 0.15, sq.get_top(),
                                      color=pal.TEXT_DIM, stroke_width=2))
        with audio.cue("grow", pan=0.2):
            self.play(Create(connectors), LaggedStart(*[GrowFromCenter(sq) for sq in squares], lag_ratio=0.2),
                      run_time=2.4, rate_func=smooth)
        note4 = self.txt("Average of the squared deviations\nfrom the sample mean.", 25, pal.TEXT)
        self.fit_width(note4, 7.7)
        note4.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title4, eq4, num4, line4, dots4, mark4, mlab4, connectors, squares, note4], run_time=2.4)

        # 5. Its expectation (5.37-5.39). (~15 s)
        title5 = self.txt("Is the sample variance biased?", 29, pal.TEXT, BOLD)
        self.fit_width(title5, 7.8)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        objs5 = self.eq_rows(audio, [
            (r"\mathrm{bias}(\hat{\sigma}_m^2)=\mathbb{E}[\hat{\sigma}_m^2]-\sigma^2", "(5.37)", 34, pal.FORMULA),
            (r"\mathbb{E}[\hat{\sigma}_m^2]=\mathbb{E}\left[\frac{1}{m}\sum_{i=1}^{m}\left(x^{(i)}-\hat{\mu}_m\right)^2\right]",
             "(5.38)", 28, pal.FORMULA),
            (r"=\frac{m-1}{m}\sigma^2", "(5.39)", 40, pal.OUTPUT),
        ], [2.0, 0.4, -1.2], width=6.5, run=2.0)
        box5 = SurroundingRectangle(objs5[2][0], color=pal.OUTPUT, buff=0.18)
        with audio.cue("settle"):
            self.play(Create(box5), run_time=0.8)
        note5 = self.txt("We begin by evaluating the term\nE of the sample variance.", 25, pal.TEXT)
        self.fit_width(note5, 7.7)
        note5.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note5.text)):
            self.type_in(note5, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title5, *objs5, box5, note5], run_time=2.4)

        # 6. The bias is -sigma^2 / m. (~18 s)
        title6 = self.txt("The sample variance is biased", 29, pal.TEXT, BOLD)
        self.fit_width(title6, 7.8)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        H = 2.2
        base_y = -0.6
        floor6 = Line(LEFT * 3.2, RIGHT * 3.2, color=pal.TEXT_DIM, stroke_width=2).move_to([0, base_y, 0])

        def exp_bar(m):
            eh = H * (m - 1) / m
            return Rectangle(width=1.5, height=eh, color=pal.ERROR, fill_color=pal.ERROR,
                             fill_opacity=0.3).move_to([1.7, base_y + eh / 2, 0])

        def gap_arrow(m, tip):
            eh = H * (m - 1) / m
            return DoubleArrow([2.9, base_y + eh, 0], [2.9, base_y + H, 0], buff=0,
                               color=pal.FORMULA, stroke_width=4, tip_length=tip)

        true_bar = Rectangle(width=1.5, height=H, color=pal.OUTPUT, fill_color=pal.OUTPUT,
                             fill_opacity=0.3).move_to([-1.7, base_y + H / 2, 0])
        tlab = self.formula(r"\sigma^2", 30, pal.OUTPUT).move_to([-1.7, base_y + H + 0.35, 0])
        elab = self.formula(r"\mathbb{E}[\hat{\sigma}_m^2]", 28, pal.ERROR).move_to([1.7, base_y + H + 0.35, 0])
        ebar = exp_bar(3)
        with audio.cue("grow", pan=-0.3):
            self.play(Create(floor6), GrowFromEdge(true_bar, DOWN), FadeIn(tlab),
                      run_time=1.5, rate_func=smooth)
        with audio.cue("grow", pan=0.3):
            self.play(GrowFromEdge(ebar, DOWN), FadeIn(elab), run_time=1.5, rate_func=smooth)
        top_line = DashedLine([-0.95, base_y + H, 0], [2.9, base_y + H, 0], color=pal.TEXT_DIM, stroke_width=2)
        gap = gap_arrow(3, 0.15)
        mlab = self.txt("m = 3", 24, pal.TEXT).move_to([0, base_y - 0.4, 0])
        with audio.cue("settle"):
            self.play(Create(top_line), GrowFromCenter(gap), FadeIn(mlab), run_time=1.2)
        eq6 = self.formula(r"\mathrm{bias}(\hat{\sigma}_m^2)=-\sigma^2/m", 36, pal.ERROR)
        self.fit_width(eq6, 7.0)
        eq6.move_to(DOWN * 1.8)
        with audio.cue("draw"):
            self.play(Write(eq6), run_time=1.8)
        mlab2 = self.txt("m = 12", 24, pal.TEXT).move_to([0, base_y - 0.4, 0])
        with audio.cue("slide", profile="converge"):
            self.play(Transform(ebar, exp_bar(12)), Transform(gap, gap_arrow(12, 0.07)),
                      Transform(mlab, mlab2), run_time=2.4, rate_func=smooth)
        note6 = self.txt("Therefore the sample variance\nis a biased estimator.", 26, pal.TEXT)
        self.fit_width(note6, 7.6)
        note6.move_to(DOWN * 2.85)
        with audio.cue("type", glyphs=len(note6.text)):
            self.type_in(note6, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, floor6, true_bar, tlab, elab, ebar, top_line, gap, mlab, eq6, note6],
                           run_time=2.4)

        # 7. The book page returns, text and all. (~9 s)
        paper2, bands2 = self.make_page(w, h, band_info)
        with audio.cue("grow"):
            self.play(FadeIn(paper2), run_time=1.2)
        with audio.cue("type", glyphs=max(60, len(bands2) * 14)):
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in bands2],
                                  lag_ratio=0.05, run_time=3.0))
        self.wait(0.6)
        page_all = Group(paper2, *bands2)
        with audio.cue("zoom"):
            self.play(page_all.animate.scale(1.04), run_time=1.2, rate_func=smooth)
            self.wait(0.6)
            self.play(page_all.animate.scale(1 / 1.04), run_time=1.2, rate_func=smooth)
        self.wait(1.5)
        audio.finish()


if __name__ == "__main__":
    Page_124().render()
