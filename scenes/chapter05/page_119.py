"""Page 119 - why hyperparameters need a validation set, the 80/20 split,
and stale benchmarks. Sound design: ASMRSync cues, same as page 106."""

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


def cross_at(point, size=0.32):
    c = VGroup(Line(UL, DR), Line(UR, DL)).scale(size)
    c.set_color(pal.ERROR).set_stroke(width=6)
    return c.move_to(point)


class Page_119(Chapter5Scene):
    PAGE_NO = "119"
    RNG_SEED = 119

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)

        # 1. Learned on the training set, capacity always goes to the maximum.
        title1 = self.txt("Why not learn them on training data?", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        axes1 = Axes(x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=5.6, y_length=2.6,
                     axis_config={"color": pal.TEXT_DIM, "include_tip": False,
                                  "stroke_width": 1.5}).move_to(UP * 0.7)
        curve1 = axes1.plot(lambda t: 0.35 + 3.3 * np.exp(-0.9 * t), x_range=[0, 5],
                            color=pal.INPUT, stroke_width=4)
        bead1 = Dot(axes1.c2p(0, 0.35 + 3.3), radius=0.11, color=pal.FORMULA)
        label1 = self.txt("training error", 24, pal.INPUT).next_to(axes1, UP, buff=0.12)
        xlab1 = self.txt("model capacity", 24, pal.TEXT_DIM).next_to(axes1, DOWN, buff=0.15)
        with audio.cue("draw"):
            self.play(Create(axes1), Create(curve1), FadeIn(bead1), FadeIn(label1),
                      FadeIn(xlab1), run_time=2.4)
        self.wait(1.0)
        with audio.cue("slide", profile="converge"):
            self.play(MoveAlongPath(bead1, curve1), run_time=3.4, rate_func=smooth)
        maxlab1 = self.txt("maximum capacity", 24, pal.ERROR)
        maxlab1.next_to(bead1, UP, buff=0.35).shift(LEFT * 0.7)
        with audio.cue("settle"):
            self.play(FadeIn(maxlab1), bead1.animate.set_color(pal.ERROR), run_time=1.0)
        note1 = self.txt("Learned on training data, capacity would\nalways go to the maximum: overfitting.",
                         26, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=2.0)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title1, axes1, curve1, bead1, label1, xlab1, maxlab1, note1],
                           run_time=2.4)

        # 2. The bigger model always fits the training set better.
        title2 = self.txt("Training error picks the biggest model", 30, pal.TEXT, BOLD)
        self.fit_width(title2, 7.8)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        left2 = self.formula(r"\text{degree }9,\ \lambda=0", 30, pal.FORMULA).move_to(LEFT * 2.1 + UP * 1.9)
        right2 = self.formula(r"\text{degree }2,\ \lambda>0", 30, pal.FORMULA).move_to(RIGHT * 2.1 + UP * 1.9)
        with audio.cue("draw"):
            self.play(Write(left2), Write(right2), run_time=1.8)
        floor2 = Line(LEFT * 3.4, RIGHT * 3.4, color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.9)
        bar2a = Rectangle(width=1.5, height=0.25, color=pal.OUTPUT, fill_color=pal.OUTPUT,
                          fill_opacity=0.3).move_to([-2.1, -0.9 + 0.125, 0])
        bar2b = Rectangle(width=1.5, height=1.6, color=pal.ERROR, fill_color=pal.ERROR,
                          fill_opacity=0.3).move_to([2.1, -0.9 + 0.8, 0])
        lab2a = self.txt("tiny training error", 24, pal.OUTPUT).move_to(LEFT * 2.1 + DOWN * 1.35)
        lab2b = self.txt("larger training error", 24, pal.ERROR).move_to(RIGHT * 2.1 + DOWN * 1.35)
        shrink(lab2a, 3.0)
        shrink(lab2b, 3.0)
        with audio.cue("draw"):
            self.play(Create(floor2), run_time=1.0)
        with audio.cue("grow", pan=-0.4):
            self.play(GrowFromEdge(bar2a, DOWN), FadeIn(lab2a), run_time=1.8, rate_func=smooth)
        with audio.cue("grow", pan=0.4):
            self.play(GrowFromEdge(bar2b, DOWN), FadeIn(lab2b), run_time=2.4, rate_func=smooth)
        note2 = self.txt("The training set always prefers\nthe bigger model.", 27, pal.TEXT)
        self.fit_width(note2, 7.6)
        note2.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title2, left2, right2, floor2, bar2a, bar2b, lab2a, lab2b, note2],
                           run_time=2.4)

        # 3. The fix: a validation set the training algorithm does not observe.
        title3 = self.txt("The fix: a validation set", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        algo3 = RoundedRectangle(width=3.3, height=1.3, corner_radius=0.18,
                                 color=pal.INPUT).move_to(LEFT * 2.0 + UP * 1.5)
        algo3t = self.txt("Training\nalgorithm", 26, pal.INPUT).move_to(algo3)
        val3 = RoundedRectangle(width=3.3, height=1.3, corner_radius=0.18,
                                color=pal.DISTRIBUTION).move_to(RIGHT * 2.0 + UP * 1.5)
        val3t = self.txt("Validation\nset", 26, pal.DISTRIBUTION).move_to(val3)
        with audio.cue("grow", pan=-0.3):
            self.play(GrowFromCenter(algo3), FadeIn(algo3t), run_time=1.8, rate_func=smooth)
        with audio.cue("grow", pan=0.3):
            self.play(GrowFromCenter(val3), FadeIn(val3t), run_time=1.8, rate_func=smooth)
        arrow3 = Arrow(val3.get_left(), algo3.get_right(), buff=0.12, color=pal.ERROR)
        cross3 = cross_at(arrow3.get_center())
        with audio.cue("slide", profile="transfer"):
            self.play(GrowArrow(arrow3), run_time=1.2)
        with audio.cue("settle"):
            self.play(Create(cross3), run_time=0.8)
        note3 = self.txt("Examples the training algorithm\nnever observes.", 27, pal.TEXT)
        self.fit_width(note3, 7.6)
        note3.move_to(DOWN * 0.5)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.8)
        note3b = self.txt("It scores each hyperparameter setting.", 26, pal.OUTPUT)
        self.fit_width(note3b, 7.6)
        note3b.move_to(DOWN * 2.2)
        with audio.cue("type", glyphs=len(note3b.text)):
            self.type_in(note3b, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, algo3, algo3t, val3, val3t, arrow3, cross3, note3, note3b],
                           run_time=2.4)

        # 4. The test set must never influence any choice.
        title4 = self.txt("The test set stays untouched", 31, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        test4 = RoundedRectangle(width=3.4, height=1.0, corner_radius=0.18,
                                 color=pal.OUTPUT).move_to(UP * 1.9)
        test4t = self.txt("TEST SET", 26, pal.OUTPUT, BOLD).move_to(test4)
        choices4 = RoundedRectangle(width=6.2, height=1.3, corner_radius=0.18,
                                    color=pal.FORMULA).move_to(DOWN * 0.1)
        choices4t = self.txt("model choices,\nincluding hyperparameters", 25, pal.FORMULA).move_to(choices4)
        shrink(choices4t, 5.6)
        with audio.cue("grow"):
            self.play(GrowFromCenter(test4), FadeIn(test4t), run_time=1.8, rate_func=smooth)
        with audio.cue("grow"):
            self.play(GrowFromCenter(choices4), FadeIn(choices4t), run_time=1.8, rate_func=smooth)
        arrow4 = Arrow(test4.get_bottom(), choices4.get_top(), buff=0.12, color=pal.ERROR)
        cross4 = cross_at(arrow4.get_center())
        with audio.cue("slide", profile="transfer"):
            self.play(GrowArrow(arrow4), run_time=1.2)
        with audio.cue("settle"):
            self.play(Create(cross4), run_time=0.8)
        note4 = self.txt("No test example may guide any choice,\nso validation data comes from training data.", 26, pal.TEXT)
        self.fit_width(note4, 7.6)
        note4.move_to(DOWN * 2.4)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=2.2)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title4, test4, test4t, choices4, choices4t, arrow4, cross4, note4],
                           run_time=2.4)

        # 5. Split the training data 80 / 20.
        title5 = self.txt("Split the training data", 31, pal.TEXT, BOLD)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        whole5 = Rectangle(width=6.4, height=0.9, color=pal.INPUT, stroke_width=3).move_to(UP * 1.2)
        wlabel5 = self.txt("training data", 26, pal.INPUT).next_to(whole5, UP, buff=0.25)
        with audio.cue("grow"):
            self.play(Create(whole5), FadeIn(wlabel5), run_time=1.8, rate_func=smooth)
        self.wait(0.8)
        part5a = Rectangle(width=5.12, height=0.9, color=pal.INPUT, fill_color=pal.INPUT,
                           fill_opacity=0.3).move_to(whole5.get_left() + RIGHT * 2.56)
        part5b = Rectangle(width=1.28, height=0.9, color=pal.DISTRIBUTION, fill_color=pal.DISTRIBUTION,
                           fill_opacity=0.3).move_to(whole5.get_right() + LEFT * 0.64)
        pct5a = self.txt("80%", 30, pal.INPUT, BOLD).move_to(part5a)
        pct5b = self.txt("20%", 28, pal.DISTRIBUTION, BOLD).move_to(part5b)
        with audio.cue("slide", profile="transfer"):
            self.play(FadeOut(whole5), GrowFromEdge(part5a, LEFT), GrowFromEdge(part5b, RIGHT),
                      FadeIn(pct5a), FadeIn(pct5b), run_time=2.2, rate_func=smooth)
        lab5a = self.txt("learn the parameters", 24, pal.INPUT).move_to(part5a.get_center() + DOWN * 0.95)
        lab5b = self.txt("validation set", 24, pal.DISTRIBUTION).move_to(part5b.get_center() + DOWN * 0.95)
        with audio.cue("type", glyphs=len(lab5a.text) + len(lab5b.text)):
            self.play(FadeIn(lab5a, shift=UP * 0.1), FadeIn(lab5b, shift=UP * 0.1), run_time=1.4)
        note5 = self.txt("Two disjoint subsets.\nTypically 80% for training, 20% for validation.", 26, pal.TEXT)
        self.fit_width(note5, 7.6)
        note5.move_to(DOWN * 2.3)
        with audio.cue("type", glyphs=len(note5.text)):
            self.type_in(note5, run_time=2.2)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title5, wlabel5, part5a, part5b, pct5a, pct5b, lab5a, lab5b, note5],
                           run_time=2.4)

        # 6. Tune on validation, test once at the end.
        title6 = self.txt("Tune on validation, test once", 31, pal.TEXT, BOLD)
        self.fit_width(title6, 7.8)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        A = RoundedRectangle(width=3.1, height=0.9, corner_radius=0.15,
                             color=pal.INPUT).move_to(LEFT * 2.1 + UP * 1.7)
        B = RoundedRectangle(width=3.1, height=0.9, corner_radius=0.15,
                             color=pal.DISTRIBUTION).move_to(RIGHT * 2.1 + UP * 1.7)
        C = RoundedRectangle(width=4.4, height=0.9, corner_radius=0.15,
                             color=pal.FORMULA).move_to(UP * 0.1)
        At = shrink(self.txt("train on 80%", 24, pal.INPUT), 2.8).move_to(A)
        Bt = shrink(self.txt("validate on 20%", 24, pal.DISTRIBUTION), 2.8).move_to(B)
        Ct = shrink(self.txt("update hyperparameters", 24, pal.FORMULA), 4.0).move_to(C)
        with audio.cue("grow", pan=-0.4):
            self.play(GrowFromCenter(A), FadeIn(At), run_time=1.4, rate_func=smooth)
        with audio.cue("grow", pan=0.4):
            self.play(GrowFromCenter(B), FadeIn(Bt), run_time=1.4, rate_func=smooth)
        with audio.cue("grow", pan=0):
            self.play(GrowFromCenter(C), FadeIn(Ct), run_time=1.4, rate_func=smooth)
        ab = Arrow(A.get_right(), B.get_left(), buff=0.1, color=pal.TEXT_DIM)
        bc = Arrow(B.get_bottom(), C.get_top() + RIGHT * 1.3, buff=0.1, color=pal.TEXT_DIM)
        ca = Arrow(C.get_top() + LEFT * 1.3, A.get_bottom(), buff=0.1, color=pal.TEXT_DIM)
        with audio.cue("draw"):
            self.play(Create(ab), Create(bc), Create(ca), run_time=1.6)
        runner = Dot(A.get_center(), radius=0.13, color=pal.OUTPUT)
        path6 = VMobject().set_points_as_corners(
            [A.get_center(), B.get_center(), C.get_center(), A.get_center(),
             B.get_center(), C.get_center()])
        self.add(runner)
        with audio.cue("slide", profile="transfer"):
            self.play(MoveAlongPath(runner, path6), run_time=4.0, rate_func=linear)
        test6 = RoundedRectangle(width=4.4, height=0.9, corner_radius=0.15,
                                 color=pal.OUTPUT).move_to(DOWN * 1.55)
        test6t = self.txt("final: TEST SET", 24, pal.OUTPUT, BOLD).move_to(test6)
        down6 = Arrow(C.get_bottom(), test6.get_top(), buff=0.1, color=pal.OUTPUT)
        with audio.cue("grow"):
            self.play(GrowArrow(down6), GrowFromCenter(test6), FadeIn(test6t),
                      run_time=1.8, rate_func=smooth)
        note6 = self.txt("The test set is used once,\nafter all tuning is done.", 26, pal.TEXT)
        self.fit_width(note6, 7.6)
        note6.move_to(DOWN * 2.9)
        with audio.cue("type", glyphs=len(note6.text)):
            self.type_in(note6, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, A, B, C, At, Bt, Ct, ab, bc, ca, runner, down6, test6, test6t, note6],
                           run_time=2.4)

        # 7. Validation error is only slightly optimistic.
        title7 = self.txt("Validation error is a close estimate", 30, pal.TEXT, BOLD)
        self.fit_width(title7, 7.8)
        title7.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title7.text)):
            self.type_in(title7, run_time=1.6)
        floor7 = Line(LEFT * 3.6, RIGHT * 3.6, color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.9)
        heights = [0.7, 1.8, 2.8]
        colors = [pal.INPUT, pal.DISTRIBUTION, pal.ERROR]
        xs = [-2.4, 0.0, 2.4]
        bars7 = VGroup(*[
            Rectangle(width=1.3, height=h, color=c, fill_color=c, fill_opacity=0.3)
            .move_to([x, -0.9 + h / 2, 0])
            for h, c, x in zip(heights, colors, xs)])
        names7 = ["training", "validation", "generalization"]
        labs7 = VGroup(*[shrink(self.txt(n, 24, c), 2.3).move_to([x, -1.35, 0])
                         for n, c, x in zip(names7, colors, xs)])
        with audio.cue("draw"):
            self.play(Create(floor7), run_time=1.0)
        for i, pan in enumerate((-0.5, 0.0, 0.5)):
            with audio.cue("grow", pan=pan):
                self.play(GrowFromEdge(bars7[i], DOWN), FadeIn(labs7[i]),
                          run_time=1.8, rate_func=smooth)
        top7 = DashedLine([-3.2, -0.9 + heights[2], 0], [3.2, -0.9 + heights[2], 0],
                          color=pal.ERROR, stroke_width=3)
        gap7 = DoubleArrow([1.2, -0.9 + heights[1], 0], [1.2, -0.9 + heights[2], 0],
                           buff=0, color=pal.FORMULA, stroke_width=4, tip_length=0.15)
        with audio.cue("settle"):
            self.play(Create(top7), GrowFromCenter(gap7), run_time=1.4)
        note7 = self.txt("It still underestimates generalization error,\nbut by less than training error does.", 25, pal.TEXT)
        self.fit_width(note7, 7.7)
        note7.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note7.text)):
            self.type_in(note7, run_time=2.2)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title7, floor7, bars7, labs7, top7, gap7, note7], run_time=2.4)

        # 8. Reused test sets go stale.
        title8 = self.txt("Test sets go stale", 31, pal.TEXT, BOLD)
        title8.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title8.text)):
            self.type_in(title8, run_time=1.6)
        reported_lbl = self.txt("reported error", 24, pal.OUTPUT).move_to(LEFT * 1.9 + UP * 2.5)
        true_lbl = self.txt("true error", 24, pal.ERROR).move_to(RIGHT * 1.9 + UP * 2.5)
        axes8 = Axes(x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=5.6, y_length=2.8,
                     axis_config={"color": pal.TEXT_DIM, "include_tip": False,
                                  "stroke_width": 1.5}).move_to(UP * 0.6)
        xlab8 = self.txt("years of reuse", 24, pal.TEXT_DIM).next_to(axes8, DOWN, buff=0.15)
        with audio.cue("draw"):
            self.play(Create(axes8), FadeIn(xlab8), FadeIn(reported_lbl), FadeIn(true_lbl),
                      run_time=2.0)
        rep8 = axes8.plot(lambda t: 0.6 + 2.6 * np.exp(-0.8 * t), x_range=[0, 5],
                          color=pal.OUTPUT, stroke_width=4)
        tru8 = DashedVMobject(axes8.plot(lambda t: 1.7 + 1.4 * np.exp(-1.5 * t), x_range=[0, 5],
                                         color=pal.ERROR, stroke_width=4), num_dashes=28)
        with audio.cue("slide", profile="converge"):
            self.play(Create(rep8), run_time=3.0, rate_func=smooth)
        with audio.cue("draw"):
            self.play(Create(tru8), run_time=2.0)
        gap8 = DoubleArrow(axes8.c2p(4.6, 0.6 + 2.6 * np.exp(-0.8 * 4.6) + 0.05),
                           axes8.c2p(4.6, 1.7 + 1.4 * np.exp(-1.5 * 4.6) - 0.05),
                           buff=0, color=pal.FORMULA, stroke_width=4, tip_length=0.15)
        with audio.cue("settle"):
            self.play(GrowFromCenter(gap8), run_time=1.0)
        note8 = self.txt("Reused for years, the test set turns optimistic.\nThe field moves on to new benchmarks.", 25, pal.TEXT)
        self.fit_width(note8, 7.7)
        note8.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note8.text)):
            self.type_in(note8, run_time=2.2)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title8, reported_lbl, true_lbl, axes8, xlab8, rep8, tru8, gap8, note8],
                           run_time=2.4)

        # 9. Closing thought and camera emphasis.
        final = self.txt("Tune on validation data.\nEstimate on test data.", 30, pal.TEXT, BOLD)
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
        self.wait(4.0)
        audio.finish()


if __name__ == "__main__":
    Page_119().render()
