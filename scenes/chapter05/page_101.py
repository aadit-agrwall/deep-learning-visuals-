from manim import *
import numpy as np
import random

# ============================================================
# PAGE 101 — IMPUTATION (CONT.), DENOISING, DENSITY ESTIMATION,
#            5.1.2 THE PERFORMANCE MEASURE, P
# ============================================================

config.background_color = "#000000"
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60

random.seed(41)


class Page_101(MovingCameraScene):

    def construct(self):

        BLACK = "#000000"
        WHITE = "#F5F7FA"
        CYAN = "#4FD1FF"
        GREEN = "#65E572"
        YELLOW = "#FFD166"
        PURPLE = "#B388FF"
        RED = "#FF6B6B"

        self.camera.background_color = BLACK

        PAGE_NO = "101"

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
            Geometrical, linear wipe: every fragment travels the SAME
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
                anims.append(sm.animate.shift(travel).set_opacity(0))

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
        # SCENE 1 — IMPUTATION: WHAT THE ALGORITHM MUST DO
        # ============================================================

        title1 = txt("Imputation: predict the gaps", 25, WHITE, BOLD)
        title1.to_edge(UP, buff=0.6)
        type_in(title1, run_time=1.0)

        statement1 = txt(
            "the algorithm must provide a prediction\nof the values of the missing entries",
            18, CYAN,
        )
        statement1.next_to(title1, DOWN, buff=0.55)
        type_in(statement1, run_time=1.4)

        slots = VGroup()
        values = ["2.1", "?", "0.7", "5.3"]
        for v in values:
            box = Square(side_length=0.9, stroke_color=RED if v == "?" else WHITE, stroke_width=2.5,
                         fill_color=RED if v == "?" else BLACK, fill_opacity=0.15 if v == "?" else 0)
            label = txt(v, 20, RED if v == "?" else WHITE, BOLD)
            label.move_to(box.get_center())
            slots.add(VGroup(box, label))
        slots.arrange(RIGHT, buff=0.2)
        slots.next_to(statement1, DOWN, buff=0.6)

        self.play(FadeIn(slots, lag_ratio=0.1), run_time=0.9)

        fill_in = txt("4.2", 20, GREEN, BOLD)
        fill_in.move_to(slots[1][0].get_center())
        self.play(Transform(slots[1][1], fill_in), run_time=0.8)

        self.wait(1.1)
        dust_wipe([title1, statement1, slots])

        # ============================================================
        # SCENE 2 — DENOISING: THE SETUP
        # ============================================================

        title2 = txt("Denoising", 32, WHITE, BOLD)
        title2.to_edge(UP, buff=0.6)
        type_in(title2, run_time=1.0)

        corrupt_formula = formula(r"\tilde{\mathbf{x}} = \text{corrupt}(\mathbf{x})", 28, YELLOW)
        corrupt_formula.next_to(title2, DOWN, buff=0.6)
        self.play(Write(corrupt_formula), run_time=1.0)

        note2 = txt("a clean example x is corrupted\nby an unknown process", 17, WHITE)
        note2.next_to(corrupt_formula, DOWN, buff=0.5)
        type_in(note2, run_time=1.2)

        self.wait(1.0)
        dust_wipe([title2, corrupt_formula, note2])

        # ============================================================
        # SCENE 3 — DENOISING: RECOVER THE CLEAN EXAMPLE
        # ============================================================

        title3 = txt("Recover the clean example", 25, WHITE, BOLD)
        title3.to_edge(UP, buff=0.6)
        type_in(title3, run_time=1.0)

        # noisy grid -> clean grid
        random.seed(5)
        noisy_grid = VGroup()
        for i in range(4):
            for j in range(4):
                shade = random.uniform(0.1, 0.95)
                cell = Square(side_length=0.42, fill_color=RED, fill_opacity=shade * 0.5,
                             stroke_color=WHITE, stroke_width=1)
                cell.move_to(np.array([j * 0.42, -i * 0.42, 0]))
                noisy_grid.add(cell)
        noisy_grid.move_to(LEFT * 2.3 + DOWN * 0.2)
        noisy_label = txt("x̃  (corrupted)", 14, RED)
        noisy_label.next_to(noisy_grid, DOWN, buff=0.25)

        arrow3 = Arrow(LEFT * 0.7, RIGHT * 0.3, color=CYAN, stroke_width=4)
        arrow3.move_to(DOWN * 0.2)

        clean_grid = VGroup()
        random.seed(5)
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=0.42, fill_color=GREEN, fill_opacity=0.5,
                             stroke_color=WHITE, stroke_width=1)
                cell.move_to(np.array([j * 0.42, -i * 0.42, 0]))
                clean_grid.add(cell)
        clean_grid.move_to(RIGHT * 2.3 + DOWN * 0.2)
        clean_label = txt("x  (clean)", 14, GREEN)
        clean_label.next_to(clean_grid, DOWN, buff=0.25)

        self.play(FadeIn(noisy_grid, lag_ratio=0.04), run_time=0.9)
        type_in(noisy_label, run_time=0.6)
        self.play(GrowArrow(arrow3), run_time=0.5)
        self.play(FadeIn(clean_grid, lag_ratio=0.04), run_time=0.9)
        type_in(clean_label, run_time=0.6)

        distribution = formula(r"p(\mathbf{x} \mid \tilde{\mathbf{x}})", 26, PURPLE)
        distribution.next_to(VGroup(noisy_grid, clean_grid), DOWN, buff=0.7)
        self.play(Write(distribution), run_time=0.9)

        self.wait(1.1)
        dust_wipe([title3, noisy_grid, noisy_label, arrow3, clean_grid, clean_label, distribution])

        # ============================================================
        # SCENE 4 — DENSITY ESTIMATION: THE GOAL
        # ============================================================

        title4 = txt("Density estimation", 30, WHITE, BOLD)
        title4.to_edge(UP, buff=0.6)
        type_in(title4, run_time=1.0)

        statement4 = txt("learn a function that models\nthe shape of the data itself", 18, CYAN)
        statement4.next_to(title4, DOWN, buff=0.5)
        type_in(statement4, run_time=1.3)

        pmodel = formula(r"p_{\text{model}}: \mathbb{R}^n \rightarrow \mathbb{R}", 30, YELLOW)
        pmodel.next_to(statement4, DOWN, buff=0.55)
        self.play(Write(pmodel), run_time=1.0)

        note4 = txt("density (continuous x) or\nprobability mass (discrete x)", 16, WHITE)
        note4.next_to(pmodel, DOWN, buff=0.45)
        type_in(note4, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title4, statement4, pmodel, note4])

        # ============================================================
        # SCENE 5 — WHERE EXAMPLES CLUSTER
        # ============================================================

        title5 = txt("Where examples cluster", 28, WHITE, BOLD)
        title5.to_edge(UP, buff=0.6)
        type_in(title5, run_time=1.0)

        axes5 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
            x_length=6.4, y_length=3.2,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_numbers": False},
        )
        axes5.next_to(title5, DOWN, buff=0.5)

        density_curve = axes5.plot(
            lambda x: 0.35 * np.exp(-0.5 * ((x + 1.5) / 0.7) ** 2) + 0.25 * np.exp(-0.5 * ((x - 1.8) / 0.9) ** 2),
            x_range=[-4, 4], color=CYAN, stroke_width=3.5,
        )

        self.play(Create(axes5), run_time=0.6)
        self.play(Create(density_curve), run_time=1.1)

        tight_label = txt("tight cluster", 14, GREEN)
        tight_label.next_to(axes5.c2p(-1.5, 0.35), UP, buff=0.15)
        sparse_label = txt("unlikely region", 14, RED)
        sparse_label.next_to(axes5.c2p(0.2, 0.02), DOWN, buff=0.3)

        type_in(tight_label, run_time=0.6)
        type_in(sparse_label, run_time=0.6)

        self.wait(1.1)
        dust_wipe([title5, axes5, density_curve, tight_label, sparse_label])

        # ============================================================
        # SCENE 6 — DENSITY ESTIMATION SOLVES OTHER TASKS
        # ============================================================

        title6 = txt("One distribution, many tasks", 25, WHITE, BOLD)
        title6.to_edge(UP, buff=0.6)
        type_in(title6, run_time=1.0)

        center_box = RoundedRectangle(width=3.2, height=1.3, corner_radius=0.15, color=YELLOW, stroke_width=2.8)
        center_box.next_to(title6, DOWN, buff=0.7)
        center_text = formula(r"p(\mathbf{x})", 26, YELLOW)
        center_text.move_to(center_box.get_center())

        self.play(Create(center_box), Write(center_text), run_time=0.9)

        targets = [
            ("Imputation", CYAN, LEFT * 2.6 + DOWN * 1.6),
            ("Classification", GREEN, RIGHT * 2.6 + DOWN * 1.6),
            ("Anomaly detection", PURPLE, DOWN * 2.6),
        ]

        lines = VGroup()
        labels = VGroup()
        for label, color, pos in targets:
            dest = center_box.get_center() + pos
            line = Line(center_box.get_bottom(), dest, color=color, stroke_width=2)
            lbl = txt(label, 13, color)
            lbl.move_to(dest)
            lines.add(line)
            labels.add(lbl)

        self.play(*[Create(l) for l in lines], run_time=0.9)
        for lbl in labels:
            type_in(lbl, run_time=0.5)

        self.wait(1.1)
        dust_wipe([title6, center_box, center_text, lines, labels])

        # ============================================================
        # SCENE 7 — IMPUTATION VIA DENSITY ESTIMATION
        # ============================================================

        title7 = txt("Imputation via p(x)", 27, WHITE, BOLD)
        title7.to_edge(UP, buff=0.6)
        type_in(title7, run_time=1.0)

        conditional = formula(r"p(x_i \mid \mathbf{x}_{-i})", 32, CYAN)
        conditional.next_to(title7, DOWN, buff=0.65)
        self.play(Write(conditional), run_time=1.0)

        note7 = txt("the distribution over a missing xᵢ,\ngiven every other observed value", 17, WHITE)
        note7.next_to(conditional, DOWN, buff=0.5)
        type_in(note7, run_time=1.2)

        caveat = txt("not always tractable —\nsome operations on p(x) are too costly", 16, RED)
        caveat.next_to(note7, DOWN, buff=0.45)
        type_in(caveat, run_time=1.2)

        self.wait(1.1)
        dust_wipe([title7, conditional, note7, caveat])

        # ============================================================
        # SCENE 8 — NOT A RIGID TAXONOMY
        # ============================================================

        title8 = txt("Not a rigid taxonomy", 28, WHITE, BOLD)
        title8.to_edge(UP, buff=0.6)
        type_in(title8, run_time=1.0)

        note8 = txt(
            "many other task types are possible —\nthese are examples, not an exhaustive list",
            18, YELLOW,
        )
        note8.next_to(title8, DOWN, buff=0.6)
        type_in(note8, run_time=1.3)

        self.wait(1.0)
        dust_wipe([title8, note8])

        # ============================================================
        # SCENE 9 — 5.1.2 THE PERFORMANCE MEASURE, P
        # ============================================================

        title9 = txt("5.1.2  The Performance Measure, P", 23, WHITE, BOLD)
        title9.to_edge(UP, buff=0.6)
        type_in(title9, run_time=1.1)

        statement9 = txt(
            "a quantitative measure of ability —\nusually specific to the task T",
            18, CYAN,
        )
        statement9.next_to(title9, DOWN, buff=0.55)
        type_in(statement9, run_time=1.3)

        self.wait(1.0)
        dust_wipe([title9, statement9])

        # ============================================================
        # SCENE 10 — ACCURACY FOR CLASSIFICATION-LIKE TASKS
        # ============================================================

        title10 = txt("A common measure: accuracy", 25, WHITE, BOLD)
        title10.to_edge(UP, buff=0.6)
        type_in(title10, run_time=1.0)

        used_for = VGroup(
            txt("Classification", 16, CYAN, BOLD),
            txt("Classification w/ missing inputs", 16, YELLOW, BOLD),
            txt("Transcription", 16, GREEN, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        used_for.next_to(title10, DOWN, buff=0.55)

        for item in used_for:
            type_in(item, run_time=0.7)

        acc_box = RoundedRectangle(width=5.0, height=1.1, corner_radius=0.15, color=WHITE, stroke_width=2.5)
        acc_box.next_to(used_for, DOWN, buff=0.55)
        acc_text = txt("accuracy = ...", 18, WHITE)
        acc_text.move_to(acc_box.get_center())

        self.play(Create(acc_box), run_time=0.6)
        type_in(acc_text, run_time=0.8)

        self.wait(1.2)
        dust_wipe([title10, used_for, acc_box, acc_text])

        # ============================================================
        # SCENE 11 — FINAL MESSAGE
        # ============================================================

        final = txt(
            "To know if a model is learning,\nwe need a number that tells us so.",
            22, WHITE, BOLD,
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
    Page_101().render()
