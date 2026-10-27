from manim import *
import numpy as np
import random

# ============================================================
# PAGE 98 — CLASSIFICATION & CLASSIFICATION WITH MISSING INPUTS
# ============================================================

config.background_color = "#000000"
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60

random.seed(11)


class Page_98(MovingCameraScene):

    def construct(self):

        BLACK = "#000000"
        WHITE = "#F5F7FA"
        CYAN = "#4FD1FF"
        GREEN = "#65E572"
        YELLOW = "#FFD166"
        PURPLE = "#B388FF"
        RED = "#FF6B6B"

        self.camera.background_color = BLACK

        PAGE_NO = "98"

        # --------------------------------------------------------
        # Helpers
        # --------------------------------------------------------

        def txt(text, size=26, color=WHITE, weight=NORMAL, font="DejaVu Serif"):
            return Text(text, font=font, font_size=size, color=color, weight=weight)

        def formula(tex, size=32, color=WHITE):
            return MathTex(tex, font_size=size, color=color)

        def fit_width(obj, width=7.4):
            if obj.width > width:
                obj.scale_to_fit_width(width)
            return obj

        def type_in(mobj, run_time=1.2):
            self.play(AddTextLetterByLetter(mobj), run_time=run_time)

        def dust_wipe(mobjects, run_time=2.0):
            """
            Geometrical, linear wipe: every fragment travels in the SAME
            direction (left -> right) at a constant (linear) rate, with a
            small per-fragment stagger based on horizontal position so the
            wipe reads as a single clean sweep rather than an explosion.
            """
            targets = []
            for m in mobjects:
                if len(m.submobjects) > 0:
                    targets.extend(m.family_members_with_points())
                else:
                    targets.append(m)
            if not targets:
                return

            all_x = [sm.get_center()[0] for sm in targets]
            min_x, max_x = min(all_x), max(all_x)
            span = max(max_x - min_x, 0.01)

            travel = RIGHT * 9.5
            anims = []
            lag_ratios = []
            for sm in targets:
                x = sm.get_center()[0]
                lag_ratios.append((x - min_x) / span)
                anims.append(
                    sm.animate.shift(travel).set_opacity(0)
                )

            order = np.argsort(lag_ratios)
            ordered_anims = [anims[i] for i in order]

            self.play(
                LaggedStart(*ordered_anims, lag_ratio=0.02),
                run_time=run_time,
                rate_func=linear,
            )
            self.remove(*mobjects)

        def make_footer():
            f = txt(f"ML-{PAGE_NO}", 20, GREEN, font="DejaVu Sans Mono")
            f.to_edge(DOWN, buff=0.35)
            return f

        footer = make_footer()
        self.add(footer)

        # ============================================================
        # SCENE 1 — SECTION RECAP: MANY KINDS OF TASKS
        # ============================================================

        title1 = txt("Many kinds of tasks", 30, WHITE, BOLD)
        title1.to_edge(UP, buff=0.6)
        type_in(title1, run_time=1.0)

        statement = txt("some of the most common\nmachine learning tasks:", 20, YELLOW)
        statement.next_to(title1, DOWN, buff=0.5)
        type_in(statement, run_time=1.2)

        self.wait(0.9)
        dust_wipe([title1, statement])

        # ============================================================
        # SCENE 2 — CLASSIFICATION: THE FUNCTION
        # ============================================================

        title2 = txt("Classification", 32, WHITE, BOLD)
        title2.to_edge(UP, buff=0.6)
        type_in(title2, run_time=1.0)

        statement2 = txt("assign an input to one of k categories", 19, CYAN)
        fit_width(statement2, 7.2)
        statement2.next_to(title2, DOWN, buff=0.5)
        type_in(statement2, run_time=1.2)

        func_formula = formula(r"f: \mathbb{R}^n \rightarrow \{1, \ldots, k\}", 34, YELLOW)
        func_formula.next_to(statement2, DOWN, buff=0.6)
        self.play(Write(func_formula), run_time=1.0)

        y_formula = formula(r"y = f(\mathbf{x})", 30, WHITE)
        y_formula.next_to(func_formula, DOWN, buff=0.5)
        self.play(Write(y_formula), run_time=0.8)

        note2 = txt("x → category, identified by code y", 18, WHITE)
        fit_width(note2, 7.0)
        note2.next_to(y_formula, DOWN, buff=0.4)
        type_in(note2, run_time=1.0)

        self.wait(1.0)
        dust_wipe([title2, statement2, func_formula, y_formula, note2])

        # ============================================================
        # SCENE 3 — VARIANT: PROBABILITY DISTRIBUTION OUTPUT
        # ============================================================

        title3 = txt("A common variant", 30, WHITE, BOLD)
        title3.to_edge(UP, buff=0.6)
        type_in(title3, run_time=0.9)

        variant_box = RoundedRectangle(width=7.2, height=1.9, corner_radius=0.16, color=PURPLE, stroke_width=2.5)
        variant_box.next_to(title3, DOWN, buff=0.6)

        variant_text = txt("f outputs a full probability\ndistribution over the k classes", 18, WHITE)
        variant_text.move_to(variant_box.get_center())

        self.play(Create(variant_box), run_time=0.7)
        type_in(variant_text, run_time=1.2)

        self.wait(1.0)
        dust_wipe([title3, variant_box, variant_text])

        # ============================================================
        # SCENE 4 — EXAMPLE: OBJECT RECOGNITION
        # ============================================================

        title4 = txt("Example: object recognition", 27, WHITE, BOLD)
        title4.to_edge(UP, buff=0.6)
        type_in(title4, run_time=1.0)

        # image -> pixels -> label pipeline
        pixel_grid = VGroup()
        random.seed(4)
        for i in range(4):
            for j in range(4):
                shade = random.uniform(0.15, 0.9)
                cell = Square(side_length=0.42, fill_color=CYAN, fill_opacity=shade, stroke_color=WHITE, stroke_width=1)
                cell.move_to(np.array([j * 0.42, -i * 0.42, 0]))
                pixel_grid.add(cell)
        pixel_grid.move_to(LEFT * 2.4 + DOWN * 0.2)

        arrow = Arrow(LEFT * 0.7, RIGHT * 0.3, color=YELLOW, stroke_width=4)
        arrow.move_to(DOWN * 0.2)

        label_box = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.14, color=GREEN, stroke_width=2.5)
        label_box.move_to(RIGHT * 2.4 + DOWN * 0.2)
        label_text = txt("\"cup\"", 20, GREEN, BOLD)
        label_text.move_to(label_box.get_center())

        self.play(FadeIn(pixel_grid, lag_ratio=0.05), run_time=1.0)
        self.play(GrowArrow(arrow), run_time=0.6)
        self.play(Create(label_box), Write(label_text), run_time=0.8)

        note4 = txt("input: pixel brightness values\noutput: a numeric object code", 17, WHITE)
        note4.next_to(pixel_grid, DOWN, buff=1.0).align_to(pixel_grid, LEFT).shift(RIGHT * 0.5)
        fit_width(note4, 7.0)
        note4.next_to(VGroup(pixel_grid, arrow, label_box), DOWN, buff=0.6)
        type_in(note4, run_time=1.2)

        self.wait(1.1)
        dust_wipe([title4, pixel_grid, arrow, label_box, label_text, note4])

        # ============================================================
        # SCENE 5 — REAL-WORLD APPLICATIONS
        # ============================================================

        title5 = txt("Real-world applications", 28, WHITE, BOLD)
        title5.to_edge(UP, buff=0.6)
        type_in(title5, run_time=1.0)

        app1 = RoundedRectangle(width=7.2, height=1.5, corner_radius=0.15, color=CYAN, stroke_width=2.5)
        app1.next_to(title5, DOWN, buff=0.5)
        app1_text = txt("Willow Garage PR2: a waiter robot that\nrecognizes drinks and delivers them", 16, WHITE)
        app1_text.move_to(app1.get_center())

        app2 = RoundedRectangle(width=7.2, height=1.3, corner_radius=0.15, color=YELLOW, stroke_width=2.5)
        app2.next_to(app1, DOWN, buff=0.35)
        app2_text = txt("Modern object recognition: powered\nby deep learning", 16, WHITE)
        app2_text.move_to(app2.get_center())

        app3 = RoundedRectangle(width=7.2, height=1.3, corner_radius=0.15, color=GREEN, stroke_width=2.5)
        app3.next_to(app2, DOWN, buff=0.35)
        app3_text = txt("Face recognition: auto-tagging photos,\nmore natural human-computer interaction", 15, WHITE)
        app3_text.move_to(app3.get_center())

        self.play(Create(app1), run_time=0.6)
        type_in(app1_text, run_time=1.1)
        self.play(Create(app2), run_time=0.6)
        type_in(app2_text, run_time=0.9)
        self.play(Create(app3), run_time=0.6)
        type_in(app3_text, run_time=1.0)

        self.wait(1.1)
        dust_wipe([title5, app1, app1_text, app2, app2_text, app3, app3_text])

        # ============================================================
        # SCENE 6 — CLASSIFICATION WITH MISSING INPUTS
        # ============================================================

        title6 = txt("Classification with missing inputs", 24, WHITE, BOLD)
        title6.to_edge(UP, buff=0.6)
        type_in(title6, run_time=1.1)

        problem = txt("not every measurement is\nalways guaranteed to be provided", 18, RED)
        problem.next_to(title6, DOWN, buff=0.5)
        type_in(problem, run_time=1.2)

        self.wait(1.0)
        dust_wipe([title6, problem])

        # ============================================================
        # SCENE 7 — SINGLE FUNCTION VS SET OF FUNCTIONS
        # ============================================================

        title7 = txt("One function becomes many", 27, WHITE, BOLD)
        title7.to_edge(UP, buff=0.6)
        type_in(title7, run_time=1.0)

        single_box = RoundedRectangle(width=6.9, height=1.4, corner_radius=0.15, color=GREEN, stroke_width=2.5)
        single_box.next_to(title7, DOWN, buff=0.5)
        single_text = txt("complete inputs → a single function", 17, WHITE)
        single_text.move_to(single_box.get_center())

        self.play(Create(single_box), run_time=0.6)
        type_in(single_text, run_time=1.0)

        arrow7 = txt("↓ some inputs missing ↓", 16, YELLOW)
        arrow7.next_to(single_box, DOWN, buff=0.35)
        type_in(arrow7, run_time=0.8)

        multi_box = RoundedRectangle(width=6.9, height=1.6, corner_radius=0.15, color=PURPLE, stroke_width=2.5)
        multi_box.next_to(arrow7, DOWN, buff=0.35)
        multi_text = txt("a whole SET of functions —\none per possible subset of missing inputs", 16, WHITE)
        multi_text.move_to(multi_box.get_center())

        self.play(Create(multi_box), run_time=0.6)
        type_in(multi_text, run_time=1.2)

        self.wait(1.1)
        dust_wipe([title7, single_box, single_text, arrow7, multi_box, multi_text])

        # ============================================================
        # SCENE 8 — WHY THIS MATTERS: MEDICAL DIAGNOSIS
        # ============================================================

        title8 = txt("A common real-world case", 27, WHITE, BOLD)
        title8.to_edge(UP, buff=0.6)
        type_in(title8, run_time=1.0)

        medical_box = RoundedRectangle(width=7.0, height=1.8, corner_radius=0.16, color=RED, stroke_width=2.5)
        medical_box.next_to(title8, DOWN, buff=0.6)
        medical_text = txt("medical diagnosis:\nmany tests are expensive or invasive", 18, WHITE)
        medical_text.move_to(medical_box.get_center())

        self.play(Create(medical_box), run_time=0.7)
        type_in(medical_text, run_time=1.2)

        self.wait(1.0)
        dust_wipe([title8, medical_box, medical_text])

        # ============================================================
        # SCENE 9 — THE EFFICIENT SOLUTION: JOINT DISTRIBUTION
        # ============================================================

        title9 = txt("An efficient way to define this set", 24, WHITE, BOLD)
        title9.to_edge(UP, buff=0.6)
        type_in(title9, run_time=1.1)

        step1 = txt("learn one joint probability distribution\nover all relevant variables", 18, CYAN)
        step1.next_to(title9, DOWN, buff=0.55)
        type_in(step1, run_time=1.3)

        step2 = txt("classify by marginalizing out\nthe missing variables", 18, YELLOW)
        step2.next_to(step1, DOWN, buff=0.45)
        type_in(step2, run_time=1.2)

        formula9 = formula(r"n \text{ inputs} \rightarrow 2^n \text{ classification functions}", 22, GREEN)
        fit_width(formula9, 7.0)
        formula9.next_to(step2, DOWN, buff=0.5)
        self.play(Write(formula9), run_time=1.0)

        note9 = txt("but only ONE function to learn:\nthe joint distribution itself", 16, WHITE)
        note9.next_to(formula9, DOWN, buff=0.4)
        type_in(note9, run_time=1.1)

        self.wait(1.2)
        dust_wipe([title9, step1, step2, formula9, note9])

        # ============================================================
        # SCENE 10 — FINAL MESSAGE
        # ============================================================

        final = txt(
            "Classification assigns categories —\neven when some inputs go missing.",
            24, WHITE, BOLD,
        )
        fit_width(final, 7.2)
        final.move_to(ORIGIN)

        type_in(final, run_time=1.6)
        self.wait(0.3)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.play(self.camera.frame.animate.scale(0.9), run_time=0.8)
        self.wait(1.8)


if __name__ == "__main__":
    Page_98().render()
