from manim import *
import numpy as np

# ============================================================
# PAGE 93 — CONSTRAINED MAXIMIZATION, ACTIVE CONSTRAINTS & KKT CONDITIONS
# ============================================================

config.background_color = WHITE
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60


class Page_93(Scene):

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
        # SCENE 1 — CONSTRAINED MAXIMIZATION (4.19)
        # ========================================================

        title = bold("Constrained maximization", 27)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        intro = body("build the Lagrangian of −f(x) instead", 17, BLACK)
        fit_width(intro, 6.7)
        intro.next_to(title, DOWN, buff=0.4)
        self.play(Write(intro), run_time=0.8)

        formula1 = formula(
            r"\min_x \max_{\boldsymbol{\lambda}} \max_{\boldsymbol{\alpha},\alpha\geq 0} "
            r"-f(x) + \sum_i \lambda_i g^{(i)}(x) + \sum_j \alpha_j h^{(j)}(x)",
            16, BLUE,
        )
        fit_width(formula1, 6.9)
        formula1.next_to(intro, DOWN, buff=0.5)
        self.play(Write(formula1), run_time=1.3)

        eq_num1 = body("(4.19)", 14, BLACK)
        eq_num1.next_to(formula1, DOWN, buff=0.3)
        self.play(Write(eq_num1), run_time=0.4)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 2 — MAX-MIN OUTER LOOP VERSION (4.20)
        # ========================================================

        title = bold("Maximization in the outer loop", 25)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        formula2 = formula(
            r"\max_x \min_{\boldsymbol{\lambda}} \min_{\boldsymbol{\alpha},\alpha\geq 0} "
            r"f(x) + \sum_i \lambda_i g^{(i)}(x) - \sum_j \alpha_j h^{(j)}(x)",
            16, BLUE,
        )
        fit_width(formula2, 6.9)
        formula2.next_to(title, DOWN, buff=0.5)
        self.play(Write(formula2), run_time=1.3)

        eq_num2 = body("(4.20)", 14, BLACK)
        eq_num2.next_to(formula2, DOWN, buff=0.3)
        self.play(Write(eq_num2), run_time=0.4)

        note = body("the sign of the equality term doesn't matter —\nthe optimizer is free to pick any sign for λᵢ", 15, BLACK)
        fit_width(note, 6.6)
        note.next_to(eq_num2, DOWN, buff=0.4)
        self.play(Write(note), run_time=1.0)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 3 — ACTIVE VS INACTIVE CONSTRAINTS
        # ========================================================

        title = bold("Active vs. inactive constraints", 25)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        active_formula = formula(r"h^{(i)}(x^{*}) = 0", 24, BLUE)
        active_formula.next_to(title, DOWN, buff=0.4)
        self.play(Write(active_formula), run_time=0.8)

        active_box = RoundedRectangle(
            width=6.8, height=1.5, corner_radius=0.16,
            color=BLUE, stroke_width=2.5,
        )
        active_box.next_to(active_formula, DOWN, buff=0.4)

        active_title = bold("Active", 19, BLUE)
        active_title.move_to(active_box.get_center() + UP * 0.35)

        active_text = body("constraint holds with equality\nremoving it would change the solution", 14, BLACK)
        active_text.move_to(active_box.get_center() + DOWN * 0.3)

        self.play(Create(active_box), Write(active_title), Write(active_text), run_time=1.0)

        inactive_box = RoundedRectangle(
            width=6.8, height=1.5, corner_radius=0.16,
            color=BLACK, stroke_width=2.5,
        )
        inactive_box.next_to(active_box, DOWN, buff=0.35)

        inactive_title = bold("Inactive", 19, BLACK)
        inactive_title.move_to(inactive_box.get_center() + UP * 0.35)

        inactive_text = body("h⁽ⁱ⁾(x) < 0, not binding\nremoving it keeps at least a local solution", 14, BLACK)
        inactive_text.move_to(inactive_box.get_center() + DOWN * 0.3)

        self.play(Create(inactive_box), Write(inactive_title), Write(inactive_text), run_time=1.0)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 4 — WHY INACTIVE CONSTRAINTS CAN STILL MATTER
        # ========================================================

        title = bold("An inactive constraint can still matter", 22)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        flat_axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 3, 1],
            x_length=6.0, y_length=2.6,
            axis_config={"color": BLACK, "stroke_width": 1.4, "include_numbers": False},
        )
        flat_axes.next_to(title, DOWN, buff=0.4)

        flat_curve = flat_axes.plot(
            lambda x: 0.15 if -1.5 <= x <= 1.5 else 0.15 + 0.6 * (abs(x) - 1.5) ** 2,
            x_range=[-3, 3], color=BLUE, stroke_width=3.5,
        )

        self.play(Create(flat_axes), run_time=0.6)
        self.play(Create(flat_curve), run_time=1.0)

        excluded_region = flat_axes.get_area(
            flat_curve, x_range=(1.0, 1.5), color=BLACK, opacity=0.15,
        )
        self.play(FadeIn(excluded_region), run_time=0.6)

        note = body("a constraint can carve out part of\na flat region of equally-optimal points", 15, BLACK)
        fit_width(note, 6.6)
        note.next_to(flat_axes, DOWN, buff=0.35)
        self.play(Write(note), run_time=1.0)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 5 — COMPLEMENTARY SLACKNESS
        # ========================================================

        title = bold("Complementary slackness", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        slack_formula = formula(r"\boldsymbol{\alpha} \odot h(x) = 0", 30, BLUE)
        slack_formula.next_to(title, DOWN, buff=0.6)
        self.play(Write(slack_formula), run_time=1.0)

        note = body("inactive h⁽ⁱ⁾ has negative value  ⟹  its αᵢ = 0", 16, BLACK)
        fit_width(note, 6.7)
        note.next_to(slack_formula, DOWN, buff=0.5)
        self.play(Write(note), run_time=0.9)

        or_row = VGroup(
            body("αᵢ ≥ 0", 18, BLUE),
            body("  or  ", 16, BLACK),
            body("h⁽ⁱ⁾(x) ≤ 0", 18, BLACK),
        ).arrange(RIGHT, buff=0.15)
        or_row.next_to(note, DOWN, buff=0.5)
        self.play(Write(or_row), run_time=0.8)

        or_note = body("at least one must be active at the solution", 15, BLACK)
        fit_width(or_note, 6.5)
        or_note.next_to(or_row, DOWN, buff=0.35)
        self.play(Write(or_note), run_time=0.8)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 6 — INTUITION: BOUNDARY VS ZEROED-OUT MULTIPLIER
        # ========================================================

        title = bold("Two ways a constraint can behave", 24)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        on_boundary = RoundedRectangle(
            width=6.8, height=1.6, corner_radius=0.16,
            color=BLUE, stroke_width=2.5,
        )
        on_boundary.next_to(title, DOWN, buff=0.5)

        boundary_title = bold("On the boundary", 18, BLUE)
        boundary_title.move_to(on_boundary.get_center() + UP * 0.35)

        boundary_text = body("the KKT multiplier is used\nto actively influence x", 14, BLACK)
        boundary_text.move_to(on_boundary.get_center() + DOWN * 0.3)

        self.play(Create(on_boundary), Write(boundary_title), Write(boundary_text), run_time=1.0)

        zeroed = RoundedRectangle(
            width=6.8, height=1.6, corner_radius=0.16,
            color=BLACK, stroke_width=2.5,
        )
        zeroed.next_to(on_boundary, DOWN, buff=0.35)

        zeroed_title = bold("Zeroed out", 18, BLACK)
        zeroed_title.move_to(zeroed.get_center() + UP * 0.35)

        zeroed_text = body("the constraint has no influence,\nrepresented by αᵢ = 0", 14, BLACK)
        zeroed_text.move_to(zeroed.get_center() + DOWN * 0.3)

        self.play(Create(zeroed), Write(zeroed_title), Write(zeroed_text), run_time=1.0)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 7 — THE KKT CONDITIONS SUMMARY
        # ========================================================

        title = bold("The KKT conditions", 28)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        subtitle = body("necessary, but not always sufficient, for optimality", 15, BLACK)
        fit_width(subtitle, 6.7)
        subtitle.next_to(title, DOWN, buff=0.35)
        self.play(Write(subtitle), run_time=0.8)

        cond1 = body("1.  Gradient of the generalized Lagrangian is zero", 15, BLACK)
        cond2 = body("2.  All constraints on x and the multipliers hold", 15, BLACK)
        cond3 = formula(r"3.\ \ \boldsymbol{\alpha}\odot h(x) = 0 \ \ \text{(complementary slackness)}", 15, BLUE)

        conds = VGroup(cond1, cond2, cond3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        fit_width(conds, 6.7)
        conds.next_to(subtitle, DOWN, buff=0.55)

        self.play(Write(cond1), run_time=0.8)
        self.play(Write(cond2), run_time=0.8)
        self.play(Write(cond3), run_time=0.9)

        self.wait(1.5)
        clear_scene()

        # ========================================================
        # SCENE 8 — FINAL MESSAGE
        # ========================================================

        final = bold(
            "KKT: turn constrained optimality\ninto a checkable set of conditions.",
            22,
        )
        fit_width(final, 6.8)
        final.move_to(ORIGIN)

        self.play(Write(final), run_time=1.1)
        self.wait(0.4)

        line = Underline(final, color=BLUE, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.wait(2.0)


if __name__ == "__main__":
    Page_93().render()
