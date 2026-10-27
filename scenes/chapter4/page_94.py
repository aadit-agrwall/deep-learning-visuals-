from manim import *
import numpy as np

# ============================================================
# PAGE 94 — 4.5 EXAMPLE: LINEAR LEAST SQUARES
# ============================================================

config.background_color = WHITE
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60


class Page_94(Scene):

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

        def mono(text, size=18, color=BLACK):
            return Text(
                text,
                font="DejaVu Sans Mono",
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
        # SCENE 1 — SECTION TITLE
        # ========================================================

        section = bold("4.5  Example: Linear Least Squares", 25)
        section.to_edge(UP, buff=0.6)
        self.play(Write(section), run_time=0.9)

        statement = body("find the value of x that minimizes", 17, BLACK)
        statement.next_to(section, DOWN, buff=0.5)
        self.play(Write(statement), run_time=0.8)

        objective = formula(r"f(x) = \frac{1}{2}||Ax - b||_2^2", 30, BLUE)
        objective.next_to(statement, DOWN, buff=0.5)
        self.play(Write(objective), run_time=1.0)

        eq_num1 = body("(4.21)", 14, BLACK)
        eq_num1.next_to(objective, DOWN, buff=0.3)
        self.play(Write(eq_num1), run_time=0.4)

        note = body("solvable by specialized linear algebra —\nbut also a good example for gradient methods", 15, BLACK)
        fit_width(note, 6.6)
        note.next_to(eq_num1, DOWN, buff=0.4)
        self.play(Write(note), run_time=1.0)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 2 — THE GRADIENT (4.22)
        # ========================================================

        title = bold("Step 1: obtain the gradient", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        gradient = formula(r"\nabla_x f(x) = A^\top(Ax - b) = A^\top A x - A^\top b", 20, BLUE)
        fit_width(gradient, 6.9)
        gradient.next_to(title, DOWN, buff=0.6)
        self.play(Write(gradient), run_time=1.1)

        eq_num2 = body("(4.22)", 14, BLACK)
        eq_num2.next_to(gradient, DOWN, buff=0.3)
        self.play(Write(eq_num2), run_time=0.4)

        arrow_down = body("↓", 26, BLACK)
        arrow_down.next_to(eq_num2, DOWN, buff=0.3)
        self.play(Write(arrow_down), run_time=0.4)

        note = body("follow the gradient downhill, taking small steps", 16, BLACK)
        fit_width(note, 6.7)
        note.next_to(arrow_down, DOWN, buff=0.3)
        self.play(Write(note), run_time=0.8)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 3 — ALGORITHM 4.1: GRADIENT DESCENT PSEUDOCODE
        # ========================================================

        title = bold("Algorithm 4.1: gradient descent", 24)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        subtitle = body("minimize f(x) starting from an arbitrary x", 15, BLACK)
        fit_width(subtitle, 6.6)
        subtitle.next_to(title, DOWN, buff=0.35)
        self.play(Write(subtitle), run_time=0.8)

        algo_box = RoundedRectangle(
            width=7.0, height=3.0, corner_radius=0.14,
            color=BLACK, stroke_width=2.3,
        )
        algo_box.next_to(subtitle, DOWN, buff=0.4)

        line0 = mono("Set step size ε and tolerance δ", 15, BLACK)
        line1 = mono("while ||AᵀAx − Aᵀb||₂ > δ do", 15, BLACK)
        line2 = mono("    x ← x − ε(AᵀAx − Aᵀb)", 15, BLUE)
        line3 = mono("end while", 15, BLACK)

        code_lines = VGroup(line0, line1, line2, line3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        )
        fit_width(code_lines, 6.5)
        code_lines.move_to(algo_box.get_center())

        self.play(Create(algo_box), run_time=0.7)
        self.play(Write(line0), run_time=0.7)
        self.play(Write(line1), run_time=0.7)
        self.play(Write(line2), run_time=0.8)
        self.play(Write(line3), run_time=0.5)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 4 — NEWTON'S METHOD: EXACT IN ONE STEP
        # ========================================================

        title = bold("Newton's method: exact for quadratics", 22)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 6, 2],
            x_length=5.6, y_length=3.0,
            axis_config={"color": BLACK, "stroke_width": 1.4, "include_numbers": False},
        )
        axes.next_to(title, DOWN, buff=0.5)

        curve = axes.plot(lambda x: 0.6 * x ** 2, x_range=[-3, 3], color=BLUE, stroke_width=4)

        start = Dot(axes.c2p(-2.3, 0.6 * 2.3 ** 2), color=BLACK, radius=0.08)
        target = Dot(axes.c2p(0, 0), color=BLUE, radius=0.09)
        jump = Arrow(start.get_center(), target.get_center(), color=BLUE, stroke_width=3.5, buff=0.08)

        self.play(Create(axes), run_time=0.5)
        self.play(Create(curve), run_time=0.9)
        self.play(FadeIn(start), run_time=0.4)
        self.play(Create(jump), run_time=0.8)
        self.play(FadeIn(target), run_time=0.4)

        note = body("quadratic approximation is exact —\nconverges to the global minimum in a single step", 15, BLACK)
        fit_width(note, 6.6)
        note.next_to(axes, DOWN, buff=0.35)
        self.play(Write(note), run_time=1.0)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 5 — ADDING A CONSTRAINT: LAGRANGIAN (4.23)
        # ========================================================

        title = bold("Now add a constraint", 27)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        constraint = formula(r"x^\top x \leq 1", 28, BLUE)
        constraint.next_to(title, DOWN, buff=0.5)
        self.play(Write(constraint), run_time=0.9)

        note = body("introduce the Lagrangian", 16, BLACK)
        note.next_to(constraint, DOWN, buff=0.4)
        self.play(Write(note), run_time=0.6)

        lagrangian = formula(r"L(x,\lambda) = f(x) + \lambda(x^\top x - 1)", 22, BLUE)
        fit_width(lagrangian, 6.8)
        lagrangian.next_to(note, DOWN, buff=0.4)
        self.play(Write(lagrangian), run_time=1.0)

        eq_num3 = body("(4.23)", 14, BLACK)
        eq_num3.next_to(lagrangian, DOWN, buff=0.3)
        self.play(Write(eq_num3), run_time=0.4)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 6 — SOLVE THE MIN-MAX PROBLEM (4.24)
        # ========================================================

        title = bold("Solving the min-max problem", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        minmax = formula(r"\min_x \max_{\lambda,\lambda \geq 0} L(x,\lambda)", 28, BLUE)
        minmax.next_to(title, DOWN, buff=0.6)
        self.play(Write(minmax), run_time=1.0)

        eq_num4 = body("(4.24)", 14, BLACK)
        eq_num4.next_to(minmax, DOWN, buff=0.3)
        self.play(Write(eq_num4), run_time=0.4)

        self.wait(1.1)
        clear_scene()

        # ========================================================
        # SCENE 7 — CHECK THE UNCONSTRAINED SOLUTION FIRST
        # ========================================================

        title = bold("Check the unconstrained solution first", 21)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        pseudo = formula(r"x = A^{+}b", 32, BLUE)
        pseudo.next_to(title, DOWN, buff=0.6)
        self.play(Write(pseudo), run_time=1.0)

        note = body("smallest-norm solution via the\nMoore-Penrose pseudoinverse", 16, BLACK)
        fit_width(note, 6.6)
        note.next_to(pseudo, DOWN, buff=0.5)
        self.play(Write(note), run_time=0.9)

        feasible_box = RoundedRectangle(
            width=6.6, height=1.3, corner_radius=0.15,
            color=BLUE, stroke_width=2.3,
        )
        feasible_box.next_to(note, DOWN, buff=0.4)

        feasible_text = body("if feasible → this IS the\nconstrained solution", 15, BLACK)
        feasible_text.move_to(feasible_box.get_center())

        self.play(Create(feasible_box), Write(feasible_text), run_time=0.9)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 8 — FINAL MESSAGE
        # ========================================================

        final = bold(
            "Gradient descent, Newton's method, and\nLagrangians all meet at least squares.",
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
    Page_94().render()
