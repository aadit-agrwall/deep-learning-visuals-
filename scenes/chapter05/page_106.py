"""Page 106 — an ASMR experiment with measured animation/audio timing."""

from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.ml_shapes import dataset_table
from common.asmr_sync import ASMRSync


def weight_lanes(scene, weight):
    """Two tactile tracks: slide a feature and see its weighted contribution."""
    tracker = ValueTracker(1)
    input_line = NumberLine(x_range=[0, 3, 1], length=5.7, include_numbers=True,
                            font_size=24, color=pal.INPUT, stroke_width=2)
    output_line = NumberLine(x_range=[-6, 6, 2], length=5.7, include_numbers=True,
                             font_size=24, color=pal.OUTPUT, stroke_width=2)
    input_line.move_to(RIGHT * 0.25 + UP * 0.85)
    output_line.move_to(RIGHT * 0.25 + DOWN * 1.25)
    input_name = scene.formula(r"x_j", 32, pal.INPUT).move_to(LEFT * 3.5 + UP * 0.85)
    output_name = scene.formula(r"w_jx_j", 30, pal.OUTPUT).move_to(LEFT * 3.5 + DOWN * 1.25)
    input_dot = Dot(input_line.n2p(1), radius=0.12, color=pal.INPUT)
    output_dot = Dot(output_line.n2p(weight), radius=0.12, color=pal.OUTPUT)
    input_dot.add_updater(lambda m: m.move_to(input_line.n2p(tracker.get_value())))
    output_dot.add_updater(lambda m: m.move_to(output_line.n2p(weight * tracker.get_value())))
    number_x = DecimalNumber(1, num_decimal_places=1, font_size=34, color=pal.INPUT)
    number_y = DecimalNumber(weight, num_decimal_places=1, include_sign=True,
                             font_size=34, color=pal.OUTPUT)
    number_x.move_to(UP * 1.65)
    number_y.move_to(DOWN * 0.45)
    number_x.add_updater(lambda m: m.set_value(tracker.get_value()))
    number_y.add_updater(lambda m: m.set_value(weight * tracker.get_value()))
    group = VGroup(input_line, output_line, input_name, output_name,
                   input_dot, output_dot, number_x, number_y)
    return group, tracker


class Page_106(Chapter5Scene):
    PAGE_NO = "106"
    RNG_SEED = 91

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)

        # 1. Positive coefficient: feature rises, prediction rises.
        title1 = self.txt("Positive weight: prediction rises", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        weight1 = self.formula(r"w_j=+2", 40, pal.FORMULA).move_to(UP * 2.55)
        with audio.cue("draw"):
            self.play(Write(weight1), run_time=1.6)
        lanes1, x1 = weight_lanes(self, 2)
        with audio.cue("grow"):
            self.play(FadeIn(lanes1, shift=UP * 0.12), run_time=1.8, rate_func=smooth)
        self.wait(1.0)
        with audio.cue("slide", profile="positive"):
            self.play(x1.animate.set_value(3), run_time=3.6, rate_func=smooth)
        note1 = self.txt("Hold all other features fixed.\nA positive coefficient adds more.", 26, pal.TEXT).move_to(DOWN * 2.75)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=1.8)
        self.wait(3.0)
        lanes1.clear_updaters()
        with audio.cue("wipe"):
            self.dust_wipe([title1, weight1, lanes1, note1], run_time=2.4)
        self.remove(x1)

        # 2. Negative coefficient reverses the direction.
        title2 = self.txt("Negative weight: prediction falls", 30, pal.TEXT, BOLD)
        self.fit_width(title2, 7.8)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        weight2 = self.formula(r"w_j=-2", 40, pal.FORMULA).move_to(UP * 2.55)
        with audio.cue("draw"):
            self.play(Write(weight2), run_time=1.6)
        lanes2, x2 = weight_lanes(self, -2)
        with audio.cue("grow"):
            self.play(FadeIn(lanes2, shift=UP * 0.12), run_time=1.8, rate_func=smooth)
        self.wait(1.0)
        with audio.cue("slide", profile="negative"):
            self.play(x2.animate.set_value(3), run_time=3.6, rate_func=smooth)
        note2 = self.txt("The feature increases.\nIts contribution becomes more negative.", 26, pal.TEXT)
        self.fit_width(note2, 7.6)
        note2.move_to(DOWN * 2.75)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.8)
        self.wait(3.0)
        lanes2.clear_updaters()
        with audio.cue("wipe"):
            self.dust_wipe([title2, weight2, lanes2, note2], run_time=2.4)
        self.remove(x2)

        # 3. A larger absolute weight means greater sensitivity.
        title3 = self.txt("Magnitude sets the strength", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        delta3 = self.formula(r"\Delta x_j=1\qquad\Delta\hat{y}=w_j\Delta x_j", 36, pal.FORMULA)
        delta3.move_to(UP * 2.25)
        with audio.cue("draw"):
            self.play(Write(delta3), run_time=1.8)
        w3a = self.formula(r"w_j=1", 33, pal.FORMULA).move_to(LEFT * 2.4 + UP * 1.15)
        w3b = self.formula(r"w_j=4", 33, pal.FORMULA).move_to(LEFT * 2.4 + DOWN * 0.65)
        bar3a = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.13,
                                  color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=0.22)
        bar3b = RoundedRectangle(width=4.8, height=0.6, corner_radius=0.13,
                                  color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=0.22)
        bar3a.move_to(LEFT * 1.9 + UP * 0.35)
        bar3b.move_to(RIGHT * 0.1 + DOWN * 1.45)
        result3a = self.formula(r"\Delta\hat{y}=1", 32, pal.OUTPUT).next_to(bar3a, RIGHT, buff=0.35)
        result3b = self.formula(r"\Delta\hat{y}=4", 32, pal.OUTPUT).next_to(bar3b, UP, buff=0.3).shift(RIGHT * 1.9)
        with audio.cue("draw", pan=-0.3):
            self.play(Write(w3a), Write(w3b), run_time=1.4)
        with audio.cue("grow", pan=-0.3):
            self.play(GrowFromEdge(bar3a, LEFT), Write(result3a), run_time=2.2, rate_func=smooth)
        with audio.cue("grow", pan=0.3):
            self.play(GrowFromEdge(bar3b, LEFT), Write(result3b), run_time=2.8, rate_func=smooth)
        note3 = self.txt("Larger |w| → a larger effect\nfor the same feature change.", 26, pal.TEXT).move_to(DOWN * 2.9)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, delta3, w3a, w3b, bar3a, bar3b, result3a, result3b, note3], run_time=2.4)

        # 4. A zero coefficient ignores that feature completely.
        title4 = self.txt("Zero weight: no effect", 31, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        weight4 = self.formula(r"w_j=0", 40, pal.FORMULA).move_to(UP * 2.55)
        with audio.cue("draw"):
            self.play(Write(weight4), run_time=1.4)
        lanes4, x4 = weight_lanes(self, 0)
        with audio.cue("grow"):
            self.play(FadeIn(lanes4, shift=UP * 0.12), run_time=1.8, rate_func=smooth)
        with audio.cue("slide", profile="zero"):
            self.play(x4.animate.set_value(3), run_time=3.6, rate_func=smooth)
        note4 = self.txt("The input moves.\nThe contribution stays at zero.", 26, pal.TEXT).move_to(DOWN * 2.75)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=1.8)
        self.wait(3.0)
        lanes4.clear_updaters()
        with audio.cue("wipe"):
            self.dust_wipe([title4, weight4, lanes4, note4], run_time=2.4)
        self.remove(x4)

        # 5. Define task T and performance P; evaluation data is held out.
        title5 = self.txt("From a prediction to a score", 31, pal.TEXT, BOLD)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        task5 = self.formula(r"T:\quad\hat{y}=\mathbf{w}^{\top}\mathbf{x}", 42, pal.FORMULA).move_to(UP * 2.0)
        with audio.cue("draw"):
            self.play(Write(task5), run_time=1.8)
        statement5 = self.txt("P: How close are predictions\nto the correct targets?", 28, pal.TEXT).move_to(UP * 0.3)
        with audio.cue("type", glyphs=len(statement5.text)):
            self.type_in(statement5, run_time=2.0)
        test5 = RoundedRectangle(width=6.7, height=1.5, corner_radius=0.2, color=pal.INPUT)
        test5.move_to(DOWN * 1.75)
        label5 = self.txt("TEST SET\nheld out for evaluation", 27, pal.INPUT).move_to(test5)
        with audio.cue("grow"):
            self.play(GrowFromCenter(test5), FadeIn(label5, shift=UP * 0.1), run_time=2.0, rate_func=smooth)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title5, task5, statement5, test5, label5], run_time=2.4)

        # 6. A small, internally consistent held-out numerical example.
        title6 = self.txt("Predict on the test examples", 31, pal.TEXT, BOLD)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        parameters6 = self.formula(r"\mathbf{w}=(1,2)^{\top}\qquad\hat{y}=x_1+2x_2", 36, pal.FORMULA)
        parameters6.move_to(UP * 2.5)
        with audio.cue("draw"):
            self.play(Write(parameters6), run_time=1.8)
        table6 = dataset_table(["x1", "x2", "target"],
                               [["1", "0", "2"], ["0", "2", "2"], ["1", "1", "4"]],
                               col_width=1.7, row_height=0.85, font_size=24,
                               header_color=pal.INPUT, cell_color=pal.INPUT)
        for j in (2, 5, 8, 11):
            table6[3][j].set_color(pal.OUTPUT)
        table6.move_to(LEFT * 1.0)
        predictions6 = dataset_table(["ŷ"], [["1"], ["4"], ["3"]],
                                     col_width=1.3, row_height=0.85, font_size=26,
                                     header_color=pal.OUTPUT, cell_color=pal.OUTPUT)
        predictions6.move_to(RIGHT * 2.75)
        with audio.cue("draw", pan=-0.3):
            self.play(Create(table6), run_time=2.2)
        with audio.cue("grow", pan=0.4):
            self.play(FadeIn(predictions6, shift=RIGHT * 0.2), run_time=2.0, rate_func=smooth)
        held6 = self.txt("Three held-out examples: m = 3", 26, pal.TEXT).move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(held6.text)):
            self.type_in(held6, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, parameters6, table6, predictions6, held6], run_time=2.4)

        # 7. Signed residuals are the gaps between predictions and targets.
        title7 = self.txt("Measure each prediction error", 31, pal.TEXT, BOLD)
        title7.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title7.text)):
            self.type_in(title7, run_time=1.6)
        definition7 = self.formula(r"e_i=\hat{y}_i-y_i", 42, pal.ERROR).move_to(UP * 2.4)
        with audio.cue("draw"):
            self.play(Write(definition7), run_time=1.8)
        table7 = dataset_table(["ŷ", "y", "error"],
                               [["1", "2", "−1"], ["4", "2", "+2"], ["3", "4", "−1"]],
                               col_width=2.0, row_height=0.85, font_size=28,
                               header_color=pal.OUTPUT, cell_color=pal.OUTPUT)
        for j in (2, 5, 8, 11):
            table7[3][j].set_color(pal.ERROR)
        table7.move_to(UP * 0.1)
        with audio.cue("draw"):
            self.play(Create(table7), run_time=2.4)
        note7 = self.txt("Errors can be positive or negative.\nSquaring keeps them from cancelling.", 26, pal.TEXT)
        self.fit_width(note7, 7.6)
        note7.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note7.text)):
            self.type_in(note7, run_time=2.0)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title7, definition7, table7, note7], run_time=2.4)

        # 8. Square areas make the larger error's effect visible.
        title8 = self.txt("Square, then average", 31, pal.TEXT, BOLD)
        title8.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title8.text)):
            self.type_in(title8, run_time=1.6)
        errors8 = VGroup(self.formula(r"(-1)^2", 37, pal.ERROR),
                         self.formula(r"(+2)^2", 37, pal.ERROR),
                         self.formula(r"(-1)^2", 37, pal.ERROR))
        errors8.arrange(RIGHT, buff=1.3).move_to(UP * 1.85)
        with audio.cue("draw"):
            self.play(Write(errors8), run_time=1.8)
        square8a = Square(side_length=0.8, color=pal.ERROR, fill_color=pal.ERROR, fill_opacity=0.2).move_to(LEFT * 2.5 + UP * 0.05)
        square8b = Square(side_length=1.6, color=pal.ERROR, fill_color=pal.ERROR, fill_opacity=0.2).move_to(UP * 0.05)
        square8c = Square(side_length=0.8, color=pal.ERROR, fill_color=pal.ERROR, fill_opacity=0.2).move_to(RIGHT * 2.5 + UP * 0.05)
        area8a = self.formula("1", 38, pal.ERROR).move_to(square8a)
        area8b = self.formula("4", 38, pal.ERROR).move_to(square8b)
        area8c = self.formula("1", 38, pal.ERROR).move_to(square8c)
        with audio.cue("grow", pan=-0.55):
            self.play(GrowFromCenter(square8a), FadeIn(area8a), run_time=1.8, rate_func=smooth)
        with audio.cue("grow", pan=0):
            self.play(GrowFromCenter(square8b), FadeIn(area8b), run_time=2.4, rate_func=smooth)
        with audio.cue("grow", pan=0.55):
            self.play(GrowFromCenter(square8c), FadeIn(area8c), run_time=1.8, rate_func=smooth)
        average8 = self.formula(r"\mathrm{MSE}=\frac{1+4+1}{3}=2", 43, pal.FORMULA).move_to(DOWN * 1.85)
        with audio.cue("settle"):
            self.play(Write(average8), run_time=2.0)
        note8 = self.txt("Twice the error → four times the square.", 25, pal.TEXT)
        self.fit_width(note8, 7.7)
        note8.move_to(DOWN * 3.0)
        with audio.cue("type", glyphs=len(note8.text)):
            self.type_in(note8, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title8, errors8, square8a, square8b, square8c, area8a, area8b, area8c, average8, note8], run_time=2.4)

        # 9. Equations (5.4) and (5.5): component and Euclidean forms.
        title9 = self.txt("Two views of the same error", 31, pal.TEXT, BOLD)
        title9.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title9.text)):
            self.type_in(title9, run_time=1.6)
        eq9a = self.formula(r"\mathrm{MSE}_{\mathrm{test}}=\frac{1}{m}\sum_{i=1}^{m}\left(\hat{y}^{(\mathrm{test})}_i-y^{(\mathrm{test})}_i\right)^2", 36, pal.FORMULA)
        self.fit_width(eq9a, 7.5)
        eq9a.move_to(UP * 1.85)
        num9a = self.txt("(5.4)", 22, pal.TEXT_DIM).next_to(eq9a, DOWN, buff=0.3)
        with audio.cue("draw"):
            self.play(Write(eq9a), FadeIn(num9a), run_time=2.6)
        meaning9a = self.txt("Average squared error across m examples", 25, pal.TEXT)
        self.fit_width(meaning9a, 7.7)
        meaning9a.move_to(UP * 0.2)
        with audio.cue("type", glyphs=len(meaning9a.text)):
            self.type_in(meaning9a, run_time=1.8)
        eq9b = self.formula(r"\mathrm{MSE}_{\mathrm{test}}=\frac{1}{m}\left\|\hat{\mathbf{y}}^{(\mathrm{test})}-\mathbf{y}^{(\mathrm{test})}\right\|_2^2", 39, pal.FORMULA)
        self.fit_width(eq9b, 7.5)
        eq9b.move_to(DOWN * 1.25)
        num9b = self.txt("(5.5)", 22, pal.TEXT_DIM).next_to(eq9b, DOWN, buff=0.3)
        with audio.cue("draw"):
            self.play(Write(eq9b), FadeIn(num9b), run_time=2.6)
        meaning9b = self.txt("Squared Euclidean distance, divided by m", 25, pal.TEXT)
        self.fit_width(meaning9b, 7.7)
        meaning9b.move_to(DOWN * 2.9)
        with audio.cue("type", glyphs=len(meaning9b.text)):
            self.type_in(meaning9b, run_time=1.8)
        self.wait(3.5)
        with audio.cue("wipe"):
            self.dust_wipe([title9, eq9a, num9a, meaning9a, eq9b, num9b, meaning9b], run_time=2.4)

        # 10. Move the same predictions to their targets: MSE goes to zero.
        title10 = self.txt("Perfect matches: zero error", 31, pal.TEXT, BOLD)
        title10.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title10.text)):
            self.type_in(title10, run_time=1.6)
        legend10 = self.txt("○ prediction       ● target", 25, pal.OUTPUT).move_to(UP * 2.55)
        with audio.cue("type", glyphs=len(legend10.text)):
            self.type_in(legend10, run_time=1.5)
        progress10 = ValueTracker(0)
        lines10 = VGroup()
        predicted10 = VGroup()
        targets10 = VGroup()
        errors10 = VGroup()
        for i, (prediction, target) in enumerate([(1, 2), (4, 2), (3, 4)]):
            y = 1.35 - i * 1.05
            line = NumberLine(x_range=[0, 5, 1], length=5.8, color=pal.TEXT_DIM,
                               include_numbers=False, stroke_width=1.5).move_to(UP * y)
            target_dot = Dot(line.n2p(target), radius=0.09, color=pal.OUTPUT)
            pred_dot = Circle(radius=0.14, color=pal.OUTPUT, stroke_width=3).move_to(line.n2p(prediction))
            gap = Line(line.n2p(prediction), line.n2p(target), color=pal.ERROR, stroke_width=5)
            pred_dot.add_updater(lambda mob, line=line, p=prediction, t=target:
                                  mob.move_to(line.n2p(p + (t - p) * progress10.get_value())))
            gap.add_updater(lambda mob, line=line, p=prediction, t=target:
                             mob.put_start_and_end_on(line.n2p(p + (t - p) * progress10.get_value()),
                                                       line.n2p(t) + RIGHT * 0.00001)
                             .set_opacity(1 - progress10.get_value()))
            lines10.add(line)
            predicted10.add(pred_dot)
            targets10.add(target_dot)
            errors10.add(gap)
        mse_label10 = self.txt("MSE =", 29, pal.FORMULA).move_to(LEFT * 0.6 + DOWN * 1.85)
        mse10 = DecimalNumber(2, num_decimal_places=2, font_size=42, color=pal.ERROR).next_to(mse_label10, RIGHT, buff=0.3)
        mse10.add_updater(lambda m: m.set_value(2 * (1 - progress10.get_value()) ** 2))
        with audio.cue("draw"):
            self.play(Create(lines10), FadeIn(errors10), FadeIn(targets10), FadeIn(predicted10),
                       FadeIn(mse_label10), FadeIn(mse10), run_time=2.4)
        self.wait(1.0)
        with audio.cue("slide", profile="converge"):
            self.play(progress10.animate.set_value(1), run_time=4.0, rate_func=smooth)
        predicted10.clear_updaters()
        errors10.clear_updaters()
        mse10.clear_updaters()
        with audio.cue("settle"):
            self.play(mse10.animate.set_color(pal.OUTPUT), run_time=0.8)
        note10 = self.formula(r"\hat{\mathbf{y}}=\mathbf{y}\quad\Longrightarrow\quad\mathrm{MSE}=0", 35, pal.OUTPUT).move_to(DOWN * 2.95)
        with audio.cue("draw"):
            self.play(Write(note10), run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title10, legend10, lines10, predicted10, targets10, errors10, mse_label10, mse10, note10], run_time=2.4)
        self.remove(progress10)

        # 11. Learn on training examples; measure generalization on test examples.
        title11 = self.txt("Train the weights. Test the result.", 30, pal.TEXT, BOLD)
        self.fit_width(title11, 7.8)
        title11.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title11.text)):
            self.type_in(title11, run_time=1.6)
        train11 = RoundedRectangle(width=6.8, height=1.65, corner_radius=0.18, color=pal.INPUT).move_to(UP * 1.6)
        test11 = RoundedRectangle(width=6.8, height=1.65, corner_radius=0.18, color=pal.OUTPUT).move_to(DOWN * 1.0)
        train_label11 = self.txt("TRAINING SET", 26, pal.INPUT, BOLD).move_to(train11.get_center() + UP * 0.42)
        train_formula11 = self.formula(r"(\mathbf{X}^{\mathrm{train}},\mathbf{y}^{\mathrm{train}})\quad\min_{\mathbf{w}}\mathrm{MSE}_{\mathrm{train}}", 31, pal.FORMULA).move_to(train11.get_center() + DOWN * 0.3)
        test_label11 = self.txt("TEST SET", 26, pal.OUTPUT, BOLD).move_to(test11.get_center() + UP * 0.42)
        test_formula11 = self.formula(r"(\mathbf{X}^{\mathrm{test}},\mathbf{y}^{\mathrm{test}})\quad\mathrm{MSE}_{\mathrm{test}}", 31, pal.FORMULA).move_to(test11.get_center() + DOWN * 0.3)
        arrow11 = Arrow(train11.get_bottom(), test11.get_top(), buff=0.13, color=pal.FORMULA)
        with audio.cue("grow"):
            self.play(GrowFromCenter(train11), FadeIn(train_label11), Write(train_formula11), run_time=2.4)
        with audio.cue("slide", profile="transfer"):
            self.play(GrowArrow(arrow11), run_time=1.4)
        with audio.cue("grow"):
            self.play(GrowFromCenter(test11), FadeIn(test_label11), Write(test_formula11), run_time=2.4)
        note11 = self.txt("Fit on training data.\nEvaluate on held-out data.", 27, pal.TEXT).move_to(DOWN * 2.9)
        with audio.cue("type", glyphs=len(note11.text)):
            self.type_in(note11, run_time=1.8)
        self.wait(3.0)
        with audio.cue("wipe"):
            self.dust_wipe([title11, train11, test11, train_label11, train_formula11, test_label11, test_formula11, arrow11, note11], run_time=2.4)

        # 12. Equations (5.6), (5.7): a stationary point of the quadratic.
        title12 = self.txt("At the minimum, the gradient is zero", 29, pal.TEXT, BOLD)
        self.fit_width(title12, 7.8)
        title12.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title12.text)):
            self.type_in(title12, run_time=1.6)
        axes12 = Axes(x_range=[-2.4, 2.4, 1], y_range=[0, 4, 1], x_length=5.8, y_length=2.3,
                       axis_config={"color": pal.TEXT_DIM, "include_tip": False, "stroke_width": 1.5}).move_to(UP * 1.35)
        curve12 = axes12.plot(lambda t: 0.65 * t * t + 0.35, x_range=[-2.2, 2.2], color=pal.ERROR, stroke_width=3)
        position12 = ValueTracker(-1.9)
        bead12 = Dot(axes12.c2p(-1.9, 0.65 * 1.9 ** 2 + 0.35), radius=0.11, color=pal.FORMULA)
        bead12.add_updater(lambda m: m.move_to(axes12.c2p(position12.get_value(), 0.65 * position12.get_value() ** 2 + 0.35)))
        label12 = self.txt("training MSE", 24, pal.ERROR).next_to(axes12, UP, buff=0.12)
        with audio.cue("draw"):
            self.play(Create(axes12), Create(curve12), FadeIn(bead12), FadeIn(label12), run_time=2.4)
        with audio.cue("slide", profile="minimum"):
            self.play(position12.animate.set_value(0), run_time=3.4, rate_func=smooth)
        bead12.clear_updaters()
        tangent12 = Line(axes12.c2p(-0.8, 0.35), axes12.c2p(0.8, 0.35), color=pal.OUTPUT, stroke_width=3)
        with audio.cue("settle"):
            self.play(Create(tangent12), bead12.animate.set_color(pal.OUTPUT), run_time=1.2)
        eq12a = self.formula(r"\nabla_{\mathbf{w}}\mathrm{MSE}_{\mathrm{train}}=0", 39, pal.FORMULA).move_to(DOWN * 0.7)
        n12a = self.txt("(5.6)", 22, pal.TEXT_DIM).next_to(eq12a, DOWN, buff=0.22)
        with audio.cue("draw"):
            self.play(Write(eq12a), FadeIn(n12a), run_time=2.0)
        eq12b = self.formula(r"\nabla_{\mathbf{w}}\frac{1}{m}\left\|\hat{\mathbf{y}}^{(\mathrm{train})}-\mathbf{y}^{(\mathrm{train})}\right\|_2^2=0", 34, pal.FORMULA)
        self.fit_width(eq12b, 7.6)
        eq12b.move_to(DOWN * 2.2)
        n12b = self.txt("(5.7)", 22, pal.TEXT_DIM).next_to(eq12b, DOWN, buff=0.22)
        with audio.cue("draw"):
            self.play(Write(eq12b), FadeIn(n12b), run_time=2.6)
        self.wait(3.5)
        with audio.cue("wipe"):
            self.dust_wipe([title12, axes12, curve12, bead12, tangent12, label12, eq12a, n12a, eq12b, n12b], run_time=2.4)
        self.remove(position12)

        # 13. A quiet closing thought and inherited camera emphasis.
        final = self.txt("Weights shape the prediction.\nSquared errors measure the fit.", 30, pal.TEXT, BOLD)
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
    Page_106().render()
