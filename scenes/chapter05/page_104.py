from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.ml_shapes import dataset_table, matrix_grid


class Page_104(Chapter5Scene):

    PAGE_NO = "104"
    RNG_SEED = 71

    def construct(self):
        self.init_page()

        # ============================================================
        # SCENE 1 — THE ALTERNATIVE ROUTE: JOINT DISTRIBUTION
        # ============================================================

        title1 = self.txt("The other direction", 30, pal.TEXT, BOLD)
        title1.to_edge(UP, buff=0.6)
        self.type_in(title1, run_time=1.0)

        statement1 = self.txt("solve p(y | x) by learning the\nfull joint distribution p(x, y)", 18, pal.INPUT)
        statement1.next_to(title1, DOWN, buff=0.55)
        self.type_in(statement1, run_time=1.3)

        self.wait(1.0)
        self.dust_wipe([title1, statement1])

        # ============================================================
        # SCENE 2 — BAYES-STYLE INFERENCE FORMULA (5.2)
        # ============================================================

        title2 = self.txt("Infer p(y | x) from the joint", 27, pal.TEXT, BOLD)
        title2.to_edge(UP, buff=0.6)
        self.type_in(title2, run_time=1.0)

        formula2 = self.formula(
            r"p(y \mid \mathbf{x}) = \frac{p(\mathbf{x}, y)}{\sum_{y'} p(\mathbf{x}, y')}",
            32, pal.FORMULA,
        )
        formula2.next_to(title2, DOWN, buff=0.7)
        self.play(Write(formula2), run_time=1.3)

        eq_num2 = self.txt("(5.2)", 15, pal.TEXT_DIM)
        eq_num2.next_to(formula2, DOWN, buff=0.35)
        self.type_in(eq_num2, run_time=0.4)

        note2 = self.txt("normalize the joint by summing\nover all possible y values", 16, pal.TEXT)
        note2.next_to(eq_num2, DOWN, buff=0.5)
        self.type_in(note2, run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title2, formula2, eq_num2, note2])

        # ============================================================
        # SCENE 3 — TRADITIONAL CATEGORIZATION
        # ============================================================

        title3 = self.txt("The traditional split", 28, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        self.type_in(title3, run_time=1.0)

        sup_box = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=pal.OUTPUT, stroke_width=2.6)
        sup_box.next_to(title3, DOWN, buff=0.5)
        sup_label = self.txt("Supervised", 15, pal.OUTPUT, BOLD)
        sup_label.move_to(sup_box.get_center() + UP * 0.35)
        sup_text = self.txt("regression, classification,\nstructured output", 14, pal.TEXT)
        sup_text.move_to(sup_box.get_center() + DOWN * 0.3)

        self.play(Create(sup_box), run_time=0.6)
        self.type_in(sup_label, run_time=0.5)
        self.type_in(sup_text, run_time=0.9)

        unsup_box = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=pal.INPUT, stroke_width=2.6)
        unsup_box.next_to(sup_box, DOWN, buff=0.4)
        unsup_label = self.txt("Unsupervised", 15, pal.INPUT, BOLD)
        unsup_label.move_to(unsup_box.get_center() + UP * 0.35)
        unsup_text = self.txt("density estimation,\nin support of other tasks", 14, pal.TEXT)
        unsup_text.move_to(unsup_box.get_center() + DOWN * 0.3)

        self.play(Create(unsup_box), run_time=0.6)
        self.type_in(unsup_label, run_time=0.5)
        self.type_in(unsup_text, run_time=0.9)

        self.wait(1.1)
        self.dust_wipe([title3, sup_box, sup_label, sup_text, unsup_box, unsup_label, unsup_text])

        # ============================================================
        # SCENE 4 — OTHER LEARNING PARADIGMS: SEMI-SUPERVISED
        # ============================================================

        title4 = self.txt("Other paradigms exist", 28, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        self.type_in(title4, run_time=1.0)

        semi_box = RoundedRectangle(width=7.0, height=1.6, corner_radius=0.15, color=pal.DISTRIBUTION, stroke_width=2.6)
        semi_box.next_to(title4, DOWN, buff=0.6)
        semi_label = self.txt("Semi-supervised learning", 16, pal.DISTRIBUTION, BOLD)
        semi_label.move_to(semi_box.get_center() + UP * 0.35)
        semi_text = self.txt("some examples have a target,\nothers don't", 14, pal.TEXT)
        semi_text.move_to(semi_box.get_center() + DOWN * 0.3)

        self.play(Create(semi_box), run_time=0.7)
        self.type_in(semi_label, run_time=0.6)
        self.type_in(semi_text, run_time=0.9)

        self.wait(1.1)
        self.dust_wipe([title4, semi_box, semi_label, semi_text])

        # ============================================================
        # SCENE 5 — MULTI-INSTANCE LEARNING
        # ============================================================

        title5 = self.txt("Multi-instance learning", 27, pal.TEXT, BOLD)
        title5.to_edge(UP, buff=0.6)
        self.type_in(title5, run_time=1.0)

        bag = RoundedRectangle(width=5.0, height=2.0, corner_radius=0.16, color=pal.FORMULA, stroke_width=2.8)
        bag.next_to(title5, DOWN, buff=0.6)
        bag_label = self.txt("collection\n(labeled: contains class?)", 14, pal.FORMULA, BOLD)
        bag_label.move_to(bag.get_center() + UP * 0.6)

        members = VGroup(*[Dot(radius=0.07, color=pal.TEXT) for _ in range(6)])
        members.arrange_in_grid(rows=2, cols=3, buff=0.45)
        members.move_to(bag.get_center() + DOWN * 0.35)

        self.play(Create(bag), run_time=0.7)
        self.type_in(bag_label, run_time=1.0)
        self.play(FadeIn(members, lag_ratio=0.1), run_time=0.8)

        note5 = self.txt("individual members stay unlabeled", 16, pal.TEXT)
        note5.next_to(bag, DOWN, buff=0.5)
        self.type_in(note5, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title5, bag, bag_label, members, note5])

        # ============================================================
        # SCENE 6 — REINFORCEMENT LEARNING
        # ============================================================

        title6 = self.txt("Reinforcement learning", 28, pal.TEXT, BOLD)
        title6.to_edge(UP, buff=0.6)
        self.type_in(title6, run_time=1.0)

        agent_box = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.14, color=pal.INPUT, stroke_width=2.5)
        agent_box.move_to(LEFT * 2.0 + DOWN * 0.3)
        agent_label = self.txt("agent", 16, pal.INPUT, BOLD)
        agent_label.move_to(agent_box.get_center())

        env_box = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.14, color=pal.OUTPUT, stroke_width=2.5)
        env_box.move_to(RIGHT * 2.0 + DOWN * 0.3)
        env_label = self.txt("environment", 14, pal.OUTPUT, BOLD)
        env_label.move_to(env_box.get_center())

        arrow_right = Arrow(agent_box.get_right(), env_box.get_left(), color=pal.FORMULA, stroke_width=3, buff=0.1)
        arrow_right.shift(UP * 0.25)
        arrow_left = Arrow(env_box.get_left(), agent_box.get_right(), color=pal.FORMULA, stroke_width=3, buff=0.1)
        arrow_left.shift(DOWN * 0.25)

        self.play(Create(agent_box), run_time=0.6)
        self.play(FadeIn(agent_label), run_time=0.3)
        self.play(Create(env_box), run_time=0.6)
        self.play(FadeIn(env_label), run_time=0.3)
        self.play(GrowArrow(arrow_right), run_time=0.5)
        self.play(GrowArrow(arrow_left), run_time=0.5)

        note6 = self.txt("a feedback loop between the learner\nand its experience — beyond this book's scope", 15, pal.TEXT)
        note6.next_to(VGroup(agent_box, env_box), DOWN, buff=0.6)
        self.type_in(note6, run_time=1.2)

        self.wait(1.1)
        self.dust_wipe([title6, agent_box, agent_label, env_box, env_label, arrow_right, arrow_left, note6])

        # ============================================================
        # SCENE 7 — MOST ALGORITHMS: A FIXED DATASET
        # ============================================================

        title7 = self.txt("Back to the common case", 27, pal.TEXT, BOLD)
        title7.to_edge(UP, buff=0.6)
        self.type_in(title7, run_time=1.0)

        statement7 = self.txt("most algorithms simply experience\na fixed dataset", 18, pal.INPUT)
        statement7.next_to(title7, DOWN, buff=0.55)
        self.type_in(statement7, run_time=1.2)

        note7 = self.txt("a dataset = a collection of examples,\nwhich are collections of features", 16, pal.TEXT)
        note7.next_to(statement7, DOWN, buff=0.5)
        self.type_in(note7, run_time=1.2)

        self.wait(1.1)
        self.dust_wipe([title7, statement7, note7])

        # ============================================================
        # SCENE 8 — THE DESIGN MATRIX
        # ============================================================

        title8 = self.txt("The design matrix", 30, pal.TEXT, BOLD)
        title8.to_edge(UP, buff=0.6)
        self.type_in(title8, run_time=1.0)

        statement8 = self.txt("each row = one example\neach column = one feature", 18, pal.FORMULA)
        statement8.next_to(title8, DOWN, buff=0.5)
        self.type_in(statement8, run_time=1.2)

        matrix_vis = dataset_table(
            headers=["X·,1", "X·,2", "X·,3", "X·,4"],
            rows=[["5.1", "3.5", "1.4", "0.2"], ["7.0", "3.2", "4.7", "1.4"], ["6.3", "3.3", "6.0", "2.5"]],
            col_width=1.5, row_height=0.5, font_size=13,
        )
        matrix_vis.next_to(statement8, DOWN, buff=0.5)
        self.play(Create(matrix_vis), run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title8, statement8, matrix_vis])

        # ============================================================
        # SCENE 9 — THE IRIS DATASET AS A DESIGN MATRIX
        # ============================================================

        title9 = self.txt("Iris as a design matrix", 27, pal.TEXT, BOLD)
        title9.to_edge(UP, buff=0.6)
        self.type_in(title9, run_time=1.0)

        formula9 = self.formula(r"\mathbf{X} \in \mathbb{R}^{150 \times 4}", 32, pal.FORMULA)
        formula9.next_to(title9, DOWN, buff=0.6)
        self.play(Write(formula9), run_time=1.0)

        entry9 = self.formula(r"X_{i,1} = \text{sepal length of plant } i", 20, pal.TEXT)
        self.fit_width(entry9, 7.0)
        entry9.next_to(formula9, DOWN, buff=0.5)
        self.play(Write(entry9), run_time=1.1)

        entry9b = self.formula(r"X_{i,2} = \text{sepal width of plant } i", 20, pal.TEXT)
        self.fit_width(entry9b, 7.0)
        entry9b.next_to(entry9, DOWN, buff=0.3)
        self.play(Write(entry9b), run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title9, formula9, entry9, entry9b])

        # ============================================================
        # SCENE 10 — WHEN THE DESIGN MATRIX BREAKS DOWN
        # ============================================================

        title10 = self.txt("When it isn't possible", 27, pal.TEXT, BOLD)
        title10.to_edge(UP, buff=0.6)
        self.type_in(title10, run_time=1.0)

        statement10 = self.txt("every example must be describable\nas a vector of the SAME size", 18, pal.ERROR)
        statement10.next_to(title10, DOWN, buff=0.5)
        self.type_in(statement10, run_time=1.3)

        img1 = Square(side_length=1.2, stroke_color=pal.ERROR, stroke_width=2.4, fill_color=pal.ERROR, fill_opacity=0.12)
        img1.move_to(LEFT * 2.0 + DOWN * 1.6)
        img1_label = self.txt("200×300 px", 13, pal.ERROR)
        img1_label.next_to(img1, DOWN, buff=0.2)

        img2 = Rectangle(width=2.0, height=0.9, stroke_color=pal.ERROR, stroke_width=2.4, fill_color=pal.ERROR, fill_opacity=0.12)
        img2.move_to(RIGHT * 2.0 + DOWN * 1.6)
        img2_label = self.txt("640×480 px", 13, pal.ERROR)
        img2_label.next_to(img2, DOWN, buff=0.2)

        self.play(Create(img1), run_time=0.6)
        self.type_in(img1_label, run_time=0.5)
        self.play(Create(img2), run_time=0.6)
        self.type_in(img2_label, run_time=0.5)

        note10 = self.txt("different sizes → different pixel counts →\nno shared vector length", 14, pal.TEXT)
        note10.next_to(VGroup(img1, img2), DOWN, buff=0.5)
        self.type_in(note10, run_time=1.1)

        self.wait(1.2)
        self.dust_wipe([title10, statement10, img1, img1_label, img2, img2_label, note10])

        # ============================================================
        # SCENE 11 — FINAL MESSAGE
        # ============================================================

        final = self.txt(
            "A dataset is a table — until the examples\nrefuse to be the same shape.",
            21, pal.TEXT, BOLD,
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
    Page_104().render()
