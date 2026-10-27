from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal


class Page_108(Chapter5Scene):

    PAGE_NO = "108"
    RNG_SEED = 74

    def construct(self):
        self.init_page()

        # ============================================================
        # SCENE 1 — AFFINE FUNCTION AND BIAS
        # ============================================================

        title1 = self.txt(
            "Linear model, affine function",
            28, pal.TEXT, BOLD
        )
        title1.to_edge(UP, buff=0.6)
        self.type_in(title1, run_time=1.0)

        statement1 = self.txt(
            "adding the bias lets the line move away from the origin",
            17, pal.TEXT
        )
        statement1.next_to(title1, DOWN, buff=0.55)
        self.type_in(statement1, run_time=1.1)

        axes1 = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5.2,
            y_length=3.8,
            axis_config={
                "color": pal.TEXT_DIM,
                "stroke_width": 1.8,
            },
            tips=False,
        )
        axes1.move_to(DOWN * 0.7)

        origin_line = axes1.plot(
            lambda x: x,
            x_range=[-2.0, 2.0],
            color=pal.TEXT_DIM,
            stroke_width=2.2,
        )

        affine_line = axes1.plot(
            lambda x: x + 0.8,
            x_range=[-2.0, 2.0],
            color=pal.INPUT,
            stroke_width=3.2,
        )

        b_arrow = Arrow(
            axes1.c2p(0, 0),
            axes1.c2p(0, 0.8),
            color=pal.OUTPUT,
            stroke_width=2.8,
            buff=0.05,
        )

        b_label = self.formula(
            r"b",
            22,
            pal.OUTPUT,
        )
        b_label.next_to(b_arrow, RIGHT, buff=0.12)

        origin_label = self.txt(
            "without bias",
            14,
            pal.TEXT_DIM,
        )
        origin_label.next_to(
            axes1.c2p(1.55, 1.55),
            DOWN,
            buff=0.15,
        )

        affine_label = self.txt(
            "with bias",
            14,
            pal.INPUT,
        )
        affine_label.next_to(
            axes1.c2p(1.35, 2.15),
            RIGHT,
            buff=0.12,
        )

        self.play(Create(axes1), run_time=0.8)
        self.play(Create(origin_line), run_time=0.7)
        self.type_in(origin_label, run_time=0.5)

        self.play(Create(affine_line), run_time=0.8)
        self.type_in(affine_label, run_time=0.5)

        self.play(GrowArrow(b_arrow), run_time=0.6)
        self.type_in(b_label, run_time=0.5)

        self.wait(1.1)

        self.dust_wipe([
            title1,
            statement1,
            axes1,
            origin_line,
            affine_line,
            b_arrow,
            b_label,
            origin_label,
            affine_label,
        ])

        # ============================================================
        # SCENE 2 — BIAS AS AN EXTRA FEATURE
        # ============================================================

        title2 = self.txt(
            "The bias can be folded into the input",
            27,
            pal.TEXT,
            BOLD,
        )
        title2.to_edge(UP, buff=0.6)
        self.type_in(title2, run_time=1.0)

        formula2a = self.formula(
            r"\mathbf{x}\quad\longrightarrow\quad"
            r"\begin{bmatrix}\mathbf{x}\\1\end{bmatrix}",
            28,
            pal.FORMULA,
        )
        formula2a.next_to(title2, DOWN, buff=0.75)

        self.play(Write(formula2a), run_time=1.1)

        extra = self.txt(
            "add an extra feature that is always equal to 1",
            16,
            pal.TEXT,
        )
        extra.next_to(formula2a, DOWN, buff=0.55)
        self.type_in(extra, run_time=1.0)

        formula2b = self.formula(
            r"\mathbf{w}^{\mathsf T}\mathbf{x}+b"
            r"\quad\equiv\quad"
            r"\begin{bmatrix}\mathbf{w}\\b\end{bmatrix}^{\mathsf T}"
            r"\begin{bmatrix}\mathbf{x}\\1\end{bmatrix}",
            23,
            pal.INPUT,
        )
        self.fit_width(formula2b, 8.3)
        formula2b.next_to(extra, DOWN, buff=0.6)

        self.play(Write(formula2b), run_time=1.3)

        note2 = self.txt(
            "the weight attached to the extra 1 plays the role of b",
            15,
            pal.TEXT,
        )
        note2.next_to(formula2b, DOWN, buff=0.5)
        self.type_in(note2, run_time=1.0)

        self.wait(1.1)

        self.dust_wipe([
            title2,
            formula2a,
            extra,
            formula2b,
            note2,
        ])

        # ============================================================
        # SCENE 3 — TWO MEANINGS OF BIAS
        # ============================================================

        title3 = self.txt(
            "Two meanings of “bias”",
            28,
            pal.TEXT,
            BOLD,
        )
        title3.to_edge(UP, buff=0.6)
        self.type_in(title3, run_time=1.0)

        affine_box = RoundedRectangle(
            width=3.7,
            height=2.2,
            corner_radius=0.16,
            color=pal.OUTPUT,
            stroke_width=2.6,
        )
        affine_box.move_to(LEFT * 2.15 + DOWN * 0.35)

        affine_title = self.txt(
            "Bias parameter",
            17,
            pal.OUTPUT,
            BOLD,
        )
        affine_title.move_to(
            affine_box.get_center() + UP * 0.55
        )

        affine_text = self.txt(
            "intercept b\n"
            "shifts the affine function",
            14,
            pal.TEXT,
        )
        affine_text.move_to(
            affine_box.get_center() + DOWN * 0.25
        )

        stat_box = RoundedRectangle(
            width=3.7,
            height=2.2,
            corner_radius=0.16,
            color=pal.ERROR,
            stroke_width=2.6,
        )
        stat_box.move_to(RIGHT * 2.15 + DOWN * 0.35)

        stat_title = self.txt(
            "Statistical bias",
            17,
            pal.ERROR,
            BOLD,
        )
        stat_title.move_to(
            stat_box.get_center() + UP * 0.55
        )

        stat_text = self.txt(
            "systematic difference\n"
            "between estimate and truth",
            14,
            pal.TEXT,
        )
        stat_text.move_to(
            stat_box.get_center() + DOWN * 0.25
        )

        self.play(Create(affine_box), run_time=0.6)
        self.type_in(affine_title, run_time=0.5)
        self.type_in(affine_text, run_time=0.8)

        self.play(Create(stat_box), run_time=0.6)
        self.type_in(stat_title, run_time=0.5)
        self.type_in(stat_text, run_time=0.9)

        distinction = self.txt(
            "same word — different concepts",
            16,
            pal.TEXT_DIM,
            BOLD,
        )
        distinction.to_edge(DOWN, buff=0.6)
        self.type_in(distinction, run_time=0.8)

        self.wait(1.1)

        self.dust_wipe([
            title3,
            affine_box,
            affine_title,
            affine_text,
            stat_box,
            stat_title,
            stat_text,
            distinction,
        ])

        # ============================================================
        # SCENE 4 — LINEAR REGRESSION AS A SIMPLE EXAMPLE
        # ============================================================

        title4 = self.txt(
            "Why study such a simple algorithm?",
            27,
            pal.TEXT,
            BOLD,
        )
        title4.to_edge(UP, buff=0.6)
        self.type_in(title4, run_time=1.0)

        simple_box = RoundedRectangle(
            width=7.0,
            height=1.45,
            corner_radius=0.15,
            color=pal.FORMULA,
            stroke_width=2.5,
        )
        simple_box.next_to(title4, DOWN, buff=0.65)

        simple_text = self.txt(
            "Linear regression is simple and limited,\n"
            "but it exposes the basic mechanics of learning.",
            17,
            pal.FORMULA,
            BOLD,
        )
        simple_text.move_to(simple_box.get_center())

        self.play(Create(simple_box), run_time=0.7)
        self.type_in(simple_text, run_time=1.2)

        arrow4 = Arrow(
            simple_box.get_bottom(),
            simple_box.get_bottom() + DOWN * 1.0,
            color=pal.INPUT,
            stroke_width=3,
            buff=0.05,
        )

        next_text = self.txt(
            "optimization  →  generalization  →  learning algorithms",
            16,
            pal.INPUT,
        )
        next_text.next_to(arrow4, DOWN, buff=0.15)

        self.play(GrowArrow(arrow4), run_time=0.5)
        self.type_in(next_text, run_time=1.0)

        self.wait(1.1)

        self.dust_wipe([
            title4,
            simple_box,
            simple_text,
            arrow4,
            next_text,
        ])

        # ============================================================
        # SCENE 5 — CAPACITY / OVERFITTING / UNDERFITTING
        # ============================================================

        title5 = self.txt(
            "5.2  Capacity, Overfitting and Underfitting",
            26,
            pal.TEXT,
            BOLD,
        )
        title5.to_edge(UP, buff=0.55)
        self.type_in(title5, run_time=1.1)

        central = self.txt(
            "The central challenge in machine learning",
            21,
            pal.FORMULA,
            BOLD,
        )
        central.next_to(title5, DOWN, buff=0.75)
        self.type_in(central, run_time=1.0)

        train_box = RoundedRectangle(
            width=6.8,
            height=1.35,
            corner_radius=0.15,
            color=pal.INPUT,
            stroke_width=2.5,
        )
        train_box.next_to(central, DOWN, buff=0.6)

        train_text = self.txt(
            "perform well on the training examples",
            17,
            pal.INPUT,
            BOLD,
        )
        train_text.move_to(train_box.get_center())

        self.play(Create(train_box), run_time=0.6)
        self.type_in(train_text, run_time=0.9)

        unseen_box = RoundedRectangle(
            width=6.8,
            height=1.35,
            corner_radius=0.15,
            color=pal.OUTPUT,
            stroke_width=2.5,
        )
        unseen_box.next_to(train_box, DOWN, buff=0.45)

        unseen_text = self.txt(
            "AND perform well on new, unseen inputs",
            17,
            pal.OUTPUT,
            BOLD,
        )
        unseen_text.move_to(unseen_box.get_center())

        self.play(Create(unseen_box), run_time=0.6)
        self.type_in(unseen_text, run_time=1.0)

        self.wait(1.2)

        self.dust_wipe([
            title5,
            central,
            train_box,
            train_text,
            unseen_box,
            unseen_text,
        ])

        # ============================================================
        # SCENE 6 — GENERALIZATION
        # ============================================================

        title6 = self.txt(
            "Generalization",
            30,
            pal.TEXT,
            BOLD,
        )
        title6.to_edge(UP, buff=0.6)
        self.type_in(title6, run_time=1.0)

        definition = self.txt(
            "the ability to perform well on previously\n"
            "unobserved inputs",
            21,
            pal.FORMULA,
        )
        definition.next_to(title6, DOWN, buff=0.75)
        self.type_in(definition, run_time=1.2)

        train_label = self.txt(
            "TRAINING SET",
            14,
            pal.INPUT,
            BOLD,
        )
        train_label.move_to(LEFT * 2.7 + DOWN * 1.25)

        train_dots = VGroup(*[
            Dot(
                LEFT * 3.1 + RIGHT * i * 0.7 + DOWN * 1.75,
                radius=0.075,
                color=pal.INPUT,
            )
            for i in range(5)
        ])

        test_label = self.txt(
            "NEW INPUTS",
            14,
            pal.OUTPUT,
            BOLD,
        )
        test_label.move_to(RIGHT * 2.55 + DOWN * 1.25)

        test_dots = VGroup(
            Dot(
                RIGHT * 1.8 + DOWN * 1.75,
                radius=0.075,
                color=pal.OUTPUT,
            ),
            Dot(
                RIGHT * 2.55 + DOWN * 1.45,
                radius=0.075,
                color=pal.OUTPUT,
            ),
            Dot(
                RIGHT * 3.25 + DOWN * 1.85,
                radius=0.075,
                color=pal.OUTPUT,
            ),
        )

        arrow_generalize = Arrow(
            LEFT * 0.7 + DOWN * 1.65,
            RIGHT * 0.9 + DOWN * 1.65,
            color=pal.FORMULA,
            stroke_width=3,
            buff=0.05,
        )

        self.type_in(train_label, run_time=0.5)
        self.play(
            FadeIn(train_dots, lag_ratio=0.1),
            run_time=0.8,
        )

        self.play(
            GrowArrow(arrow_generalize),
            run_time=0.6,
        )

        self.type_in(test_label, run_time=0.5)
        self.play(
            FadeIn(test_dots, lag_ratio=0.1),
            run_time=0.7,
        )

        note6 = self.txt(
            "learning is not just memorizing the training set",
            16,
            pal.TEXT,
        )
        note6.to_edge(DOWN, buff=0.45)
        self.type_in(note6, run_time=0.9)

        self.wait(1.2)

        self.dust_wipe([
            title6,
            definition,
            train_label,
            train_dots,
            test_label,
            test_dots,
            arrow_generalize,
            note6,
        ])

        # ============================================================
        # SCENE 7 — TRAINING ERROR VS GENERALIZATION ERROR
        # ============================================================

        title7 = self.txt(
            "Training error is not enough",
            28,
            pal.TEXT,
            BOLD,
        )
        title7.to_edge(UP, buff=0.6)
        self.type_in(title7, run_time=1.0)

        train_error = RoundedRectangle(
            width=3.5,
            height=1.55,
            corner_radius=0.15,
            color=pal.INPUT,
            stroke_width=2.6,
        )
        train_error.move_to(LEFT * 2.1 + DOWN * 0.2)

        train_error_title = self.txt(
            "Training error",
            17,
            pal.INPUT,
            BOLD,
        )
        train_error_title.move_to(
            train_error.get_center() + UP * 0.35
        )

        train_error_text = self.txt(
            "error measured\n"
            "on training data",
            14,
            pal.TEXT,
        )
        train_error_text.move_to(
            train_error.get_center() + DOWN * 0.3
        )

        test_error = RoundedRectangle(
            width=3.5,
            height=1.55,
            corner_radius=0.15,
            color=pal.OUTPUT,
            stroke_width=2.6,
        )
        test_error.move_to(RIGHT * 2.1 + DOWN * 0.2)

        test_error_title = self.txt(
            "Generalization / test error",
            15,
            pal.OUTPUT,
            BOLD,
        )
        test_error_title.move_to(
            test_error.get_center() + UP * 0.35
        )

        test_error_text = self.txt(
            "expected error\n"
            "on new inputs",
            14,
            pal.TEXT,
        )
        test_error_text.move_to(
            test_error.get_center() + DOWN * 0.3
        )

        self.play(Create(train_error), run_time=0.6)
        self.type_in(train_error_title, run_time=0.5)
        self.type_in(train_error_text, run_time=0.8)

        self.play(Create(test_error), run_time=0.6)
        self.type_in(test_error_title, run_time=0.5)
        self.type_in(test_error_text, run_time=0.8)

        arrow7 = Arrow(
            train_error.get_right(),
            test_error.get_left(),
            color=pal.FORMULA,
            stroke_width=3,
            buff=0.12,
        )
        self.play(GrowArrow(arrow7), run_time=0.6)

        goal7 = self.txt(
            "A good model keeps BOTH errors low.",
            18,
            pal.FORMULA,
            BOLD,
        )
        goal7.next_to(
            VGroup(train_error, test_error),
            DOWN,
            buff=0.7,
        )
        self.type_in(goal7, run_time=1.0)

        self.wait(1.2)

        self.dust_wipe([
            title7,
            train_error,
            train_error_title,
            train_error_text,
            test_error,
            test_error_title,
            test_error_text,
            arrow7,
            goal7,
        ])

        # ============================================================
        # SCENE 8 — TEST SET
        # ============================================================

        title8 = self.txt(
            "How do we estimate generalization?",
            27,
            pal.TEXT,
            BOLD,
        )
        title8.to_edge(UP, buff=0.6)
        self.type_in(title8, run_time=1.0)

        train_set = RoundedRectangle(
            width=3.2,
            height=1.5,
            corner_radius=0.15,
            color=pal.INPUT,
            stroke_width=2.5,
        )
        train_set.move_to(LEFT * 2.25 + DOWN * 0.15)

        train_label8 = self.txt(
            "TRAINING SET",
            16,
            pal.INPUT,
            BOLD,
        )
        train_label8.move_to(
            train_set.get_center() + UP * 0.35
        )

        train_sub = self.txt(
            "used to fit the model",
            14,
            pal.TEXT,
        )
        train_sub.move_to(
            train_set.get_center() + DOWN * 0.3
        )

        test_set = RoundedRectangle(
            width=3.2,
            height=1.5,
            corner_radius=0.15,
            color=pal.OUTPUT,
            stroke_width=2.5,
        )
        test_set.move_to(RIGHT * 2.25 + DOWN * 0.15)

        test_label8 = self.txt(
            "TEST SET",
            16,
            pal.OUTPUT,
            BOLD,
        )
        test_label8.move_to(
            test_set.get_center() + UP * 0.35
        )

        test_sub = self.txt(
            "collected separately",
            14,
            pal.TEXT,
        )
        test_sub.move_to(
            test_set.get_center() + DOWN * 0.3
        )

        arrow8 = Arrow(
            train_set.get_right(),
            test_set.get_left(),
            color=pal.FORMULA,
            stroke_width=3,
            buff=0.12,
        )

        estimate = self.txt(
            "measure performance on the test set",
            18,
            pal.FORMULA,
            BOLD,
        )
        estimate.to_edge(DOWN, buff=0.6)

        self.play(Create(train_set), run_time=0.6)
        self.type_in(train_label8, run_time=0.5)
        self.type_in(train_sub, run_time=0.7)

        self.play(Create(test_set), run_time=0.6)
        self.type_in(test_label8, run_time=0.5)
        self.type_in(test_sub, run_time=0.7)

        self.play(GrowArrow(arrow8), run_time=0.6)
        self.type_in(estimate, run_time=0.9)

        self.wait(1.2)

        self.dust_wipe([
            title8,
            train_set,
            train_label8,
            train_sub,
            test_set,
            test_label8,
            test_sub,
            arrow8,
            estimate,
        ])

        # ============================================================
        # SCENE 9 — EQUATION 5.14
        # ============================================================

        title9 = self.txt(
            "Back to our linear regression example",
            26,
            pal.TEXT,
            BOLD,
        )
        title9.to_edge(UP, buff=0.6)
        self.type_in(title9, run_time=1.0)

        formula9 = self.formula(
            r"\frac{1}{m^{(\mathrm{train})}}"
            r"\left\|"
            r"\mathbf X^{(\mathrm{train})}\mathbf w"
            r"-\mathbf y^{(\mathrm{train})}"
            r"\right\|_2^2",
            29,
            pal.FORMULA,
        )
        formula9.next_to(title9, DOWN, buff=0.8)

        self.play(Write(formula9), run_time=1.3)

        eq9 = self.txt(
            "(5.14)",
            15,
            pal.TEXT_DIM,
        )
        eq9.next_to(formula9, RIGHT, buff=0.35)
        self.type_in(eq9, run_time=0.4)

        train_objective = self.txt(
            "training error",
            17,
            pal.INPUT,
            BOLD,
        )
        train_objective.next_to(
            formula9,
            DOWN,
            buff=0.6,
        )
        self.type_in(train_objective, run_time=0.8)

        brace = Brace(
            formula9,
            direction=DOWN,
            color=pal.INPUT,
        )

        brace_text = self.txt(
            "the quantity we minimized",
            15,
            pal.INPUT,
        )
        brace_text.next_to(
            brace,
            DOWN,
            buff=0.12,
        )

        self.play(Create(brace), run_time=0.5)
        self.type_in(brace_text, run_time=0.8)

        self.wait(1.1)

        self.dust_wipe([
            title9,
            formula9,
            eq9,
            train_objective,
            brace,
            brace_text,
        ])

        # ============================================================
        # SCENE 10 — CENTRAL PROBLEM
        # ============================================================

        title10 = self.txt(
            "The real problem",
            30,
            pal.TEXT,
            BOLD,
        )
        title10.to_edge(UP, buff=0.6)
        self.type_in(title10, run_time=1.0)

        train_formula = self.formula(
            r"\text{minimize training error}",
            25,
            pal.INPUT,
        )
        train_formula.move_to(
            LEFT * 2.1 + UP * 0.5
        )

        test_formula = self.formula(
            r"\text{also minimize test error}",
            25,
            pal.OUTPUT,
        )
        test_formula.move_to(
            RIGHT * 2.1 + UP * 0.5
        )

        self.play(
            Write(train_formula),
            run_time=0.9,
        )
        self.play(
            Write(test_formula),
            run_time=0.9,
        )

        connector10 = Arrow(
            train_formula.get_bottom(),
            test_formula.get_bottom(),
            color=pal.FORMULA,
            stroke_width=3,
            buff=0.15,
        )

        self.play(
            GrowArrow(connector10),
            run_time=0.6,
        )

        generalize = self.txt(
            "learning = low training error + low generalization error",
            18,
            pal.FORMULA,
            BOLD,
        )
        generalize.next_to(
            VGroup(train_formula, test_formula),
            DOWN,
            buff=0.8,
        )
        self.type_in(generalize, run_time=1.1)

        warning = self.txt(
            "This is where capacity, overfitting and underfitting matter.",
            16,
            pal.ERROR,
        )
        warning.to_edge(DOWN, buff=0.5)
        self.type_in(warning, run_time=1.0)

        self.wait(1.3)

        self.dust_wipe([
            title10,
            train_formula,
            test_formula,
            connector10,
            generalize,
            warning,
        ])

        # ============================================================
        # SCENE 11 — FINAL MESSAGE
        # ============================================================

        final = self.txt(
            "A model is useful only if it\n"
            "generalizes beyond its training data.",
            23,
            pal.TEXT,
            BOLD,
        )
        self.fit_width(final, 7.2)
        final.move_to(ORIGIN)

        self.type_in(final, run_time=1.5)

        line = Underline(
            final,
            color=pal.INPUT,
            stroke_width=3,
            buff=0.18,
        )
        self.play(Create(line), run_time=0.5)

        self.zoom_pulse(
            final,
            zoom_scale=0.93,
            run_time_in=0.8,
            hold=0.3,
            run_time_out=0.01,
        )

        self.wait(1.5)


if __name__ == "__main__":
    Page_108().render()
