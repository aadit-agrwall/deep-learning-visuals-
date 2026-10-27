import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


class Page_76(Scene):

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
            group = VGroup(circle, label_obj)
            group.circle_ref = circle
            return group

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt("CHAPTER 3", 24, CYAN, BOLD)
        heading = txt("Probability and Information Theory", 40, WHITE, BOLD)
        section = txt("Figure 3.7  &  Undirected Models", 27, YELLOW)

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.8)
        show(section, 0.6)
        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — FIGURE 3.7: THE DIRECTED GRAPH a,b,c,d,e
        # ============================================================

        title = txt("Figure 3.7: A directed graphical model", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.65)
        show(title, 0.7)

        node_a = node("a", CYAN)
        node_b = node("b", CYAN)
        node_c = node("c", YELLOW)
        node_d = node("d", CYAN)
        node_e = node("e", GREEN)

        node_a.move_to(UP * 2.0 + LEFT * 1.6)
        node_b.move_to(UP * 2.0 + RIGHT * 1.6)
        node_c.move_to(UP * 0.2 + LEFT * 0.5)
        node_d.move_to(UP * 0.2 + RIGHT * 2.2)
        node_e.move_to(DOWN * 1.6 + LEFT * 0.5)

        graph_group = VGroup(node_a, node_b, node_c, node_d, node_e)
        graph_group.move_to(DOWN * 0.2)
        fit_in_frame(graph_group, margin=1.2)

        edge_ab = smart_arrow(node_a, node_b, color=WHITE)
        edge_ac = smart_arrow(node_a, node_c, color=WHITE)
        edge_bc = smart_arrow(node_b, node_c, color=WHITE)
        edge_bd = smart_arrow(node_b, node_d, color=WHITE)
        edge_ce = smart_arrow(node_c, node_e, color=WHITE)

        staggered_fade_in(self, [node_a, node_b, node_c, node_d, node_e], run_time=1.2, lag_ratio=0.25)
        self.play(
            Create(edge_ab), Create(edge_ac), Create(edge_bc),
            Create(edge_bd), Create(edge_ce), run_time=1.1,
        )

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 3 — FACTORIZATION FORMULA (3.54)
        # ============================================================

        title = txt("The factorization this graph implies", 28, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        formula = MathTex(
            r"p(\mathrm{a,b,c,d,e}) = p(\mathrm{a})\,p(\mathrm{b}\mid\mathrm{a})\,"
            r"p(\mathrm{c}\mid\mathrm{a,b})\,p(\mathrm{d}\mid\mathrm{b})\,p(\mathrm{e}\mid\mathrm{c})",
            font_size=26, color=YELLOW,
        )
        formula.next_to(title, DOWN, buff=0.7)
        fit_in_frame(formula, margin=0.7)
        show(formula, 1.2)

        eq_num = txt("(3.54)", 18, MUTED)
        eq_num.next_to(formula, DOWN, buff=0.3)
        show(eq_num, 0.4)

        note = txt("one factor per node: itself given its parents in the graph", 18, MUTED)
        note.next_to(eq_num, DOWN, buff=0.5)
        fit_in_frame(note, margin=1.0)
        show(note, 0.8)

        self.wait(1.5)
        clear_scene()

        # ============================================================
        # SCENE 4 — DIRECT VS INDIRECT INTERACTION (a & c vs a & e)
        # ============================================================

        title = txt("Direct vs. indirect interaction", 30, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        node_a2 = node("a", CYAN)
        node_c2 = node("c", YELLOW)
        node_e2 = node("e", GREEN)

        node_a2.move_to(UP * 0.6 + LEFT * 2.6)
        node_c2.move_to(UP * 0.6 + RIGHT * 0)
        node_e2.move_to(UP * 0.6 + RIGHT * 2.6)

        direct_edge = smart_arrow(node_a2, node_c2, color=GREEN)
        indirect_edge = smart_arrow(node_c2, node_e2, color=MUTED)

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
        # SCENE 5 — UNDIRECTED MODEL NORMALIZATION (3.55)
        # ============================================================

        title = txt("Normalizing an undirected model", 29, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        statement = txt(
            "Probability is proportional to the product of clique factors —\nbut that product need not sum to 1.",
            19, MUTED,
        )
        statement.next_to(title, DOWN, buff=0.55)
        fit_in_frame(statement, margin=1.0)
        show(statement, 1.0)

        formula2 = MathTex(
            r"p(\mathbf{x}) = \frac{1}{Z}\prod_i \phi^{(i)}\!\left(\mathcal{C}^{(i)}\right)",
            font_size=34, color=PURPLE,
        )
        formula2.next_to(statement, DOWN, buff=0.6)
        show(formula2, 1.1)

        eq_num2 = txt("(3.55)", 18, MUTED)
        eq_num2.next_to(formula2, DOWN, buff=0.3)
        show(eq_num2, 0.4)

        z_note = txt("Z = sum/integral over all states of the product of φ's", 17, CYAN)
        z_note.next_to(eq_num2, DOWN, buff=0.5)
        fit_in_frame(z_note, margin=1.0)
        show(z_note, 0.8)

        ref = txt("see Figure 3.8 for a worked example", 16, YELLOW)
        ref.next_to(z_note, DOWN, buff=0.35)
        show(ref, 0.6)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 6 — GRAPHS ARE A LANGUAGE, NOT A CLASS OF MODELS
        # ============================================================

        title = txt("Directed and undirected: a language, not a family", 26, WHITE, BOLD)
        title.to_edge(UP, buff=0.7)
        show(title, 0.7)

        not_box = titled_box(
            "NOT a property of the distribution",
            txt("directed vs. undirected is a property\nof a particular description", 16, RED),
            chapter="chapter03", width=8.5, height=1.9,
        )
        not_box[0].set_stroke(color=RED, width=3)
        not_box.next_to(title, DOWN, buff=0.7)
        fit_in_frame(not_box, margin=0.8)
        show(not_box, 1.0)

        yes_box = titled_box(
            "Any distribution",
            txt("can be described both ways —\nthe two are not mutually exclusive", 16, GREEN),
            chapter="chapter03", width=8.5, height=1.9,
        )
        yes_box[0].set_stroke(color=GREEN, width=3)
        yes_box.next_to(not_box, DOWN, buff=0.5)
        fit_in_frame(yes_box, margin=0.8)
        show(yes_box, 1.0)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL MESSAGE
        # ============================================================

        final = txt(
            "A graph is a language for describing factorizations —\nnot an inherent property of the distribution.",
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
    Page_76().render()
