from manim import *
import numpy as np

# ============================================================
# PAGE 95 — SOLVING THE CONSTRAINED LEAST SQUARES PROBLEM
# ============================================================

config.background_color = WHITE
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60


class Page_95(Scene):

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
        # SCENE 1 — DIFFERENTIATE THE LAGRANGIAN (4.25)
        # ========================================================

        title = bold("Differentiate the Lagrangian w.r.t. x", 24)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        intro = body("assuming the constraint is active", 16, BLACK)
        intro.next_to(title, DOWN, buff=0.4)
        self.play(Write(intro), run_time=0.7)

        stationarity = formula(r"A^\top A x - A^\top b + 2\lambda x = 0", 24, BLUE)
        fit_width(stationarity, 6.9)
        stationarity.next_to(intro, DOWN, buff=0.55)
        self.play(Write(stationarity), run_time=1.1)

        eq_num1 = body("(4.25)", 14, BLACK)
        eq_num1.next_to(stationarity, DOWN, buff=0.3)
        self.play(Write(eq_num1), run_time=0.4)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 2 — SOLUTION FORM (4.26)
        # ========================================================

        title = bold("The solution takes this form", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        solution = formula(r"x = (A^\top A + 2\lambda I)^{-1} A^\top b", 26, BLUE)
        fit_width(solution, 6.9)
        solution.next_to(title, DOWN, buff=0.6)
        self.play(Write(solution), run_time=1.1)

        eq_num2 = body("(4.26)", 14, BLACK)
        eq_num2.next_to(solution, DOWN, buff=0.3)
        self.play(Write(eq_num2), run_time=0.4)

        note = body("λ must be chosen so this x obeys the constraint", 16, BLACK)
        fit_width(note, 6.7)
        note.next_to(eq_num2, DOWN, buff=0.5)
        self.play(Write(note), run_time=0.9)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 3 — GRADIENT ASCENT ON LAMBDA (4.27)
        # ========================================================

        title = bold("Find λ by gradient ascent", 26)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        partial = formula(r"\frac{\partial}{\partial \lambda} L(x,\lambda) = x^\top x - 1", 26, BLUE)
        fit_width(partial, 6.9)
        partial.next_to(title, DOWN, buff=0.6)
        self.play(Write(partial), run_time=1.1)

        eq_num3 = body("(4.27)", 14, BLACK)
        eq_num3.next_to(partial, DOWN, buff=0.3)
        self.play(Write(eq_num3), run_time=0.4)

        note = body("ascend on λ  →  push toward the correct norm", 16, BLACK)
        fit_width(note, 6.7)
        note.next_to(eq_num3, DOWN, buff=0.5)
        self.play(Write(note), run_time=0.9)

        self.wait(1.3)
        clear_scene()

        # ========================================================
        # SCENE 4 — THE FEEDBACK LOOP: NORM TOO BIG -> RAISE LAMBDA
        # ========================================================

        title = bold("The adjustment loop", 27)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        box1 = RoundedRectangle(
            width=6.6, height=1.3, corner_radius=0.15,
            color=BLACK, stroke_width=2.3,
        )
        box1.next_to(title, DOWN, buff=0.5)

        box1_text = formula(r"||x||^2 > 1 \Rightarrow \frac{\partial L}{\partial \lambda} > 0", 20, BLACK)
        box1_text.move_to(box1.get_center())

        self.play(Create(box1), Write(box1_text), run_time=1.0)

        arrow1 = Arrow(
            box1.get_bottom(), box1.get_bottom() + DOWN * 0.4,
            color=BLUE, stroke_width=3, buff=0.05,
        )
        self.play(Create(arrow1), run_time=0.4)

        box2 = RoundedRectangle(
            width=6.6, height=1.1, corner_radius=0.15,
            color=BLUE, stroke_width=2.5,
        )
        box2.next_to(box1, DOWN, buff=0.6)

        box2_text = body("increase λ", 20, BLUE)
        box2_text.move_to(box2.get_center())

        self.play(Create(box2), Write(box2_text), run_time=0.9)

        arrow2 = Arrow(
            box2.get_bottom(), box2.get_bottom() + DOWN * 0.4,
            color=BLUE, stroke_width=3, buff=0.05,
        )
        self.play(Create(arrow2), run_time=0.4)

        box3 = RoundedRectangle(
            width=6.6, height=1.3, corner_radius=0.15,
            color=BLACK, stroke_width=2.3,
        )
        box3.next_to(box2, DOWN, buff=0.6)

        box3_text = body("stronger penalty on x⊤x\n→ smaller-norm solution", 16, BLACK)
        box3_text.move_to(box3.get_center())

        self.play(Create(box3), Write(box3_text), run_time=1.0)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 5 — CONVERGENCE: WHEN TO STOP
        # ========================================================

        title = bold("Repeat until convergence", 27)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        loop_note = body("solve for x, adjust λ, repeat", 18, BLACK)
        loop_note.next_to(title, DOWN, buff=0.5)
        self.play(Write(loop_note), run_time=0.8)

        stop_box = RoundedRectangle(
            width=6.8, height=1.6, corner_radius=0.16,
            color=BLUE, stroke_width=2.5,
        )
        stop_box.next_to(loop_note, DOWN, buff=0.5)

        stop_title = bold("Stop when", 19, BLUE)
        stop_title.move_to(stop_box.get_center() + UP * 0.35)

        stop_formula = formula(r"x \text{ has correct norm, and } \frac{\partial L}{\partial \lambda} = 0", 17, BLACK)
        fit_width(stop_formula, 6.4)
        stop_formula.move_to(stop_box.get_center() + DOWN * 0.3)

        self.play(Create(stop_box), Write(stop_title), Write(stop_formula), run_time=1.1)

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 6 — CHAPTER 4 WRAP-UP
        # ========================================================

        title = bold("End of the mathematical preliminaries", 22)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        recap = body(
            "Linear algebra, probability, information theory,\nand numerical computation are now in place.",
            17, BLACK,
        )
        fit_width(recap, 6.7)
        recap.next_to(title, DOWN, buff=0.6)
        self.play(Write(recap), run_time=1.1)

        next_box = RoundedRectangle(
            width=6.6, height=1.5, corner_radius=0.15,
            color=BLACK, stroke_width=2.5,
        )
        next_box.next_to(recap, DOWN, buff=0.6)

        next_text = bold("Ready to build\nfull-fledged learning systems", 18, BLUE)
        next_text.move_to(next_box.get_center())

        self.play(Create(next_box), Write(next_text), run_time=1.0)

        self.wait(1.5)
        clear_scene()

        # ========================================================
        # SCENE 7 — FINAL MESSAGE
        # ========================================================

        final = bold(
            "Adjust λ until the constraint is\nsatisfied exactly, not just approximately.",
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
    Page_95().render()
