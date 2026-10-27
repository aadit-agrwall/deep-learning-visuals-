"""Page 120 - 5.3.1 Cross-Validation, 5.4 Estimators/Bias/Variance,
5.4.1 Point Estimation. Sound design: ASMRSync cues, same as pages 106/119.
Target length: about 75 s."""

from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.asmr_sync import ASMRSync


def shrink(mob, width):
    """Only ever shrink a mobject to fit; never enlarge it."""
    if mob.width > width:
        mob.scale(width / mob.width)
    return mob


class Page_120(Chapter5Scene):
    PAGE_NO = "120"
    RNG_SEED = 120

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)

        # 1. A small test set makes the comparison uncertain. (~11.7 s)
        title1 = self.txt("A small test set misleads", 31, pal.TEXT, BOLD)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        data1 = Rectangle(width=6.4, height=0.7, color=pal.INPUT, fill_color=pal.INPUT,
                          fill_opacity=0.25).move_to(UP * 2.35)
        slice1 = Rectangle(width=0.9, height=0.7, color=pal.OUTPUT, fill_color=pal.OUTPUT,
                           fill_opacity=0.5).move_to(data1.get_right() + LEFT * 0.45)
        dlab1 = self.txt("dataset", 24, pal.INPUT).move_to(data1.get_center() + LEFT * 1.0)
        slab1 = self.txt("test", 22, pal.TEXT).move_to(slice1)
        with audio.cue("grow"):
            self.play(GrowFromEdge(data1, LEFT), FadeIn(slice1), FadeIn(dlab1), FadeIn(slab1),
                      run_time=1.8, rate_func=smooth)
        floor1 = Line(LEFT * 3.4, RIGHT * 3.4, color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.7)
        barA = Rectangle(width=1.4, height=1.5, color=pal.INPUT, fill_color=pal.INPUT,
                         fill_opacity=0.3).move_to([-1.8, -0.7 + 0.75, 0])
        barB = Rectangle(width=1.4, height=1.9, color=pal.DISTRIBUTION, fill_color=pal.DISTRIBUTION,
                         fill_opacity=0.3).move_to([1.8, -0.7 + 0.95, 0])

        def whisker(x, top, half=0.55):
            v = Line([x, top - half, 0], [x, top + half, 0], color=pal.ERROR, stroke_width=4)
            c1 = Line([x - 0.2, top - half, 0], [x + 0.2, top - half, 0], color=pal.ERROR, stroke_width=4)
            c2 = Line([x - 0.2, top + half, 0], [x + 0.2, top + half, 0], color=pal.ERROR, stroke_width=4)
            return VGroup(v, c1, c2)

        whA = whisker(-1.8, 0.8)
        whB = whisker(1.8, 1.2)
        labA = self.txt("algorithm A", 24, pal.INPUT).move_to([-1.8, -1.05, 0])
        labB = self.txt("algorithm B", 24, pal.DISTRIBUTION).move_to([1.8, -1.05, 0])
        with audio.cue("grow", pan=0.2):
            self.play(Create(floor1), GrowFromEdge(barA, DOWN), GrowFromEdge(barB, DOWN),
                      FadeIn(labA), FadeIn(labB), Create(whA), Create(whB),
                      run_time=2.2, rate_func=smooth)
        self.wait(0.5)
        note1 = self.txt("Statistical uncertainty:\nhard to say that A beats B.", 27, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=2.0)
        self.wait(1.2)
        with audio.cue("wipe"):
            self.dust_wipe([title1, data1, slice1, dlab1, slab1, floor1, barA, barB,
                            whA, whB, labA, labB, note1], run_time=2.4)

        # 2. k-fold cross-validation: the test fold rotates. (~15.6 s)
        title2 = self.txt("k-fold cross-validation", 31, pal.TEXT, BOLD)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        klab = self.txt("k = 5 nonoverlapping subsets", 26, pal.OUTPUT).move_to(UP * 2.55)
        with audio.cue("type", glyphs=len(klab.text)):
            self.type_in(klab, run_time=1.6)
        folds = VGroup()
        for i in range(5):
            r = Rectangle(width=1.2, height=0.9, color=pal.INPUT, fill_color=pal.INPUT,
                          fill_opacity=0.3)
            n = self.txt(str(i + 1), 24, pal.TEXT).move_to(r)
            folds.add(VGroup(r, n))
        folds.arrange(RIGHT, buff=0.08).move_to(UP * 1.5)
        legend = VGroup(
            VGroup(Square(0.22, color=pal.INPUT, fill_color=pal.INPUT, fill_opacity=0.5),
                   self.txt("training set", 22, pal.INPUT)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.22, color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=0.7),
                   self.txt("test set", 22, pal.OUTPUT)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.8).move_to(DOWN * 0.45)
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(f) for f in folds], lag_ratio=0.18),
                      FadeIn(legend), run_time=2.0)
        marker = VGroup(Triangle(color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=1).scale(0.14),
                        self.txt("test fold", 22, pal.OUTPUT)).arrange(DOWN, buff=0.08)
        spot = lambda i: folds[i][0].get_bottom() + DOWN * 0.42
        marker.move_to(spot(0))
        for i in range(5):
            anims = []
            if i == 0:
                anims.append(FadeIn(marker))
            else:
                anims.append(folds[i - 1][0].animate.set_fill(pal.INPUT, opacity=0.3).set_stroke(pal.INPUT))
                anims.append(marker.animate.move_to(spot(i)))
            anims.append(folds[i][0].animate.set_fill(pal.OUTPUT, opacity=0.55).set_stroke(pal.OUTPUT))
            with audio.cue("grow", pan=-0.5 + 0.25 * i):
                self.play(*anims, run_time=1.0, rate_func=smooth)
        note2 = self.txt("Trial i: the i-th subset is the test set,\nthe rest is the training set.", 26, pal.TEXT)
        self.fit_width(note2, 7.6)
        note2.move_to(DOWN * 2.5)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.8)
        self.wait(1.2)
        with audio.cue("wipe"):
            self.dust_wipe([title2, klab, folds, legend, marker, note2], run_time=2.4)

        # 3. Average the k test errors. (~12.0 s)
        title3 = self.txt("Average the k test errors", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        floor3 = Line(LEFT * 3.4, RIGHT * 3.4, color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.5)
        heights = [1.1, 1.6, 0.9, 1.4, 1.2]
        xs = [-2.6, -1.3, 0.0, 1.3, 2.6]
        bars3 = VGroup(*[
            Rectangle(width=0.8, height=h, color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=0.3)
            .move_to([x, 0.5 + h / 2, 0]) for h, x in zip(heights, xs)])
        digits3 = VGroup(*[self.txt(str(i + 1), 22, pal.TEXT_DIM).move_to([x, 0.2, 0])
                           for i, x in enumerate(xs)])
        with audio.cue("grow"):
            self.play(Create(floor3),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars3], lag_ratio=0.2),
                      FadeIn(digits3), run_time=2.0, rate_func=smooth)
        mean_y = 0.5 + sum(heights) / 5
        mean3 = DashedLine([-3.4, mean_y, 0], [3.4, mean_y, 0], color=pal.FORMULA, stroke_width=4)
        mlab3 = self.txt("average", 22, pal.FORMULA).next_to(mean3.get_end(), UP, buff=0.08)
        with audio.cue("draw"):
            self.play(Create(mean3), FadeIn(mlab3), run_time=1.0)
        eq3 = self.formula(r"\text{test error}\approx\frac{1}{k}\sum_{i=1}^{k}\text{error}_i", 36, pal.FORMULA)
        self.fit_width(eq3, 7.2)
        eq3.move_to(DOWN * 1.0)
        with audio.cue("draw"):
            self.play(Write(eq3), run_time=1.8)
        note3 = self.txt("Every example gets used for testing.\nNo unbiased variance estimator exists.", 25, pal.TEXT)
        self.fit_width(note3, 7.7)
        note3.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=2.0)
        self.wait(1.2)
        with audio.cue("wipe"):
            self.dust_wipe([title3, floor3, bars3, digits3, mean3, mlab3, eq3, note3], run_time=2.4)

        # 4. 5.4 Estimators, bias and variance. (~10.8 s)
        title4 = self.txt("5.4 Estimators, bias, variance", 30, pal.TEXT, BOLD)
        self.fit_width(title4, 7.8)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        cards = VGroup()
        for text, col in (("Parameter\nestimation", pal.INPUT), ("Bias", pal.ERROR),
                          ("Variance", pal.DISTRIBUTION)):
            rect = RoundedRectangle(width=2.3, height=1.1, corner_radius=0.15, color=col)
            lab = shrink(self.txt(text, 24, col), 2.0).move_to(rect)
            cards.add(VGroup(rect, lab))
        cards.arrange(RIGHT, buff=0.3).move_to(UP * 1.6)
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(c) for c in cards], lag_ratio=0.35),
                      run_time=2.4)
        box4 = RoundedRectangle(width=6.4, height=1.1, corner_radius=0.15,
                                color=pal.FORMULA).move_to(DOWN * 0.7)
        box4t = shrink(self.txt("generalization, underfitting,\noverfitting", 25, pal.FORMULA), 6.0).move_to(box4)
        arrow4 = Arrow(cards.get_bottom(), box4.get_top(), buff=0.12, color=pal.FORMULA)
        with audio.cue("slide", profile="transfer"):
            self.play(GrowArrow(arrow4), GrowFromCenter(box4), FadeIn(box4t),
                      run_time=1.4, rate_func=smooth)
        note4 = self.txt("Statistics formalizes how well a task\ntransfers beyond the training set.", 26, pal.TEXT)
        self.fit_width(note4, 7.6)
        note4.move_to(DOWN * 2.5)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=1.8)
        self.wait(1.2)
        with audio.cue("wipe"):
            self.dust_wipe([title4, cards, arrow4, box4, box4t, note4], run_time=2.4)

        # 5. 5.4.1 Point estimation: theta-hat approaches theta. (~14.0 s)
        title5 = self.txt("5.4.1 Point estimation", 31, pal.TEXT, BOLD)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        line5 = NumberLine(x_range=[0, 10, 1], length=6.0, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.4)
        tick5 = Line(line5.n2p(6.5) + UP * 0.25, line5.n2p(6.5) + DOWN * 0.25,
                     color=pal.OUTPUT, stroke_width=4)
        theta5 = self.formula(r"\boldsymbol{\theta}", 32, pal.OUTPUT).next_to(tick5, UP, buff=0.1)
        est_dot = Dot(line5.n2p(1.0), radius=0.13, color=pal.FORMULA)
        est_lab = self.formula(r"\hat{\boldsymbol{\theta}}", 32, pal.FORMULA).next_to(est_dot, DOWN, buff=0.15)
        est5 = VGroup(est_dot, est_lab)
        with audio.cue("draw"):
            self.play(Create(line5), Create(tick5), FadeIn(theta5), FadeIn(est5), run_time=1.2)
        sample_pos = [(5.2, 1.9), (5.9, 2.15), (6.3, 1.9), (6.8, 2.15), (7.4, 1.9), (7.9, 2.15), (6.0, 1.7)]
        dots5 = VGroup(*[Dot([line5.n2p(x)[0], y, 0], radius=0.09, color=pal.INPUT)
                         for x, y in sample_pos])
        samp5 = self.formula(r"\{\mathbf{x}^{(1)},\dots,\mathbf{x}^{(m)}\}\ \text{i.i.d.}", 34, pal.DISTRIBUTION)
        self.fit_width(samp5, 7.4)
        samp5.move_to(UP * 2.65)
        with audio.cue("grow"):
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots5], lag_ratio=0.12),
                      FadeIn(samp5), run_time=1.6)
        dx = line5.n2p(6.0)[0] - line5.n2p(1.0)[0]
        with audio.cue("slide", profile="converge"):
            self.play(est5.animate.shift(RIGHT * dx), run_time=2.8, rate_func=smooth)
        eq5 = self.formula(r"\hat{\boldsymbol{\theta}}\ \text{estimates the true}\ \boldsymbol{\theta}", 36, pal.FORMULA)
        self.fit_width(eq5, 7.4)
        eq5.move_to(DOWN * 1.2)
        with audio.cue("draw"):
            self.play(Write(eq5), run_time=1.4)
        note5 = self.txt("A point estimate is the single \"best\"\nguess of a quantity of interest.", 26, pal.TEXT)
        self.fit_width(note5, 7.6)
        note5.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note5.text)):
            self.type_in(note5, run_time=1.8)
        self.wait(1.2)
        with audio.cue("wipe"):
            self.dust_wipe([title5, line5, tick5, theta5, est5, dots5, samp5, eq5, note5], run_time=2.4)

        # 6. Closing thought and camera emphasis. (~10.6 s)
        final = self.txt("Cross-validation reuses every example.\nEstimators guess the true parameter.", 30, pal.TEXT, BOLD)
        self.fit_width(final, 7.6)
        final.move_to(ORIGIN)
        with audio.cue("type", glyphs=len(final.text)):
            self.type_in(final, run_time=2.4)
        underline = Underline(final, color=pal.INPUT, stroke_width=3, buff=0.22)
        with audio.cue("draw"):
            self.play(Create(underline), run_time=1.4)
        self.wait(0.8)
        with audio.cue("zoom"):
            self.zoom_pulse(final, zoom_scale=0.96, run_time_in=1.2, hold=0.6, run_time_out=1.2)
        self.wait(3.0)
        audio.finish()


if __name__ == "__main__":
    Page_120().render()
