from manim import *
import numpy as np

# ============================================================
# PAGE 91 — CONVEX OPTIMIZATION & CONSTRAINED OPTIMIZATION
# ============================================================

config.background_color = WHITE
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60


class Page_91(Scene):

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
        # SCENE 1 — CONVEX OPTIMIZATION
        # ========================================================

        title = bold("Convex optimization", 32)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        intro = body("Stronger restrictions buy stronger guarantees.", 18)
        fit_width(intro, 7.0)
        intro.next_to(title, DOWN, buff=0.3)
        self.play(Write(intro), run_time=0.7)

        condition = formula(r"\nabla^2 f(x) \succeq 0 \ \ \text{everywhere}", 24, BLUE)
        fit_width(condition, 7.0)
        condition.next_to(intro, DOWN, buff=0.4)
        self.play(Write(condition), run_time=0.9)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 3],
            x_length=5.6,
            y_length=2.9,
            axis_config={"color": BLACK, "stroke_width": 1.6, "include_numbers": False},
        )
        axes.next_to(condition, DOWN, buff=0.4)

        curve = axes.plot(lambda x: x ** 2, x_range=[-3, 3], color=BLUE, stroke_width=4)

        self.play(Create(axes), run_time=0.7)
        self.play(Create(curve), run_time=1.0)

        min_dot = Dot(axes.c2p(0, 0), radius=0.08, color=BLACK)
        min_label = body("global minimum", 14, BLACK)
        min_label.next_to(min_dot, DOWN, buff=0.15)

        self.play(FadeIn(min_dot), Write(min_label), run_time=0.6)

        note = body("no saddle points — every local minimum is global", 14, BLACK)
        fit_width(note, 6.8)
        note.next_to(axes, DOWN, buff=0.35)
        self.play(Write(note), run_time=0.7)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 2 — LIMITED ROLE IN DEEP LEARNING
        # ========================================================

        title = bold("A limited role in deep learning", 25)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        box1 = RoundedRectangle(
            width=6.8, height=1.5, corner_radius=0.16,
            color=BLACK, stroke_width=2.3,
        )
        box1.move_to(UP * 1.9)

        box1_title = bold("Most DL problems", 19, BLACK)
        box1_title.move_to(box1.get_center() + UP * 0.4)

        box1_text = body("hard to express as\nconvex optimization", 15, BLACK)
        box1_text.move_to(box1.get_center() + DOWN * 0.3)

        self.play(Create(box1), Write(box1_title), Write(box1_text), run_time=1.0)

        arrow1 = Arrow(
            box1.get_bottom(), box1.get_bottom() + DOWN * 0.4,
            color=BLUE, stroke_width=3, buff=0.05,
        )
        self.play(Create(arrow1), run_time=0.4)

        box2 = RoundedRectangle(
            width=6.8, height=1.5, corner_radius=0.16,
            color=BLUE, stroke_width=2.3,
        )
        box2.move_to(UP * 0.05)

        box2_title = bold("Convex methods", 19, BLUE)
        box2_title.move_to(box2.get_center() + UP * 0.4)

        box2_text = body("used only as a subroutine\ninside larger DL algorithms", 15, BLACK)
        box2_text.move_to(box2.get_center() + DOWN * 0.3)

        self.play(Create(box2), Write(box2_title), Write(box2_text), run_time=1.0)

        result_box = RoundedRectangle(
            width=6.8, height=1.3, corner_radius=0.16,
            color=BLACK, stroke_width=2.3,
        )
        result_box.move_to(DOWN * 1.9)

        result_text = body("still useful for proving convergence", 15, BLACK)
        fit_width(result_text, 6.0)
        result_text.move_to(result_box.get_center())

        self.play(Create(result_box), Write(result_text), run_time=0.9)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 3 — 4.4 CONSTRAINED OPTIMIZATION
        # ========================================================

        title = bold("4.4  Constrained optimization", 27)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        statement = body("optimize f(x) only for x in some set S", 16, BLACK)
        fit_width(statement, 6.8)
        statement.next_to(title, DOWN, buff=0.3)
        self.play(Write(statement), run_time=0.8)

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4.6, y_length=4.6,
            background_line_style={"stroke_color": BLACK, "stroke_width": 0.6, "stroke_opacity": 0.15},
            axis_config={"color": BLACK, "stroke_width": 1.4},
        )
        plane.next_to(statement, DOWN, buff=0.35)

        feasible_region = Circle(
            radius=1.1, color=BLUE, fill_color=BLUE, fill_opacity=0.12, stroke_width=3,
        )
        feasible_region.move_to(plane.c2p(0, 0))

        s_label = formula(r"\mathbb{S}", 22, BLUE)
        s_label.move_to(plane.c2p(0, 0))

        self.play(FadeIn(plane), run_time=0.6)
        self.play(Create(feasible_region), Write(s_label), run_time=0.9)

        inside_dot = Dot(plane.c2p(0.4, 0.3), color=BLUE, radius=0.07)
        outside_dot = Dot(plane.c2p(1.9, 1.7), color=BLACK, radius=0.07)

        self.play(FadeIn(inside_dot), FadeIn(outside_dot), run_time=0.6)

        feasible_label = body("feasible", 13, BLUE)
        feasible_label.next_to(inside_dot, DOWN, buff=0.15)

        infeasible_label = body("infeasible", 13, BLACK)
        infeasible_label.next_to(outside_dot, UP, buff=0.15)

        self.play(Write(feasible_label), Write(infeasible_label), run_time=0.6)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 4 — NORM CONSTRAINT
        # ========================================================

        title = bold("A common constraint: bounded norm", 24)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        formula1 = formula(r"||x|| \leq 1", 30, BLUE)
        formula1.next_to(title, DOWN, buff=0.4)
        self.play(Write(formula1), run_time=0.9)

        plane2 = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=4.6, y_length=4.6,
            background_line_style={"stroke_color": BLACK, "stroke_width": 0.6, "stroke_opacity": 0.15},
            axis_config={"color": BLACK, "stroke_width": 1.4},
        )
        plane2.next_to(formula1, DOWN, buff=0.4)

        unit_disk = Circle(
            radius=1.2, color=BLUE, fill_color=BLUE, fill_opacity=0.12, stroke_width=3,
        )
        unit_disk.move_to(plane2.c2p(0, 0))

        self.play(FadeIn(plane2), run_time=0.6)
        self.play(Create(unit_disk), run_time=0.9)

        note = body("solutions restricted to the unit ball", 14, BLACK)
        fit_width(note, 6.5)
        note.next_to(plane2, DOWN, buff=0.35)
        self.play(Write(note), run_time=0.7)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 5 — PROJECTED GRADIENT DESCENT
        # ========================================================

        title = bold("Project after each gradient step", 24)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        plane3 = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5.0, y_length=4.6,
            background_line_style={"stroke_color": BLACK, "stroke_width": 0.6, "stroke_opacity": 0.15},
            axis_config={"color": BLACK, "stroke_width": 1.4},
        )
        plane3.next_to(title, DOWN, buff=0.5)

        region = Circle(
            radius=1.2, color=BLUE, fill_color=BLUE, fill_opacity=0.1, stroke_width=3,
        )
        region.move_to(plane3.c2p(0, 0))

        step_start = Dot(plane3.c2p(1.0, 0.8), color=BLACK, radius=0.07)
        step_grad = Dot(plane3.c2p(2.0, 1.6), color=BLACK, radius=0.07)
        step_proj = Dot(plane3.c2p(1.24, 0.99), color=BLUE, radius=0.07)

        arrow_step = Arrow(
            step_start.get_center(), step_grad.get_center(),
            color=BLACK, buff=0.08, stroke_width=3,
        )
        arrow_proj = DashedLine(
            step_grad.get_center(), step_proj.get_center(),
            color=BLUE, stroke_width=2.5,
        )

        self.play(FadeIn(plane3), Create(region), run_time=0.8)
        self.play(FadeIn(step_start), run_time=0.4)
        self.play(GrowArrow(arrow_step), FadeIn(step_grad), run_time=0.7)
        self.play(Create(arrow_proj), FadeIn(step_proj), run_time=0.7)

        gd_label = body("gradient step", 12, BLACK)
        gd_label.next_to(arrow_step, UP, buff=0.08)

        proj_label = body("project back into S", 12, BLUE)
        proj_label.next_to(step_proj, DOWN, buff=0.15)

        self.play(Write(gd_label), Write(proj_label), run_time=0.6)

        note = body("or: line-search only over feasible step sizes ε", 13, BLACK)
        fit_width(note, 6.5)
        note.next_to(plane3, DOWN, buff=0.35)
        self.play(Write(note), run_time=0.7)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 6 — FINAL MESSAGE
        # ========================================================

        final = bold(
            "Convexity buys guarantees.\nConstraints keep the search inside S.",
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
    Page_91().render()
