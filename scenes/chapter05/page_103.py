from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.ml_shapes import dataset_table, matrix_grid


class Page_103(Chapter5Scene):

    PAGE_NO = "103"
    RNG_SEED = 61

    def construct(self):
        self.init_page()

        # ============================================================
        # SCENE 1 — WHAT IS A DATASET
        # ============================================================

        title1 = self.txt("The Experience: a dataset", 27, pal.TEXT, BOLD)
        title1.to_edge(UP, buff=0.6)
        self.type_in(title1, run_time=1.0)

        statement1 = self.txt("a collection of many examples\n(sometimes called data points)", 18, pal.INPUT)
        statement1.next_to(title1, DOWN, buff=0.55)
        self.type_in(statement1, run_time=1.3)

        dots = VGroup(*[Dot(radius=0.06, color=pal.INPUT) for _ in range(24)])
        dots.arrange_in_grid(rows=4, cols=6, buff=0.4)
        dots.next_to(statement1, DOWN, buff=0.6)
        self.play(FadeIn(dots, lag_ratio=0.05), run_time=1.0)

        self.wait(1.0)
        self.dust_wipe([title1, statement1, dots])

        # ============================================================
        # SCENE 2 — THE IRIS DATASET
        # ============================================================

        title2 = self.txt("Example: the Iris dataset", 27, pal.TEXT, BOLD)
        title2.to_edge(UP, buff=0.6)
        self.type_in(title2, run_time=1.0)

        subtitle2 = self.txt("Fisher (1936) — one of the oldest\ndatasets in statistics", 16, pal.TEXT_DIM)
        subtitle2.next_to(title2, DOWN, buff=0.4)
        self.type_in(subtitle2, run_time=1.1)

        table = dataset_table(
            headers=["sepal L", "sepal W", "species"],
            rows=[["5.1", "3.5", "setosa"], ["7.0", "3.2", "versicolor"], ["6.3", "3.3", "virginica"]],
            col_width=1.9, row_height=0.5, font_size=13,
        )
        table.next_to(subtitle2, DOWN, buff=0.5)
        self.play(Create(table), run_time=1.2)

        note2 = self.txt("150 plants, 3 species,\n4 measurements each", 15, pal.TEXT)
        note2.next_to(table, DOWN, buff=0.4)
        self.type_in(note2, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title2, subtitle2, table, note2])

        # ============================================================
        # SCENE 3 — FEATURES OF THE IRIS DATASET
        # ============================================================

        title3 = self.txt("One example = one plant", 27, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        self.type_in(title3, run_time=1.0)

        vec3 = matrix_grid(
            ["sepal\nL", "sepal\nW", "petal\nL", "petal\nW"],
            cell_size=1.1, font_size=14,
        )
        vec3.next_to(title3, DOWN, buff=0.7)
        self.play(FadeIn(vec3, lag_ratio=0.1), run_time=1.0)

        note3 = self.txt("the features = measurements of each part", 17, pal.TEXT)
        note3.next_to(vec3, DOWN, buff=0.5)
        self.type_in(note3, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title3, vec3, note3])

        # ============================================================
        # SCENE 4 — UNSUPERVISED LEARNING
        # ============================================================

        title4 = self.txt("Unsupervised learning", 30, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        self.type_in(title4, run_time=1.0)

        statement4 = self.txt("experience features — learn useful\nproperties of the dataset's structure", 17, pal.INPUT)
        statement4.next_to(title4, DOWN, buff=0.5)
        self.type_in(statement4, run_time=1.3)

        goal4 = self.formula(r"\text{learn } p(\mathbf{x})", 28, pal.DISTRIBUTION)
        goal4.next_to(statement4, DOWN, buff=0.5)
        self.play(Write(goal4), run_time=0.9)

        note4 = self.txt("explicitly (density estimation) or\nimplicitly (synthesis, denoising)", 15, pal.TEXT)
        note4.next_to(goal4, DOWN, buff=0.4)
        self.type_in(note4, run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title4, statement4, goal4, note4])

        # ============================================================
        # SCENE 5 — CLUSTERING EXAMPLE
        # ============================================================

        title5 = self.txt("Example: clustering", 28, pal.TEXT, BOLD)
        title5.to_edge(UP, buff=0.6)
        self.type_in(title5, run_time=0.9)

        axes5 = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=6.2, y_length=4.2,
            axis_config={"color": pal.TEXT_DIM, "stroke_width": 1.2, "include_numbers": False},
        )
        axes5.next_to(title5, DOWN, buff=0.5)

        import random as _r
        _r.seed(9)
        cluster_a = VGroup(*[Dot(axes5.c2p(_r.gauss(2.5, 0.6), _r.gauss(2.5, 0.6)), radius=0.05, color=pal.INPUT) for _ in range(12)])
        cluster_b = VGroup(*[Dot(axes5.c2p(_r.gauss(7, 0.6), _r.gauss(7, 0.6)), radius=0.05, color=pal.OUTPUT) for _ in range(12)])
        cluster_c = VGroup(*[Dot(axes5.c2p(_r.gauss(7, 0.6), _r.gauss(2.5, 0.6)), radius=0.05, color=pal.ACCENT_1) for _ in range(12)])

        self.play(Create(axes5), run_time=0.6)
        self.play(FadeIn(cluster_a, lag_ratio=0.08), FadeIn(cluster_b, lag_ratio=0.08), FadeIn(cluster_c, lag_ratio=0.08), run_time=1.1)

        note5 = self.txt("dividing the dataset into\nclusters of similar examples", 16, pal.TEXT)
        note5.next_to(axes5, DOWN, buff=0.4)
        self.type_in(note5, run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title5, axes5, cluster_a, cluster_b, cluster_c, note5])

        # ============================================================
        # SCENE 6 — SUPERVISED LEARNING
        # ============================================================

        title6 = self.txt("Supervised learning", 30, pal.TEXT, BOLD)
        title6.to_edge(UP, buff=0.6)
        self.type_in(title6, run_time=1.0)

        statement6 = self.txt("each example also comes with a\nlabel or target", 18, pal.OUTPUT)
        statement6.next_to(title6, DOWN, buff=0.5)
        self.type_in(statement6, run_time=1.2)

        pair6 = VGroup(
            self.formula(r"\mathbf{x}", 30, pal.INPUT),
            self.txt("→", 24, pal.TEXT),
            self.formula(r"\mathbf{y}", 30, pal.OUTPUT),
        ).arrange(RIGHT, buff=0.4)
        pair6.next_to(statement6, DOWN, buff=0.55)
        self.play(Write(pair6), run_time=1.0)

        note6 = self.txt("Iris: measurements → species label", 16, pal.TEXT)
        note6.next_to(pair6, DOWN, buff=0.4)
        self.type_in(note6, run_time=1.0)

        self.wait(1.1)
        self.dust_wipe([title6, statement6, pair6, note6])

        # ============================================================
        # SCENE 7 — THE TWO GOALS SIDE BY SIDE
        # ============================================================

        title7 = self.txt("Two different goals", 29, pal.TEXT, BOLD)
        title7.to_edge(UP, buff=0.6)
        self.type_in(title7, run_time=1.0)

        unsup_box = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.15, color=pal.INPUT, stroke_width=2.6)
        unsup_box.move_to(LEFT * 2.0 + DOWN * 0.3)
        unsup_title = self.txt("Unsupervised", 15, pal.INPUT, BOLD)
        unsup_title.move_to(unsup_box.get_center() + UP * 0.6)
        unsup_formula = self.formula(r"p(\mathbf{x})", 24, pal.INPUT)
        unsup_formula.move_to(unsup_box.get_center() + DOWN * 0.3)

        sup_box = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.15, color=pal.OUTPUT, stroke_width=2.6)
        sup_box.move_to(RIGHT * 2.0 + DOWN * 0.3)
        sup_title = self.txt("Supervised", 15, pal.OUTPUT, BOLD)
        sup_title.move_to(sup_box.get_center() + UP * 0.6)
        sup_formula = self.formula(r"p(\mathbf{y} \mid \mathbf{x})", 24, pal.OUTPUT)
        sup_formula.move_to(sup_box.get_center() + DOWN * 0.3)

        self.play(Create(unsup_box), run_time=0.6)
        self.type_in(unsup_title, run_time=0.5)
        self.play(Write(unsup_formula), run_time=0.7)

        self.play(Create(sup_box), run_time=0.6)
        self.type_in(sup_title, run_time=0.5)
        self.play(Write(sup_formula), run_time=0.7)

        self.wait(1.1)
        self.dust_wipe([title7, unsup_box, unsup_title, unsup_formula, sup_box, sup_title, sup_formula])

        # ============================================================
        # SCENE 8 — THE TEACHER METAPHOR
        # ============================================================

        title8 = self.txt("Where \"supervised\" comes from", 25, pal.TEXT, BOLD)
        title8.to_edge(UP, buff=0.6)
        self.type_in(title8, run_time=1.0)

        sup_metaphor = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=pal.OUTPUT, stroke_width=2.5)
        sup_metaphor.next_to(title8, DOWN, buff=0.5)
        sup_metaphor_text = self.txt("y is provided by an instructor\nwho shows the system what to do", 15, pal.TEXT)
        sup_metaphor_text.move_to(sup_metaphor.get_center())

        self.play(Create(sup_metaphor), run_time=0.6)
        self.type_in(sup_metaphor_text, run_time=1.1)

        unsup_metaphor = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=pal.INPUT, stroke_width=2.5)
        unsup_metaphor.next_to(sup_metaphor, DOWN, buff=0.4)
        unsup_metaphor_text = self.txt("no instructor — the algorithm must\nmake sense of the data alone", 15, pal.TEXT)
        unsup_metaphor_text.move_to(unsup_metaphor.get_center())

        self.play(Create(unsup_metaphor), run_time=0.6)
        self.type_in(unsup_metaphor_text, run_time=1.1)

        self.wait(1.1)
        self.dust_wipe([title8, sup_metaphor, sup_metaphor_text, unsup_metaphor, unsup_metaphor_text])

        # ============================================================
        # SCENE 9 — THE LINE IS BLURRY
        # ============================================================

        title9 = self.txt("Not a rigid distinction", 28, pal.TEXT, BOLD)
        title9.to_edge(UP, buff=0.6)
        self.type_in(title9, run_time=1.0)

        statement9 = self.txt(
            "unsupervised and supervised are not\nformally defined — the line is often blurred",
            17, pal.FORMULA,
        )
        statement9.next_to(title9, DOWN, buff=0.55)
        self.type_in(statement9, run_time=1.3)

        self.wait(1.0)
        self.dust_wipe([title9, statement9])

        # ============================================================
        # SCENE 10 — CHAIN RULE: ONE DISTRIBUTION, MANY FACTORS
        # ============================================================

        title10 = self.txt("The chain rule connects them", 26, pal.TEXT, BOLD)
        title10.to_edge(UP, buff=0.6)
        self.type_in(title10, run_time=1.0)

        chain_formula = self.formula(
            r"p(\mathbf{x}) = \prod_{i=1}^{n} p(\mathrm{x}_i \mid \mathrm{x}_1, \ldots, \mathrm{x}_{i-1})",
            28, pal.FORMULA,
        )
        chain_formula.next_to(title10, DOWN, buff=0.6)
        self.play(Write(chain_formula), run_time=1.3)

        eq_num10 = self.txt("(5.1)", 14, pal.TEXT_DIM)
        eq_num10.next_to(chain_formula, DOWN, buff=0.3)
        self.type_in(eq_num10, run_time=0.4)

        note10 = self.txt("an unsupervised p(x) can be decomposed\ninto a series of supervised problems", 16, pal.TEXT)
        note10.next_to(eq_num10, DOWN, buff=0.45)
        self.type_in(note10, run_time=1.2)

        self.wait(1.2)
        self.dust_wipe([title10, chain_formula, eq_num10, note10])

        # ============================================================
        # SCENE 11 — FINAL MESSAGE
        # ============================================================

        final = self.txt(
            "Supervised or unsupervised —\nboth are shaped by one underlying p(x).",
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
    Page_103().render()
