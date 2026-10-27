from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.ml_shapes import loss_curve, matrix_grid


class Page_102(Chapter5Scene):

    PAGE_NO = "102"
    RNG_SEED = 51

    def construct(self):
        self.init_page()

        # ============================================================
        # SCENE 1 — ACCURACY VS ERROR RATE
        # ============================================================

        title1 = self.txt("Accuracy vs. error rate", 30, pal.TEXT, BOLD)
        title1.to_edge(UP, buff=0.6)
        self.type_in(title1, run_time=1.0)

        acc_box = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.15,
                                    color=pal.OUTPUT, stroke_width=2.6)
        acc_box.move_to(LEFT * 2.0 + DOWN * 0.3)
        acc_label = self.txt("accuracy", 17, pal.OUTPUT, BOLD)
        acc_label.move_to(acc_box.get_center() + UP * 0.35)
        acc_text = self.txt("% correct", 14, pal.TEXT)
        acc_text.move_to(acc_box.get_center() + DOWN * 0.3)

        vs_label = self.txt("=", 24, pal.TEXT)
        vs_label.move_to(DOWN * 0.3)

        err_box = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.15,
                                    color=pal.ERROR, stroke_width=2.6)
        err_box.move_to(RIGHT * 2.3 + DOWN * 0.3)
        err_label = self.txt("error rate", 17, pal.ERROR, BOLD)
        err_label.move_to(err_box.get_center() + UP * 0.35)
        err_text = self.txt("1 − accuracy", 14, pal.TEXT)
        err_text.move_to(err_box.get_center() + DOWN * 0.3)

        self.play(Create(acc_box), run_time=0.6)
        self.type_in(acc_label, run_time=0.6)
        self.type_in(acc_text, run_time=0.6)
        self.type_in(vs_label, run_time=0.3)
        self.play(Create(err_box), run_time=0.6)
        self.type_in(err_label, run_time=0.6)
        self.type_in(err_text, run_time=0.6)

        note1 = self.txt("equivalent information, opposite framing", 16, pal.TEXT_DIM)
        note1.next_to(VGroup(acc_box, err_box), DOWN, buff=0.6)
        self.type_in(note1, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title1, acc_box, acc_label, acc_text, vs_label, err_box, err_label, err_text, note1])

        # ============================================================
        # SCENE 2 — THE 0-1 LOSS
        # ============================================================

        title2 = self.txt("The 0-1 loss", 32, pal.TEXT, BOLD)
        title2.to_edge(UP, buff=0.6)
        self.type_in(title2, run_time=0.9)

        loss_formula = self.formula(
            r"\text{loss} = \begin{cases} 0 & \text{correct} \\ 1 & \text{incorrect} \end{cases}",
            28, pal.FORMULA,
        )
        loss_formula.next_to(title2, DOWN, buff=0.6)
        self.play(Write(loss_formula), run_time=1.1)

        note2 = self.txt("error rate = the expected 0-1 loss", 17, pal.TEXT)
        note2.next_to(loss_formula, DOWN, buff=0.5)
        self.type_in(note2, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title2, loss_formula, note2])

        # ============================================================
        # SCENE 3 — WHEN 0-1 LOSS DOESN'T MAKE SENSE: DENSITY ESTIMATION
        # ============================================================

        title3 = self.txt("When 0-1 loss breaks down", 27, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        self.type_in(title3, run_time=1.0)

        de_box = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15,
                                   color=pal.DISTRIBUTION, stroke_width=2.6)
        de_box.next_to(title3, DOWN, buff=0.6)
        de_text = self.txt("density estimation has no single\n\"correct\" discrete answer", 17, pal.TEXT)
        de_text.move_to(de_box.get_center())

        self.play(Create(de_box), run_time=0.7)
        self.type_in(de_text, run_time=1.1)

        note3 = self.txt("need a continuous-valued score instead", 17, pal.FORMULA)
        note3.next_to(de_box, DOWN, buff=0.5)
        self.type_in(note3, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title3, de_box, de_text, note3])

        # ============================================================
        # SCENE 4 — THE FIX: AVERAGE LOG-PROBABILITY
        # ============================================================

        title4 = self.txt("The usual fix: average log-probability", 23, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        self.type_in(title4, run_time=1.1)

        logp_formula = self.formula(r"\frac{1}{m}\sum_i \log p_{\text{model}}(x^{(i)})", 28, pal.FORMULA)
        logp_formula.next_to(title4, DOWN, buff=0.65)
        self.play(Write(logp_formula), run_time=1.1)

        note4 = self.txt("the model's own assigned probability\nbecomes the continuous score", 16, pal.TEXT)
        note4.next_to(logp_formula, DOWN, buff=0.5)
        self.type_in(note4, run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title4, logp_formula, note4])

        # ============================================================
        # SCENE 5 — EVALUATE ON UNSEEN DATA: THE TEST SET
        # ============================================================

        title5 = self.txt("Evaluate on unseen data", 28, pal.TEXT, BOLD)
        title5.to_edge(UP, buff=0.6)
        self.type_in(title5, run_time=1.0)

        statement5 = self.txt("what matters: performance on data\nthe model has NOT seen before", 18, pal.INPUT)
        statement5.next_to(title5, DOWN, buff=0.5)
        self.type_in(statement5, run_time=1.3)

        train_box = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.14,
                                      color=pal.OUTPUT, stroke_width=2.4)
        train_box.move_to(LEFT * 1.9 + DOWN * 1.9)
        train_label = self.txt("training set", 15, pal.OUTPUT, BOLD)
        train_label.move_to(train_box.get_center())

        test_box = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.14,
                                     color=pal.ERROR, stroke_width=2.4)
        test_box.move_to(RIGHT * 1.9 + DOWN * 1.9)
        test_label = self.txt("test set", 15, pal.ERROR, BOLD)
        test_label.move_to(test_box.get_center())

        self.play(Create(train_box), run_time=0.5)
        self.type_in(train_label, run_time=0.5)
        self.play(Create(test_box), run_time=0.5)
        self.type_in(test_label, run_time=0.5)

        note5 = self.txt("separate data, used only for evaluation", 15, pal.TEXT_DIM)
        note5.next_to(VGroup(train_box, test_box), DOWN, buff=0.4)
        self.type_in(note5, run_time=0.9)

        self.wait(1.1)
        self.dust_wipe([title5, statement5, train_box, train_label, test_box, test_label, note5])

        # ============================================================
        # SCENE 6 — CHOOSING A PERFORMANCE MEASURE IS HARD
        # ============================================================

        title6 = self.txt("Choosing the right measure is hard", 23, pal.TEXT, BOLD)
        title6.to_edge(UP, buff=0.6)
        self.type_in(title6, run_time=1.1)

        statement6 = self.txt(
            "objective-sounding, but rarely\nstraightforward to design well",
            18, pal.ERROR,
        )
        statement6.next_to(title6, DOWN, buff=0.55)
        self.type_in(statement6, run_time=1.3)

        self.wait(1.0)
        self.dust_wipe([title6, statement6])

        # ============================================================
        # SCENE 7 — EXAMPLE: TRANSCRIPTION GRANULARITY
        # ============================================================

        title7 = self.txt("Example: how fine-grained?", 27, pal.TEXT, BOLD)
        title7.to_edge(UP, buff=0.6)
        self.type_in(title7, run_time=1.0)

        q1_box = RoundedRectangle(width=7.0, height=1.6, corner_radius=0.15,
                                   color=pal.INPUT, stroke_width=2.5)
        q1_box.next_to(title7, DOWN, buff=0.5)
        q1_text = self.txt("transcription: whole-sequence accuracy,\nor partial credit per element?", 16, pal.TEXT)
        q1_text.move_to(q1_box.get_center())

        self.play(Create(q1_box), run_time=0.6)
        self.type_in(q1_text, run_time=1.2)

        q2_box = RoundedRectangle(width=7.0, height=1.6, corner_radius=0.15,
                                   color=pal.DISTRIBUTION, stroke_width=2.5)
        q2_box.next_to(q1_box, DOWN, buff=0.4)
        q2_text = self.txt("regression: penalize frequent\nmedium errors, or rare large ones?", 16, pal.TEXT)
        q2_text.move_to(q2_box.get_center())

        self.play(Create(q2_box), run_time=0.6)
        self.type_in(q2_text, run_time=1.2)

        note7 = self.txt("these design choices depend on the application", 14, pal.TEXT_DIM)
        note7.next_to(q2_box, DOWN, buff=0.4)
        self.type_in(note7, run_time=1.0)

        self.wait(1.2)
        self.dust_wipe([title7, q1_box, q1_text, q2_box, q2_text, note7])

        # ============================================================
        # SCENE 8 — WHEN THE IDEAL MEASURE IS INTRACTABLE
        # ============================================================

        title8 = self.txt("Sometimes the ideal measure\nis intractable", 24, pal.TEXT, BOLD)
        title8.to_edge(UP, buff=0.6)
        self.type_in(title8, run_time=1.2)

        curve_vis = loss_curve(
            x_range=(0, 10, 2), y_range=(0, 1, 0.25),
            width=6.2, height=2.6, color=pal.DISTRIBUTION,
            x_label="", y_label="p(x)",
        )
        curve_vis.next_to(title8, DOWN, buff=0.5)
        self.play(Create(curve_vis.axes), run_time=0.5)
        self.play(Create(curve_vis.curve), run_time=0.9)

        note8 = self.txt(
            "many good probabilistic models represent\np(x) only implicitly — can't compute it exactly",
            15, pal.TEXT,
        )
        self.fit_width(note8, 6.9)
        note8.next_to(curve_vis, DOWN, buff=0.4)
        self.type_in(note8, run_time=1.2)

        self.wait(1.1)
        self.dust_wipe([title8, curve_vis, note8])

        # ============================================================
        # SCENE 9 — THE WORKAROUND
        # ============================================================

        title9 = self.txt("The workaround", 30, pal.TEXT, BOLD)
        title9.to_edge(UP, buff=0.6)
        self.type_in(title9, run_time=0.9)

        workaround_box = RoundedRectangle(width=7.0, height=1.8, corner_radius=0.16,
                                           color=pal.FORMULA, stroke_width=2.6)
        workaround_box.next_to(title9, DOWN, buff=0.6)
        workaround_text = self.txt(
            "design an alternative criterion that still\nmatches the goal, or approximate it well",
            17, pal.TEXT,
        )
        workaround_text.move_to(workaround_box.get_center())

        self.play(Create(workaround_box), run_time=0.7)
        self.type_in(workaround_text, run_time=1.2)

        self.wait(1.1)
        self.dust_wipe([title9, workaround_box, workaround_text])

        # ============================================================
        # SCENE 10 — 5.1.3 THE EXPERIENCE, E
        # ============================================================

        title10 = self.txt("5.1.3  The Experience, E", 28, pal.TEXT, BOLD)
        title10.to_edge(UP, buff=0.6)
        self.type_in(title10, run_time=1.1)

        split_box = VGroup(
            RoundedRectangle(width=3.0, height=1.4, corner_radius=0.14, color=pal.INPUT, stroke_width=2.5),
            RoundedRectangle(width=3.0, height=1.4, corner_radius=0.14, color=pal.OUTPUT, stroke_width=2.5),
        ).arrange(RIGHT, buff=0.6)
        split_box.next_to(title10, DOWN, buff=0.7)

        unsup_label = self.txt("unsupervised", 16, pal.INPUT, BOLD)
        unsup_label.move_to(split_box[0].get_center())
        sup_label = self.txt("supervised", 16, pal.OUTPUT, BOLD)
        sup_label.move_to(split_box[1].get_center())

        self.play(Create(split_box[0]), run_time=0.6)
        self.type_in(unsup_label, run_time=0.6)
        self.play(Create(split_box[1]), run_time=0.6)
        self.type_in(sup_label, run_time=0.6)

        note10 = self.txt("categorized by what kind of experience\nthe algorithm is allowed during learning", 16, pal.TEXT)
        note10.next_to(split_box, DOWN, buff=0.55)
        self.type_in(note10, run_time=1.2)

        self.wait(1.2)
        self.dust_wipe([title10, split_box, unsup_label, sup_label, note10])

        # ============================================================
        # SCENE 11 — FINAL MESSAGE
        # ============================================================

        final = self.txt(
            "Measuring performance well is its own\ndesign problem — not an afterthought.",
            22, pal.TEXT, BOLD,
        )
        self.fit_width(final, 7.2)
        final.move_to(ORIGIN)

        self.type_in(final, run_time=1.6)
        self.wait(0.3)

        line = Underline(final, color=pal.INPUT, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.zoom_pulse(final, zoom_scale=0.92, run_time_in=0.8, hold=0.3, run_time_out=0.01)
        self.wait(1.5)


if __name__ == "__main__":
    Page_102().render()
