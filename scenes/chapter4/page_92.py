from manim import *
import numpy as np

# ============================================================
# PAGE 92 — KKT APPROACH & THE GENERALIZED LAGRANGIAN
# ============================================================

config.background_color = WHITE
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60


class Page_92(Scene):

    def construct(self):

        BLACK = "#000000"
        BLUE = "#0047AB"
        WHITE_BG = "#FFFFFF"

        self.camera.background_color = WHITE_BG

        # --------------------------------------------------------
        # Helpers
        # --------------------------------------------------------

        def body(text, size=21, color=BLACK):
            return Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
            )

        def bold(text, size=30, color=BLACK):
            obj = Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
                weight=BOLD,
            )
            if obj.width > 7.4:
                obj.scale_to_fit_width(7.4)
            return obj

        def formula(tex, size=32, color=BLACK):
            return MathTex(
                tex,
                font_size=size,
                color=color,
            )

        def fit_width(obj, width=7.25):
            if obj.width > width:
                obj.scale_to_fit_width(width)
            return obj

        def clear_scene():
            mobs = list(self.mobjects)
            if mobs:
                self.play(
                    *[FadeOut(mob) for mob in mobs],
                    run_time=0.45,
                )
            self.wait(0.2)

        # ========================================================
        # SCENE 1 — REFORMULATION EXAMPLE: UNIT NORM CONSTRAINT
        # ========================================================

        title = bold("Reformulating a constraint", 27)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        intro = body("x ∈ R² constrained to unit L² norm", 17, BLACK)
        fit_width(intro, 6.8)
        intro.next_to(title, DOWN, buff=0.35)
        self.play(Write(intro), run_time=0.8)

        circle_axes = Axes(
            x_range=[-1.6, 1.6, 1], y_range=[-1.6, 1.6, 1],
            x_length=3.6, y_length=3.6,
            axis_config={"color": BLACK, "stroke_width": 1.2, "include_numbers": False},
        )
        circle_axes.next_to(intro, DOWN, buff=0.4)

        unit_circle = Circle(radius=1.35, color=BLUE, stroke_width=3.5)
        unit_circle.move_to(circle_axes.c2p(0, 0))

        theta_dot = Dot(circle_axes.c2p(np.cos(0.9), np.sin(0.9)), color=BLACK, radius=0.07)
        theta_line = Line(circle_axes.c2p(0, 0), theta_dot.get_center(), color=BLACK, stroke_width=2)
        theta_label = formula(r"\theta", 22, BLUE)
        theta_label.next_to(circle_axes.c2p(0.5, 0.15), UP, buff=0.05)

        self.play(Create(circle_axes), run_time=0.5)
        self.play(Create(unit_circle), run_time=0.9)
        self.play(Create(theta_line), FadeIn(theta_dot), Write(theta_label), run_time=0.7)

        reparam = formula(r"g(\theta) = f([\cos\theta, \sin\theta]^\top)", 22, BLUE)
        fit_width(reparam, 6.8)
        reparam.next_to(circle_axes, DOWN, buff=0.35)
        self.play(Write(reparam), run_time=1.0)

        note = body("minimize over θ, then return [cos θ, sin θ]", 15, BLACK)
        fit_width(note, 6.6)
        note.next_to(reparam, DOWN, buff=0.3)
        self.play(Write(note), run_time=0.8)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 2 — THE KKT APPROACH: GENERAL SOLUTION
        # ========================================================

        title = bold("The Karush-Kuhn-Tucker approach", 24)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        kkt_box = RoundedRectangle(
            width=6.8, height=1.8, corner_radius=0.16,
            color=BLUE, stroke_width=2.5,
        )
        kkt_box.next_to(title, DOWN, buff=0.5)

        kkt_text = body("a very general solution\nto constrained optimization", 18, BLACK)
        kkt_text.move_to(kkt_box.get_center())

        self.play(Create(kkt_box), Write(kkt_text), run_time=1.0)

        intro_lagrangian = body("introduces the generalized Lagrangian", 17, BLACK)
        fit_width(intro_lagrangian, 6.6)
        intro_lagrangian.next_to(kkt_box, DOWN, buff=0.5)
        self.play(Write(intro_lagrangian), run_time=0.8)

        self.wait(1.2)
        clear_scene()

        # ========================================================
        # SCENE 3 — DESCRIBING S: EQUALITY AND INEQUALITY CONSTRAINTS
        # ========================================================

        title = bold("Describing S with constraints", 25)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        set_def = formula(
            r"\mathbb{S} = \{x \mid \forall i, g^{(i)}(x)=0,\ \forall j, h^{(j)}(x)\leq 0\}",
            20, BLUE,
        )
        fit_width(set_def, 6.9)
        set_def.next_to(title, DOWN, buff=0.5)
        self.play(Write(set_def), run_time=1.1)

        eq_box = RoundedRectangle(
            width=6.6, height=1.3, corner_radius=0.15,
            color=BLACK, stroke_width=2.3,
        )
        eq_box.next_to(set_def, DOWN, buff=0.5)

        eq_text = formula(r"g^{(i)}(x) = 0", 22, BLACK)
        eq_text.move_to(eq_box.get_center() + UP * 0.28)
        eq_caption = body("equality constraints", 14, BLACK)
        eq_caption.move_to(eq_box.get_center() + DOWN * 0.32)

        self.play(Create(eq_box), Write(eq_text), Write(eq_caption), run_time=0.9)

        ineq_box = RoundedRectangle(
            width=6.6, height=1.3, corner_radius=0.15,
            color=BLUE, stroke_width=2.3,
        )
        ineq_box.next_to(eq_box, DOWN, buff=0.35)

        ineq_text = formula(r"h^{(j)}(x) \leq 0", 22, BLUE)
        ineq_text.move_to(ineq_box.get_center() + UP * 0.28)
        ineq_caption = body("inequality constraints", 14, BLACK)
        ineq_caption.move_to(ineq_box.get_center() + DOWN * 0.32)

        self.play(Create(ineq_box), Write(ineq_text), Write(ineq_caption), run_time=0.9)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 4 — KKT MULTIPLIERS & GENERALIZED LAGRANGIAN (4.14)
        # ========================================================

        title = bold("The generalized Lagrangian", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        multiplier_note = body("introduce λᵢ and αⱼ — one per constraint", 16, BLACK)
        fit_width(multiplier_note, 6.7)
        multiplier_note.next_to(title, DOWN, buff=0.4)
        self.play(Write(multiplier_note), run_time=0.9)

        lagrangian = formula(
            r"L(x,\boldsymbol{\lambda},\boldsymbol{\alpha}) = f(x) + \sum_i \lambda_i g^{(i)}(x) + \sum_j \alpha_j h^{(j)}(x)",
            18, BLUE,
        )
        fit_width(lagrangian, 6.9)
        lagrangian.next_to(multiplier_note, DOWN, buff=0.55)
        self.play(Write(lagrangian), run_time=1.3)

        eq_num = body("(4.14)", 14, BLACK)
        eq_num.next_to(lagrangian, DOWN, buff=0.3)
        self.play(Write(eq_num), run_time=0.4)

        term_row = VGroup(
            body("f(x)", 15, BLACK),
            body("+", 15, BLACK),
            body("Σ λᵢ g⁽ⁱ⁾", 15, BLACK),
            body("+", 15, BLACK),
            body("Σ αⱼ h⁽ʲ⁾", 15, BLUE),
        ).arrange(RIGHT, buff=0.25)
        term_row.next_to(eq_num, DOWN, buff=0.4)
        fit_width(term_row, 6.8)
        self.play(Write(term_row), run_time=0.9)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 5 — UNCONSTRAINED MIN-MAX = CONSTRAINED MIN (4.15, 4.16)
        # ========================================================

        title = bold("Constrained min becomes unconstrained min-max", 21)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        minmax = formula(
            r"\min_x \max_{\boldsymbol{\lambda}} \max_{\boldsymbol{\alpha},\alpha\geq 0} L(x,\boldsymbol{\lambda},\boldsymbol{\alpha})",
            22, BLUE,
        )
        fit_width(minmax, 6.8)
        minmax.next_to(title, DOWN, buff=0.5)
        self.play(Write(minmax), run_time=1.1)

        eq_num1 = body("(4.15)", 14, BLACK)
        eq_num1.next_to(minmax, DOWN, buff=0.2)
        self.play(Write(eq_num1), run_time=0.4)

        same_as = body("has the same optimum as", 16, BLACK)
        same_as.next_to(eq_num1, DOWN, buff=0.4)
        self.play(Write(same_as), run_time=0.6)

        constrained_min = formula(r"\min_{x \in \mathbb{S}} f(x)", 26, BLACK)
        constrained_min.next_to(same_as, DOWN, buff=0.4)
        self.play(Write(constrained_min), run_time=0.9)

        eq_num2 = body("(4.16)", 14, BLACK)
        eq_num2.next_to(constrained_min, DOWN, buff=0.2)
        self.play(Write(eq_num2), run_time=0.4)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 6 — WHY IT WORKS: FEASIBLE VS VIOLATED (4.17, 4.18)
        # ========================================================

        title = bold("Why the equivalence holds", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        feasible_box = RoundedRectangle(
            width=6.9, height=1.7, corner_radius=0.16,
            color=BLUE, stroke_width=2.5,
        )
        feasible_box.next_to(title, DOWN, buff=0.5)

        feasible_title = bold("Constraints satisfied", 18, BLUE)
        feasible_title.move_to(feasible_box.get_center() + UP * 0.4)

        feasible_formula = formula(
            r"\max_{\boldsymbol{\lambda}} \max_{\boldsymbol{\alpha}, \alpha \geq 0} L = f(x)",
            17, BLUE,
        )
        fit_width(feasible_formula, 6.4)
        feasible_formula.move_to(feasible_box.get_center() + DOWN * 0.35)

        self.play(Create(feasible_box), Write(feasible_title), Write(feasible_formula), run_time=1.0)

        eq_num3 = body("(4.17)", 13, BLACK)
        eq_num3.next_to(feasible_box, DOWN, buff=0.15)
        self.play(Write(eq_num3), run_time=0.3)

        violated_box = RoundedRectangle(
            width=6.9, height=1.7, corner_radius=0.16,
            color=BLACK, stroke_width=2.5,
        )
        violated_box.next_to(eq_num3, DOWN, buff=0.35)

        violated_title = bold("Constraint violated", 18, BLACK)
        violated_title.move_to(violated_box.get_center() + UP * 0.4)

        violated_formula = formula(
            r"\max_{\boldsymbol{\lambda}} \max_{\boldsymbol{\alpha}, \alpha \geq 0} L = \infty",
            17, BLACK,
        )
        violated_formula.move_to(violated_box.get_center() + DOWN * 0.35)

        self.play(Create(violated_box), Write(violated_title), Write(violated_formula), run_time=1.0)

        eq_num4 = body("(4.18)", 13, BLACK)
        eq_num4.next_to(violated_box, DOWN, buff=0.15)
        self.play(Write(eq_num4), run_time=0.3)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 7 — FINAL MESSAGE
        # ========================================================

        final = bold(
            "Infeasible points get pushed to infinity;\nthe feasible optimum stays untouched.",
            21,
        )
        fit_width(final, 6.8)
        final.move_to(ORIGIN)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=BLUE, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.0)


if __name__ == "__main__":
    Page_92().render()
