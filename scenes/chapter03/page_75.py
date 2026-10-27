import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_75(Scene):

    def construct(self):

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"
        PURPLE = "#C58CFF"

        self.camera.background_color = BG

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(text, font="DejaVu Sans", font_size=size, color=color, weight=weight)

        def show(obj, time=0.7):
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(*[FadeOut(obj) for obj in list(self.mobjects)], run_time=0.5)
            self.wait(0.3)

        def node(label, color=CYAN, radius=0.5):
            circle = Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.15, stroke_width=3)
            label_obj = txt(label, 26, WHITE, BOLD)
            label_obj.move_to(circle.get_center())
            return VGroup(circle, label_obj)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("3.14  Structured Probabilistic Models", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — SPLITTING INTO FACTORS
        # ============================================================

        title = txt("Split one big function into many factors", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        single_box = titled_box(
            "Single function",
            txt("p(a, b, c)\none huge joint table", 17, RED),
            chapter="chapter03", width=6.5, height=1.9,
        )
        single_box[0].set_stroke(color=RED, width=3)
        single_box.next_to(title, DOWN, buff=0.7)
        fit_in_frame(single_box, margin=0.9)
        show(single_box, 1.0)

        arrow_down = txt("↓", 34, MUTED)
        arrow_down.next_to(single_box, DOWN, buff=0.25)
        show(arrow_down, 0.4)

        factored_box = titled_box(
            "Factored form",
            txt("p(a) · p(b|a) · p(c|b)\nsmaller, cheaper pieces", 17, GREEN),
            chapter="chapter03", width=6.5, height=1.9,
        )
        factored_box[0].set_stroke(color=GREEN, width=3)
        factored_box.next_to(arrow_down, DOWN, buff=0.25)
        fit_in_frame(factored_box, margin=0.9)
        show(factored_box, 1.0)

        self.wait(1.4)
        clear_scene()

        # ============================================================
        # SCENE 3 — EXAMPLE GRAPH: a -> b -> c
        # ============================================================

        title = txt("Example: a influences b, b influences c", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        node_a = node("a", CYAN)
        node_b = node("b", YELLOW)
        node_c = node("c", GREEN)

        graph_row = flow_row([node_a, node_b, node_c], buff=2.2)
        graph_row.next_to(title, DOWN, buff=1.0)

        edge_ab = smart_arrow(node_a, node_b, color=WHITE)
        edge_bc = smart_arrow(node_b, node_c, color=WHITE)

        staggered_fade_in(self, [node_a, node_b, node_c], run_time=1.1, lag_ratio=0.3)
        self.play(Create(edge_ab), Create(edge_bc), run_time=0.9)

        indep_note = txt("a and c are independent given b", 18, MUTED)
        indep_note.next_to(graph_row, DOWN, buff=0.7)
        fit_in_frame(indep_note, margin=1.0)
        show(indep_note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — FACTORIZATION FORMULA (3.52)
        # ============================================================

        title = txt("Factorizing the joint distribution", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"p(\mathrm{a}, \mathrm{b}, \mathrm{c}) = p(\mathrm{a})\,p(\mathrm{b} \mid \mathrm{a})\,p(\mathrm{c} \mid \mathrm{b})",
            font_size=32, color=YELLOW,
        )
        formula.next_to(title, DOWN, buff=0.7)
        show(formula, 1.1)

        eq_num = txt("(3.52)", 18, MUTED)
        eq_num.next_to(formula, DOWN, buff=0.3)
        show(eq_num, 0.4)

        node_a2 = node("a", CYAN, radius=0.4)
        node_b2 = node("b", YELLOW, radius=0.4)
        node_c2 = node("c", GREEN, radius=0.4)
        mini_row = flow_row([node_a2, node_b2, node_c2], buff=1.6)
        mini_row.next_to(eq_num, DOWN, buff=0.6)
        edge1 = smart_arrow(node_a2, node_b2, color=WHITE)
        edge2 = smart_arrow(node_b2, node_c2, color=WHITE)

        self.play(FadeIn(mini_row), Create(edge1), Create(edge2), run_time=0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 5 — WHY FACTORIZATION HELPS: PARAMETER COUNT
        # ============================================================

        title = txt("Factorization reduces parameter cost", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        big_box = titled_box(
            "Cost per factor",
            txt("exponential in the number of\nvariables inside that factor", 17, WHITE),
            chapter="chapter03", width=7.5, height=1.9,
        )
        big_box.next_to(title, DOWN, buff=0.8)
        fit_in_frame(big_box, margin=0.9)
        show(big_box, 1.0)

        conclusion = txt("fewer variables per factor  →  far fewer total parameters", 19, CYAN)
        conclusion.next_to(big_box, DOWN, buff=0.6)
        fit_in_frame(conclusion, margin=1.0)
        show(conclusion, 0.9)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — GRAPHS DESCRIBE FACTORIZATIONS
        # ============================================================

        title = txt("Graphical models", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Nodes = random variables.\nEdges = direct interactions the distribution can represent.",
            20, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.6)
        fit_in_frame(statement, margin=1.0)
        show(statement, 1.0)

        directed_box = titled_box(
            "Directed", txt("directed edges\nconditional distributions", 16, CYAN),
            chapter="chapter03", width=5.0, height=1.9,
        )
        directed_box[0].set_stroke(color=CYAN, width=3)

        undirected_box = titled_box(
            "Undirected", txt("undirected edges\nfactors over cliques", 16, PURPLE),
            chapter="chapter03", width=5.0, height=1.9,
        )
        undirected_box[0].set_stroke(color=PURPLE, width=3)

        row = flow_row([directed_box, undirected_box], buff=0.7)
        row.next_to(statement, DOWN, buff=0.7)
        fit_in_frame(row, margin=0.8)

        staggered_fade_in(self, [directed_box, undirected_box], run_time=1.2, lag_ratio=0.35)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 7 — DIRECTED MODEL FORMULA (3.53)
        # ============================================================

        title = txt("Directed models: one factor per variable", 28, WHITE, BOLD, )
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula2 = MathTex(
            r"p(\mathbf{x}) = \prod_i p\left(\mathrm{x}_i \mid Pa_{\mathcal{G}}(\mathrm{x}_i)\right)",
            font_size=34, color=CYAN,
        )
        formula2.next_to(title, DOWN, buff=0.7)
        show(formula2, 1.1)

        eq_num2 = txt("(3.53)", 18, MUTED)
        eq_num2.next_to(formula2, DOWN, buff=0.3)
        show(eq_num2, 0.4)

        note = txt("each factor is x_i's conditional distribution given its parents in G", 18, MUTED)
        note.next_to(eq_num2, DOWN, buff=0.5)
        fit_in_frame(note, margin=1.0)
        show(note, 0.9)

        ref = txt("see Figure 3.7 for a worked example", 16, YELLOW)
        ref.next_to(note, DOWN, buff=0.4)
        show(ref, 0.6)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 8 — UNDIRECTED MODELS: CLIQUES
        # ============================================================

        title = txt("Undirected models: cliques and factors", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        n1 = node("x₁", PURPLE, radius=0.45)
        n2 = node("x₂", PURPLE, radius=0.45)
        n3 = node("x₃", PURPLE, radius=0.45)

        n1.move_to(UP * 1.0 + LEFT * 1.6)
        n2.move_to(UP * 1.0 + RIGHT * 1.6)
        n3.move_to(DOWN * 0.6)

        e12 = Line(n1.get_bottom(), n2.get_bottom(), color=WHITE, stroke_width=2.5).set_z_index(-1)
        e12 = Line(n1.get_center(), n2.get_center(), color=WHITE, stroke_width=2.5, buff=0.45)
        e13 = Line(n1.get_center(), n3.get_center(), color=WHITE, stroke_width=2.5, buff=0.45)
        e23 = Line(n2.get_center(), n3.get_center(), color=WHITE, stroke_width=2.5, buff=0.45)

        clique_group = VGroup(e12, e13, e23, n1, n2, n3)
        clique_group.next_to(title, DOWN, buff=0.9)
        fit_in_frame(clique_group, margin=1.0)

        self.play(Create(e12), Create(e13), Create(e23), run_time=0.8)
        staggered_fade_in(self, [n1, n2, n3], run_time=0.9, lag_ratio=0.3)

        clique_label = txt("all mutually connected → a clique C  →  factor φ(C)", 17, MUTED)
        clique_label.next_to(clique_group, DOWN, buff=0.5)
        fit_in_frame(clique_label, margin=1.0)
        show(clique_label, 0.8)

        note2 = txt("unlike directed factors, φ(C) is just a function — not a probability", 16, RED)
        note2.next_to(clique_label, DOWN, buff=0.35)
        fit_in_frame(note2, margin=1.0)
        show(note2, 0.7)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Graphs turn one huge distribution\ninto many small, cheap factors.",
            27, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page_75().render()
