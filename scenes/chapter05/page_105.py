"""Page 105: supervised targets and the linear regression model (5.3)."""

from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.ml_shapes import dataset_table, pixel_grid, neuron_node


class Page_105(Chapter5Scene):
    PAGE_NO = "105"
    RNG_SEED = 81

    def construct(self):
        self.init_page()

        # 1. A set does not impose a shared example length.
        title1 = self.txt("When examples have different sizes", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        self.type_in(title1, run_time=1.2)

        set1 = self.formula(r"\mathcal{D}=\{\mathbf{x}^{(1)},\mathbf{x}^{(2)},\ldots,\mathbf{x}^{(m)}\}", 38, pal.FORMULA)
        set1.move_to(UP * 2.25)
        self.play(Write(set1), run_time=1.2)

        image1a = pixel_grid(rows=3, cols=3, cell_size=0.48, seed=81)
        image1b = pixel_grid(rows=3, cols=5, cell_size=0.48, seed=82)
        image1a.move_to(LEFT * 2.1 + UP * 0.15)
        image1b.move_to(RIGHT * 1.65 + UP * 0.15)
        name1a = self.formula(r"\mathbf{x}^{(1)}", 32, pal.INPUT).next_to(image1a, UP, buff=0.3)
        name1b = self.formula(r"\mathbf{x}^{(2)}", 32, pal.INPUT).next_to(image1b, UP, buff=0.3)
        count1a = self.txt("9 pixels", 25, pal.INPUT).next_to(image1a, DOWN, buff=0.3)
        count1b = self.txt("15 pixels", 25, pal.INPUT).next_to(image1b, DOWN, buff=0.3)
        self.play(Create(image1a), Create(image1b), Write(name1a), Write(name1b), run_time=1.5)
        self.type_in(count1a, run_time=0.6)
        self.type_in(count1b, run_time=0.6)

        note1 = self.txt("A collection of m examples.\nTheir vector lengths can differ.", 26, pal.TEXT)
        note1.move_to(DOWN * 2.15)
        self.type_in(note1, run_time=1.5)
        self.wait(2.5)
        self.dust_wipe([title1, set1, image1a, image1b, name1a, name1b, count1a, count1b, note1])

        # 2. A supervised example pairs features with a target.
        title2 = self.txt("Supervised examples have targets", 30, pal.TEXT, BOLD)
        self.fit_width(title2, 7.8)
        title2.to_edge(UP, buff=0.6)
        self.type_in(title2, run_time=1.2)
        pair2 = self.formula(r"(\mathbf{x}^{(i)},\ y_i)", 44, pal.FORMULA)
        pair2.move_to(UP * 2.2)
        self.play(Write(pair2), run_time=1.0)

        photo2 = pixel_grid(rows=4, cols=4, cell_size=0.42, seed=83)
        photo2.move_to(LEFT * 2.25 + UP * 0.1)
        photo_label2 = self.txt("photo of a car", 25, pal.INPUT).next_to(photo2, DOWN, buff=0.35)
        features2 = self.txt("features x", 26, pal.INPUT, BOLD).next_to(photo2, UP, buff=0.35)
        target2 = neuron_node("1", color=pal.OUTPUT, radius=0.65, label_size=40, label_color=pal.OUTPUT)
        target2.move_to(RIGHT * 2.3 + UP * 0.1)
        target_label2 = self.txt("target y", 26, pal.OUTPUT, BOLD).next_to(target2, UP, buff=0.55)
        arrow2 = Arrow(photo2.get_right(), target2.get_left(), buff=0.25, color=pal.TEXT_DIM)
        self.play(Create(photo2), FadeIn(features2), FadeIn(photo_label2), run_time=1.2)
        self.play(GrowArrow(arrow2), Create(target2), FadeIn(target_label2), run_time=1.0)

        codes2 = self.mono("0 = person   1 = car   2 = cat", 23, pal.OUTPUT)
        codes2.move_to(DOWN * 1.8)
        self.type_in(codes2, run_time=1.4)
        note2 = self.txt("The code tells us which object appears.", 25, pal.TEXT)
        self.fit_width(note2, 7.5)
        note2.move_to(DOWN * 2.75)
        self.type_in(note2, run_time=1.3)
        self.wait(2.5)
        self.dust_wipe([title2, pair2, photo2, photo_label2, features2, target2, target_label2, arrow2, codes2, note2])

        # 3. Fixed-size features form X; aligned targets form y.
        title3 = self.txt("One target for each row", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        self.type_in(title3, run_time=1.0)

        table3 = dataset_table(
            ["x1", "x2", "x3"],
            [["0.2", "0.8", "1.4"], ["0.9", "0.1", "0.6"], ["0.5", "0.3", "1.1"]],
            col_width=1.7, row_height=0.85, font_size=24,
            header_color=pal.INPUT, cell_color=pal.INPUT,
        )
        table3.move_to(LEFT * 0.95 + UP * 0.25)
        labels3 = dataset_table(
            ["y"], [["1"], ["0"], ["2"]],
            col_width=1.15, row_height=0.85, font_size=24,
            header_color=pal.OUTPUT, cell_color=pal.OUTPUT,
        )
        labels3.move_to(RIGHT * 2.75 + UP * 0.25)
        x_name3 = self.formula(r"\mathbf{X}\in\mathbb{R}^{m\times n}", 34, pal.INPUT)
        x_name3.next_to(table3, UP, buff=0.4)
        y_name3 = self.formula(r"\mathbf{y}", 38, pal.OUTPUT).next_to(labels3, UP, buff=0.4)
        self.play(Create(table3), Write(x_name3), run_time=1.5)
        self.play(Create(labels3), Write(y_name3), run_time=1.0)

        row3 = RoundedRectangle(width=5.2, height=0.83, corner_radius=0.08, color=pal.FORMULA, stroke_width=3)
        row3.move_to(LEFT * 0.95 + DOWN * 0.175)
        label_row3 = RoundedRectangle(width=1.25, height=0.83, corner_radius=0.08, color=pal.FORMULA, stroke_width=3)
        label_row3.move_to(RIGHT * 2.75 + DOWN * 0.175)
        match3 = Arrow(row3.get_right(), label_row3.get_left(), buff=0.12, color=pal.FORMULA, stroke_width=3)
        self.play(Create(row3), GrowArrow(match3), Create(label_row3), run_time=1.0)
        mapping3 = self.formula(r"\mathbf{X}_{i,:}=\mathbf{x}^{(i)\top}\quad\longleftrightarrow\quad y_i", 33, pal.FORMULA)
        mapping3.move_to(DOWN * 2.15)
        self.play(Write(mapping3), run_time=1.2)
        note3 = self.txt("m examples, n features per example", 25, pal.TEXT).move_to(DOWN * 3.0)
        self.type_in(note3, run_time=1.2)
        self.wait(2.5)
        self.dust_wipe([title3, table3, labels3, x_name3, y_name3, row3, label_row3, match3, mapping3, note3])

        # 4. A target can be a sequence rather than one number.
        title4 = self.txt("A label can be a whole sentence", 30, pal.TEXT, BOLD)
        self.fit_width(title4, 7.8)
        title4.to_edge(UP, buff=0.6)
        self.type_in(title4, run_time=1.2)

        waveform4 = VGroup(*[
            Line(
                [t, 1.2 - h, 0], [t, 1.2 + h, 0],
                color=pal.INPUT, stroke_width=4,
            )
            for t, h in zip(np.linspace(-2.9, 2.9, 49),
                            0.12 + 0.55 * np.abs(np.sin(np.linspace(0, 5 * np.pi, 49))))
        ])
        input4 = self.txt("spoken audio", 26, pal.INPUT).move_to(UP * 2.4)
        self.type_in(input4, run_time=0.8)
        self.play(Create(waveform4), run_time=1.3)
        arrow4 = Arrow(UP * 0.2, DOWN * 0.8, buff=0.06, color=pal.TEXT_DIM)
        self.play(GrowArrow(arrow4), run_time=0.6)

        word4a = self.txt("turn", 30, pal.OUTPUT)
        word4b = self.txt("left", 30, pal.OUTPUT)
        word4c = self.txt("now", 30, pal.OUTPUT)
        words4 = VGroup(word4a, word4b, word4c).arrange(RIGHT, buff=0.7).move_to(DOWN * 1.3)
        self.type_in(word4a, run_time=0.6)
        self.type_in(word4b, run_time=0.6)
        self.type_in(word4c, run_time=0.6)
        target4 = self.txt("target = sequence of words", 26, pal.OUTPUT).move_to(DOWN * 2.35)
        self.type_in(target4, run_time=1.2)
        self.wait(2.8)
        self.dust_wipe([title4, input4, waveform4, arrow4, word4a, word4b, word4c, target4])

        # 5. Dataset structures are useful conventions, not rigid categories.
        title5 = self.txt("Let the task shape the dataset", 30, pal.TEXT, BOLD)
        self.fit_width(title5, 7.8)
        title5.to_edge(UP, buff=0.6)
        self.type_in(title5, run_time=1.2)

        box5a = RoundedRectangle(width=6.9, height=1.0, corner_radius=0.12, color=pal.INPUT)
        box5b = box5a.copy().shift(DOWN * 1.4)
        box5c = box5a.copy().shift(DOWN * 2.8)
        box5a.move_to(UP * 1.5)
        box5b.move_to(UP * 0.1)
        box5c.move_to(DOWN * 1.3)
        text5a = self.txt("Fixed-size features → a matrix", 26, pal.TEXT).move_to(box5a)
        text5b = self.txt("Different sizes → a set of examples", 25, pal.TEXT).move_to(box5b)
        text5c = self.txt("Structured targets → sequences", 26, pal.TEXT).move_to(box5c)
        self.play(Create(box5a), run_time=0.6)
        self.type_in(text5a, run_time=1.2)
        self.play(Create(box5b), run_time=0.6)
        self.type_in(text5b, run_time=1.2)
        self.play(Create(box5c), run_time=0.6)
        self.type_in(text5c, run_time=1.2)
        note5 = self.txt("New applications can need new structures.", 25, pal.TEXT)
        self.fit_width(note5, 7.5)
        note5.move_to(DOWN * 2.8)
        self.type_in(note5, run_time=1.4)
        self.wait(2.5)
        self.dust_wipe([title5, box5a, box5b, box5c, text5a, text5b, text5c, note5])

        # 6. Section 5.1.4: the regression task maps a vector to a scalar.
        section6 = self.txt("5.1.4  Linear Regression", 31, pal.TEXT, BOLD)
        section6.to_edge(UP, buff=0.6)
        self.type_in(section6, run_time=1.2)
        intro6 = self.txt("A concrete learning algorithm", 26, pal.TEXT).move_to(UP * 2.45)
        self.type_in(intro6, run_time=1.1)

        input6 = self.formula(r"\mathbf{x}\in\mathbb{R}^{n}", 36, pal.INPUT).move_to(LEFT * 2.65 + UP * 0.25)
        model6 = RoundedRectangle(width=2.15, height=1.3, corner_radius=0.13, color=pal.FORMULA)
        model6.move_to(UP * 0.25)
        model_name6 = self.txt("linear\nmodel", 26, pal.FORMULA).move_to(model6)
        output6 = self.formula(r"\hat{y}\in\mathbb{R}", 36, pal.OUTPUT).move_to(RIGHT * 2.75 + UP * 0.25)
        arrow6a = Arrow(input6.get_right(), model6.get_left(), buff=0.15, color=pal.INPUT)
        arrow6b = Arrow(model6.get_right(), output6.get_left(), buff=0.15, color=pal.OUTPUT)
        self.play(Write(input6), run_time=0.8)
        self.play(GrowArrow(arrow6a), Create(model6), FadeIn(model_name6), run_time=1.0)
        self.play(GrowArrow(arrow6b), Write(output6), run_time=1.0)

        vector6 = self.txt("feature vector", 23, pal.INPUT).next_to(input6, DOWN, buff=0.5)
        scalar6 = self.txt("one number", 23, pal.OUTPUT).next_to(output6, DOWN, buff=0.5)
        self.play(FadeIn(vector6), FadeIn(scalar6), run_time=0.6)
        note6 = self.txt("Predict a numerical target y.\nŷ is the model's prediction.", 27, pal.TEXT).move_to(DOWN * 2.0)
        self.type_in(note6, run_time=1.5)
        self.wait(2.5)
        self.dust_wipe([section6, intro6, input6, model6, model_name6, output6, arrow6a, arrow6b, vector6, scalar6, note6])

        # 7. Equation (5.3): expand the dot product into a weighted sum.
        title7 = self.txt("The prediction is a weighted sum", 30, pal.TEXT, BOLD)
        self.fit_width(title7, 7.8)
        title7.to_edge(UP, buff=0.6)
        self.type_in(title7, run_time=1.2)

        equation7 = self.formula(r"{{\hat{y}}}={{\mathbf{w}}}^{\top}{{\mathbf{x}}}", 56, pal.FORMULA)
        equation7.set_color_by_tex(r"\hat{y}", pal.OUTPUT)
        equation7.set_color_by_tex(r"\mathbf{x}", pal.INPUT)
        equation7.move_to(UP * 1.9)
        number7 = self.txt("(5.3)", 23, pal.TEXT_DIM).next_to(equation7, RIGHT, buff=0.6)
        self.play(Write(equation7), FadeIn(number7), run_time=1.3)

        expanded7 = self.formula(r"\hat{y}=\sum_{j=1}^{n}w_jx_j", 43, pal.FORMULA)
        expanded7.move_to(UP * 0.25)
        self.play(Write(expanded7), run_time=1.3)
        roles7 = self.formula(r"\mathbf{x}\in\mathbb{R}^{n}\qquad\mathbf{w}\in\mathbb{R}^{n}", 35, pal.FORMULA)
        roles7.move_to(DOWN * 1.25)
        self.play(Write(roles7), run_time=1.0)
        explanation7 = self.txt("One weight per feature.\nMultiply, then add the contributions.", 26, pal.TEXT)
        explanation7.move_to(DOWN * 2.7)
        self.type_in(explanation7, run_time=1.6)
        self.wait(3.0)
        self.dust_wipe([title7, equation7, number7, expanded7, roles7, explanation7])

        # 8. A numerical dot product, without introducing a bias term.
        title8 = self.txt("Watch the contributions add up", 30, pal.TEXT, BOLD)
        self.fit_width(title8, 7.8)
        title8.to_edge(UP, buff=0.6)
        self.type_in(title8, run_time=1.2)

        x8 = self.formula(r"\mathbf{x}=(2,\ 3,\ 1)^{\top}", 36, pal.INPUT).move_to(UP * 2.4)
        w8 = self.formula(r"\mathbf{w}=(4,\ -1,\ 2)^{\top}", 36, pal.FORMULA).move_to(UP * 1.45)
        self.play(Write(x8), run_time=1.0)
        self.play(Write(w8), run_time=1.0)

        term8a = self.formula(r"4\times2", 37, pal.FORMULA).move_to(LEFT * 2.5 + UP * 0.05)
        term8b = self.formula(r"(-1)\times3", 37, pal.FORMULA).move_to(UP * 0.05)
        term8c = self.formula(r"2\times1", 37, pal.FORMULA).move_to(RIGHT * 2.5 + UP * 0.05)
        self.play(Write(term8a), run_time=0.6)
        self.play(Write(term8b), run_time=0.6)
        self.play(Write(term8c), run_time=0.6)

        result8a = self.formula(r"8", 44, pal.FORMULA).move_to(LEFT * 2.5 + DOWN * 1.1)
        result8b = self.formula(r"-3", 44, pal.FORMULA).move_to(DOWN * 1.1)
        result8c = self.formula(r"2", 44, pal.FORMULA).move_to(RIGHT * 2.5 + DOWN * 1.1)
        self.play(TransformFromCopy(term8a, result8a), TransformFromCopy(term8b, result8b), TransformFromCopy(term8c, result8c), run_time=1.2)
        sum8 = self.formula(r"\hat{y}=8-3+2=7", 46, pal.OUTPUT).move_to(DOWN * 2.55)
        self.play(Write(sum8), run_time=1.2)
        self.wait(3.0)
        self.dust_wipe([title8, x8, w8, term8a, term8b, term8c, result8a, result8b, result8c, sum8])

        # 9. Parameters control behavior; change w while holding x fixed.
        title9 = self.txt("Weights are the model's parameters", 30, pal.TEXT, BOLD)
        self.fit_width(title9, 7.8)
        title9.to_edge(UP, buff=0.6)
        self.type_in(title9, run_time=1.2)
        fixed9 = self.formula(r"\mathbf{x}=(2,\ 3,\ 1)^{\top}\quad\text{(fixed)}", 35, pal.INPUT).move_to(UP * 2.35)
        self.play(Write(fixed9), run_time=1.2)
        weights9 = self.formula(r"\mathbf{w}=(4,\ -1,\ 2)^{\top}", 38, pal.FORMULA).move_to(UP * 0.85)
        pred9 = self.formula(r"\hat{y}=7", 48, pal.OUTPUT).move_to(DOWN * 0.55)
        self.play(Write(weights9), Write(pred9), run_time=1.2)
        self.wait(1.5)

        new_weights9 = self.formula(r"\mathbf{w}=(4,\ +1,\ 2)^{\top}", 38, pal.FORMULA).move_to(weights9)
        new_pred9 = self.formula(r"\hat{y}=8+3+2=13", 48, pal.OUTPUT).move_to(pred9)
        self.play(Transform(weights9, new_weights9), Transform(pred9, new_pred9), run_time=1.5)
        caption9 = self.txt("Change a coefficient.\nChange the feature's contribution.", 27, pal.TEXT).move_to(DOWN * 2.15)
        self.type_in(caption9, run_time=1.5)
        self.wait(3.0)
        self.dust_wipe([title9, fixed9, weights9, pred9, caption9])

        # 10. One feature makes linearity visible: the weight sets the slope.
        title10 = self.txt("One feature: a line through the origin", 29, pal.TEXT, BOLD)
        self.fit_width(title10, 7.8)
        title10.to_edge(UP, buff=0.6)
        self.type_in(title10, run_time=1.2)
        formula10 = self.formula(r"n=1:\quad\hat{y}=wx", 37, pal.FORMULA).move_to(UP * 2.65)
        self.play(Write(formula10), run_time=1.0)

        axes10 = Axes(
            x_range=[0, 4, 1], y_range=[0, 8, 2], x_length=5.9, y_length=3.8,
            axis_config={"color": pal.TEXT_DIM, "stroke_width": 2, "include_tip": True},
        ).move_to(DOWN * 0.15)
        x_label10 = self.formula(r"x", 30, pal.INPUT).next_to(axes10.x_axis.get_end(), RIGHT, buff=0.15)
        y_label10 = self.formula(r"\hat{y}", 30, pal.OUTPUT).next_to(axes10.y_axis.get_end(), UP, buff=0.15)
        origin10 = self.mono("0", 23, pal.TEXT_DIM).next_to(axes10.c2p(0, 0), DL, buff=0.15)
        curve10 = axes10.plot(lambda x: x, x_range=[0, 3.6], color=pal.FORMULA, stroke_width=4)
        slope10 = self.formula(r"w=1", 31, pal.FORMULA).move_to(RIGHT * 1.7 + UP * 0.65)
        self.play(Create(axes10), Write(x_label10), Write(y_label10), FadeIn(origin10), run_time=1.2)
        self.play(Create(curve10), Write(slope10), run_time=1.2)
        self.wait(1.5)

        steeper10 = axes10.plot(lambda x: 2 * x, x_range=[0, 3.6], color=pal.FORMULA, stroke_width=4)
        new_slope10 = self.formula(r"w=2", 31, pal.FORMULA).move_to(LEFT * 0.1 + UP * 1.65)
        self.play(Transform(curve10, steeper10), Transform(slope10, new_slope10), run_time=1.5)
        note10 = self.txt("The weight controls the slope.", 26, pal.TEXT).move_to(DOWN * 3.0)
        self.type_in(note10, run_time=1.3)
        self.wait(2.5)
        self.dust_wipe([title10, formula10, axes10, x_label10, y_label10, origin10, curve10, slope10, note10])

        # 11. Keep the zoom duration at 1.0 s to match the music parser.
        final = self.txt("Linear regression turns features\ninto a prediction with a weighted sum.", 29, pal.TEXT, BOLD)
        self.fit_width(final, 7.6)
        final.move_to(ORIGIN)
        self.type_in(final, run_time=2.0)
        self.wait(0.5)
        line = Underline(final, color=pal.INPUT, stroke_width=3, buff=0.22)
        self.play(Create(line), run_time=0.6)
        self.zoom_pulse(final, zoom_scale=0.94, run_time_in=0.4, hold=0.2, run_time_out=0.4)
        self.wait(3.0)


if __name__ == "__main__":
    Page_105().render()
