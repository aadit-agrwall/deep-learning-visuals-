import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_77(Scene):

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

        def node(label, color=CYAN, radius=0.42):
            circle = Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.15, stroke_width=3)
            label_obj = txt(label, 24, WHITE, BOLD)
            label_obj.move_to(circle.get_center())
            return VGroup(circle, label_obj)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("Figure 3.8  &  Chapter Wrap-Up", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 3.8: THE UNDIRECTED GRAPH a,b,c,d,e
        # ============================================================

        title = txt("Figure 3.8: An undirected graphical model", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.65)
        show(title, 0.7)

        node_a = node("a", PURPLE)
        node_b = node("b", PURPLE)
        node_c = node("c", YELLOW)
        node_d = node("d", PURPLE)
        node_e = node("e", GREEN)

        node_a.move_to(UP * 2.0 + LEFT * 1.6)
        node_b.move_to(UP * 2.0 + RIGHT * 1.6)
        node_c.move_to(UP * 0.2 + LEFT * 0.5)
        node_d.move_to(UP * 0.2 + RIGHT * 2.2)
        node_e.move_to(DOWN * 1.6 + LEFT * 0.5)

        graph_group = VGroup(node_a, node_b, node_c, node_d, node_e)
        graph_group.move_to(DOWN * 0.2)
        fit_in_frame(graph_group, margin=1.2)

        # undirected edges: plain lines, no arrowheads
        edge_ab = Line(node_a.get_center(), node_b.get_center(), color=WHITE, stroke_width=2.5, buff=0.42)
        edge_ac = Line(node_a.get_center(), node_c.get_center(), color=WHITE, stroke_width=2.5, buff=0.42)
        edge_bc = Line(node_b.get_center(), node_c.get_center(), color=WHITE, stroke_width=2.5, buff=0.42)
        edge_bd = Line(node_b.get_center(), node_d.get_center(), color=WHITE, stroke_width=2.5, buff=0.42)
        edge_ce = Line(node_c.get_center(), node_e.get_center(), color=WHITE, stroke_width=2.5, buff=0.42)

        staggered_fade_in(self, [node_a, node_b, node_c, node_d, node_e], run_time=1.2, lag_ratio=0.25)
        self.play(
            Create(edge_ab), Create(edge_ac), Create(edge_bc),
            Create(edge_bd), Create(edge_ce), run_time=1.1,
        )

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 3 — CLIQUE FACTORIZATION (3.56)
        # ============================================================

        title = txt("Factoring over cliques", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"p(\mathrm{a,b,c,d,e}) = \frac{1}{Z}\,\phi^{(1)}(\mathrm{a,b,c})\,"
            r"\phi^{(2)}(\mathrm{b,d})\,\phi^{(3)}(\mathrm{c,e})",
            font_size=28, color=YELLOW,
        )
        formula.next_to(title, DOWN, buff=0.7)
        fit_in_frame(formula, margin=0.7)
        show(formula, 1.2)

        eq_num = txt("(3.56)", 18, MUTED)
        eq_num.next_to(formula, DOWN, buff=0.3)
        show(eq_num, 0.4)

        clique1 = titled_box("φ⁽¹⁾", txt("clique {a, b, c}", 15, PURPLE), chapter="chapter03", width=3.2, height=1.4)
        clique2 = titled_box("φ⁽²⁾", txt("clique {b, d}", 15, CYAN), chapter="chapter03", width=3.2, height=1.4)
        clique3 = titled_box("φ⁽³⁾", txt("clique {c, e}", 15, GREEN), chapter="chapter03", width=3.2, height=1.4)

        clique_row = flow_row([clique1, clique2, clique3], buff=0.4)
        clique_row.next_to(eq_num, DOWN, buff=0.5)
        fit_in_frame(clique_row, margin=0.8)

        staggered_fade_in(self, [clique1, clique2, clique3], run_time=1.1, lag_ratio=0.3)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — SAME INSIGHT: DIRECT VS INDIRECT
        # ============================================================

        title = txt("Same structural insight as before", 29, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        node_a2 = node("a", PURPLE)
        node_c2 = node("c", YELLOW)
        node_e2 = node("e", GREEN)

        node_a2.move_to(UP * 0.6 + LEFT * 2.6)
        node_c2.move_to(UP * 0.6 + RIGHT * 0)
        node_e2.move_to(UP * 0.6 + RIGHT * 2.6)

        direct_edge = Line(node_a2.get_center(), node_c2.get_center(), color=GREEN, stroke_width=3, buff=0.42)
        indirect_edge = Line(node_c2.get_center(), node_e2.get_center(), color=MUTED, stroke_width=3, buff=0.42)

        small_group = VGroup(node_a2, node_c2, node_e2)
        fit_in_frame(VGroup(small_group, direct_edge, indirect_edge), margin=1.0)

        staggered_fade_in(self, [node_a2, node_c2, node_e2], run_time=1.0, lag_ratio=0.3)
        self.play(Create(direct_edge), run_time=0.6)
        self.play(Create(indirect_edge), run_time=0.6)

        direct_label = txt("a, c interact directly", 18, GREEN)
        direct_label.next_to(small_group, DOWN, buff=0.6)

        indirect_label = txt("a, e interact only indirectly, through c", 18, MUTED)
        indirect_label.next_to(direct_label, DOWN, buff=0.35)

        fit_in_frame(VGroup(direct_label, indirect_label), margin=1.0)
        show(direct_label, 0.7)
        show(indirect_label, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 5 — WHAT GRAPHS ARE FOR, AND CHAPTER LOOKAHEAD
        # ============================================================

        title = txt("A language, not a full theory (yet)", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        lang_box = titled_box(
            "For now",
            txt("graphs describe which direct probabilistic\nrelationships an ML algorithm chooses to represent",
                16, WHITE),
            chapter="chapter03", width=8.6, height=2.0,
        )
        lang_box.next_to(title, DOWN, buff=0.7)
        fit_in_frame(lang_box, margin=0.8)
        show(lang_box, 1.0)

        later_box = titled_box(
            "Later",
            txt("Part III explores structured\nprobabilistic models in far more depth", 16, CYAN),
            chapter="chapter03", width=8.6, height=1.9,
        )
        later_box.next_to(lang_box, DOWN, buff=0.45)
        fit_in_frame(later_box, margin=0.8)
        show(later_box, 1.0)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 6 — CHAPTER 3 WRAP-UP / LOOKAHEAD TO NUMERICAL METHODS
        # ============================================================

        title = txt("End of Chapter 3", 32, WHITE, BOLD)
        title.to_edge(UP, buff=0.8)
        show(title, 0.8)

        recap = txt(
            "Probability theory + information theory:\nthe basic tools for reasoning under uncertainty.",
            22, MUTED,
        )
        recap.next_to(title, DOWN, buff=0.7)
        fit_in_frame(recap, margin=1.0)
        show(recap, 1.0)

        next_box = titled_box(
            "Up next: Chapter 4",
            txt("Numerical Methods", 20, YELLOW, BOLD),
            chapter="chapter03", width=6.5, height=1.7,
        )
        next_box[0].set_stroke(color=YELLOW, width=3)
        next_box.next_to(recap, DOWN, buff=0.7)
        fit_in_frame(next_box, margin=0.8)
        show(next_box, 1.0)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "Graphs are a language for factorizations —\none more tool remains: numerical methods.",
            25, WHITE, BOLD,
        )
        final.move_to(ORIGIN + UP * 0.25)
        fit_in_frame(final, margin=1.0)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.2)


if __name__ == "__main__":
    Page_77().render()
