from manim import *
import numpy as np
import random

# ============================================================
# PAGE 100 — STRUCTURED OUTPUT (CONT.), ANOMALY DETECTION,
#            SYNTHESIS & SAMPLING, IMPUTATION OF MISSING VALUES
# ============================================================

config.background_color = "#000000"
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60

random.seed(31)


class Page_100(MovingCameraScene):

    def construct(self):

        BLACK = "#000000"
        WHITE = "#F5F7FA"
        CYAN = "#4FD1FF"
        GREEN = "#65E572"
        YELLOW = "#FFD166"
        PURPLE = "#B388FF"
        RED = "#FF6B6B"

        self.camera.background_color = BLACK

        PAGE_NO = "100"

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
        # SCENE 1 — STRUCTURED OUTPUT: ANNOTATION EXAMPLE
        # ============================================================

        title1 = txt("Structured output: annotation", 25, WHITE, BOLD)
        title1.to_edge(UP, buff=0.6)
        type_in(title1, run_time=1.1)

        statement1 = txt("annotate road locations\nin aerial photographs", 19, CYAN)
        statement1.next_to(title1, DOWN, buff=0.5)
        type_in(statement1, run_time=1.2)

        # aerial photo with road overlay
        photo = Square(side_length=2.6, fill_color=GREEN, fill_opacity=0.25, stroke_color=WHITE, stroke_width=2)
        photo.next_to(statement1, DOWN, buff=0.5)
        road = Line(photo.get_corner(UL) + RIGHT * 0.3, photo.get_corner(DR) + LEFT * 0.3, color=YELLOW, stroke_width=5)

        self.play(Create(photo), run_time=0.7)
        self.play(Create(road), run_time=0.9)

        note1 = txt("output need not mirror the\ninput's structure so closely", 16, WHITE)
        note1.next_to(photo, DOWN, buff=0.4)
        type_in(note1, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title1, statement1, photo, road, note1])

        # ============================================================
        # SCENE 2 — STRUCTURED OUTPUT: IMAGE CAPTIONING
        # ============================================================

        title2 = txt("Example: image captioning", 27, WHITE, BOLD)
        title2.to_edge(UP, buff=0.6)
        type_in(title2, run_time=1.0)

        img_box = RoundedRectangle(width=2.8, height=2.0, corner_radius=0.12, color=CYAN, stroke_width=2.5)
        img_box.move_to(LEFT * 2.1 + DOWN * 0.2)
        img_icon = txt("🖼", 40)
        img_icon.move_to(img_box.get_center())

        arrow2 = Arrow(LEFT * 0.4, RIGHT * 0.6, color=YELLOW, stroke_width=4)
        arrow2.move_to(DOWN * 0.2)

        caption_box = RoundedRectangle(width=3.4, height=2.0, corner_radius=0.12, color=GREEN, stroke_width=2.5)
        caption_box.move_to(RIGHT * 2.3 + DOWN * 0.2)
        caption_text = txt("\"a dog\nrunning\nin a field\"", 15, WHITE)
        caption_text.move_to(caption_box.get_center())

        self.play(Create(img_box), FadeIn(img_icon), run_time=0.8)
        self.play(GrowArrow(arrow2), run_time=0.6)
        self.play(Create(caption_box), run_time=0.6)
        type_in(caption_text, run_time=1.1)

        note2 = txt("the words must form a\nvalid, coherent sentence", 17, WHITE)
        note2.next_to(VGroup(img_box, caption_box), DOWN, buff=0.9)
        type_in(note2, run_time=1.0)

        self.wait(1.1)
        dust_wipe([title2, img_box, img_icon, arrow2, caption_box, caption_text, note2])

        # ============================================================
        # SCENE 3 — WHY "STRUCTURED": TIGHT INTERRELATIONS
        # ============================================================

        title3 = txt("Why \"structured\"?", 28, WHITE, BOLD)
        title3.to_edge(UP, buff=0.6)
        type_in(title3, run_time=1.0)

        struct_box = RoundedRectangle(width=7.2, height=1.8, corner_radius=0.16, color=PURPLE, stroke_width=2.5)
        struct_box.next_to(title3, DOWN, buff=0.6)
        struct_text = txt("several output values —\nall tightly interrelated with each other", 18, WHITE)
        struct_text.move_to(struct_box.get_center())

        self.play(Create(struct_box), run_time=0.7)
        type_in(struct_text, run_time=1.2)

        self.wait(1.0)
        dust_wipe([title3, struct_box, struct_text])

        # ============================================================
        # SCENE 4 — ANOMALY DETECTION
        # ============================================================

        title4 = txt("Anomaly detection", 30, WHITE, BOLD)
        title4.to_edge(UP, buff=0.6)
        type_in(title4, run_time=1.0)

        statement4 = txt("sift through events and flag\nwhat's unusual or atypical", 19, CYAN)
        statement4.next_to(title4, DOWN, buff=0.55)
        type_in(statement4, run_time=1.3)

        self.wait(1.0)
        dust_wipe([title4, statement4])

        # ============================================================
        # SCENE 5 — ANOMALY DETECTION: CREDIT CARD FRAUD
        # ============================================================

        title5 = txt("Example: credit card fraud", 26, WHITE, BOLD)
        title5.to_edge(UP, buff=0.6)
        type_in(title5, run_time=1.0)

        axes5 = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=6.4, y_length=4.2,
            axis_config={"color": WHITE, "stroke_width": 1.4, "include_numbers": False},
        )
        axes5.next_to(title5, DOWN, buff=0.5)

        random.seed(8)
        normal_pts = VGroup()
        for _ in range(24):
            x = random.gauss(4, 1.0)
            y = random.gauss(4, 1.0)
            normal_pts.add(Dot(axes5.c2p(x, y), radius=0.05, color=CYAN))

        anomaly_pt = Dot(axes5.c2p(8.5, 8.7), radius=0.09, color=RED)
        anomaly_label = txt("uncharacteristic\npurchase", 14, RED)
        anomaly_label.next_to(anomaly_pt, UR, buff=0.15)

        self.play(Create(axes5), run_time=0.6)
        self.play(FadeIn(normal_pts, lag_ratio=0.05), run_time=1.0)
        self.play(FadeIn(anomaly_pt, scale=2), run_time=0.6)
        type_in(anomaly_label, run_time=0.8)

        self.wait(1.1)
        dust_wipe([title5, axes5, normal_pts, anomaly_pt, anomaly_label])

        # ============================================================
        # SCENE 6 — HOW FRAUD DETECTION WORKS
        # ============================================================

        title6 = txt("Different purchase distribution", 24, WHITE, BOLD)
        title6.to_edge(UP, buff=0.6)
        type_in(title6, run_time=1.0)

        step1 = txt("model your normal purchasing habits", 17, CYAN)
        step1.next_to(title6, DOWN, buff=0.5)
        type_in(step1, run_time=1.0)

        step2 = txt("a thief's purchases come from a\ndifferent probability distribution", 17, YELLOW)
        step2.next_to(step1, DOWN, buff=0.45)
        type_in(step2, run_time=1.2)

        step3 = txt("place a hold as soon as the card\nis used uncharacteristically", 17, RED)
        step3.next_to(step2, DOWN, buff=0.45)
        type_in(step3, run_time=1.2)

        self.wait(1.1)
        dust_wipe([title6, step1, step2, step3])

        # ============================================================
        # SCENE 7 — SYNTHESIS AND SAMPLING
        # ============================================================

        title7 = txt("Synthesis and sampling", 28, WHITE, BOLD)
        title7.to_edge(UP, buff=0.6)
        type_in(title7, run_time=1.0)

        statement7 = txt("generate new examples similar\nto the training data", 19, CYAN)
        statement7.next_to(title7, DOWN, buff=0.55)
        type_in(statement7, run_time=1.2)

        why_box = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=GREEN, stroke_width=2.5)
        why_box.next_to(statement7, DOWN, buff=0.5)
        why_text = txt("useful when generating content\nby hand is expensive or boring", 16, WHITE)
        why_text.move_to(why_box.get_center())

        self.play(Create(why_box), run_time=0.6)
        type_in(why_text, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title7, statement7, why_box, why_text])

        # ============================================================
        # SCENE 8 — SYNTHESIS EXAMPLE: TEXTURES
        # ============================================================

        title8 = txt("Example: procedural textures", 25, WHITE, BOLD)
        title8.to_edge(UP, buff=0.6)
        type_in(title8, run_time=1.0)

        texture_grid = VGroup()
        random.seed(19)
        for i in range(5):
            for j in range(5):
                shade = random.uniform(0.2, 0.7)
                cell = Square(side_length=0.5, fill_color=GREEN, fill_opacity=shade, stroke_color=WHITE, stroke_width=0.8)
                cell.move_to(np.array([j * 0.5, -i * 0.5, 0]))
                texture_grid.add(cell)
        texture_grid.move_to(ORIGIN)
        texture_grid.next_to(title8, DOWN, buff=0.55)

        self.play(FadeIn(texture_grid, lag_ratio=0.04), run_time=1.0)

        note8 = txt("video games auto-generate textures for\nlarge objects and landscapes", 16, WHITE)
        note8.next_to(texture_grid, DOWN, buff=0.45)
        type_in(note8, run_time=1.2)

        self.wait(1.1)
        dust_wipe([title8, texture_grid, note8])

        # ============================================================
        # SCENE 9 — SYNTHESIS EXAMPLE: SPEECH SYNTHESIS
        # ============================================================

        title9 = txt("Example: speech synthesis", 26, WHITE, BOLD)
        title9.to_edge(UP, buff=0.6)
        type_in(title9, run_time=1.0)

        written = txt("\"Good morning\"", 18, WHITE, font="DejaVu Sans Mono")
        written.next_to(title9, DOWN, buff=0.5)
        type_in(written, run_time=0.9)

        arrow9 = txt("↓", 26, YELLOW)
        arrow9.next_to(written, DOWN, buff=0.3)
        self.play(FadeIn(arrow9, shift=DOWN * 0.15), run_time=0.5)

        wave_axes9 = Axes(
            x_range=[0, 8, 2], y_range=[-1, 1, 1],
            x_length=5.6, y_length=1.6,
            axis_config={"color": WHITE, "stroke_width": 1.0, "include_numbers": False},
        )
        wave_axes9.next_to(arrow9, DOWN, buff=0.3)
        waveform9 = wave_axes9.plot(
            lambda x: 0.5 * np.sin(4 * x) * np.exp(-0.03 * x),
            x_range=[0, 8], color=GREEN, stroke_width=3,
        )
        self.play(Create(wave_axes9), Create(waveform9), run_time=1.0)

        note9 = txt("no single correct output —\nvariation makes it sound natural", 15, WHITE)
        note9.next_to(wave_axes9, DOWN, buff=0.4)
        type_in(note9, run_time=1.1)

        self.wait(1.2)
        dust_wipe([title9, written, arrow9, wave_axes9, waveform9, note9])

        # ============================================================
        # SCENE 10 — IMPUTATION OF MISSING VALUES
        # ============================================================

        title10 = txt("Imputation of missing values", 25, WHITE, BOLD)
        title10.to_edge(UP, buff=0.6)
        type_in(title10, run_time=1.1)

        vec_formula = formula(r"\mathbf{x} \in \mathbb{R}^n", 32, CYAN)
        vec_formula.next_to(title10, DOWN, buff=0.6)
        self.play(Write(vec_formula), run_time=0.9)

        note10 = txt("some entries xᵢ of x are missing —\nthe algorithm must fill them in", 18, WHITE)
        note10.next_to(vec_formula, DOWN, buff=0.5)
        type_in(note10, run_time=1.2)

        # visual: vector with a missing slot
        slots = VGroup()
        values = ["2.1", "?", "0.7", "5.3"]
        for i, v in enumerate(values):
            box = Square(side_length=0.9, stroke_color=RED if v == "?" else WHITE, stroke_width=2.5,
                         fill_color=RED if v == "?" else BLACK, fill_opacity=0.15 if v == "?" else 0)
            label = txt(v, 20, RED if v == "?" else WHITE, BOLD)
            label.move_to(box.get_center())
            slots.add(VGroup(box, label))
        slots.arrange(RIGHT, buff=0.2)
        slots.next_to(note10, DOWN, buff=0.5)

        self.play(FadeIn(slots, lag_ratio=0.1), run_time=1.0)

        self.wait(1.2)
        dust_wipe([title10, vec_formula, note10, slots])

        # ============================================================
        # SCENE 11 — FINAL MESSAGE
        # ============================================================

        final = txt(
            "From flagging outliers to filling gaps —\nML tasks stretch far beyond prediction.",
            21, WHITE, BOLD,
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
    Page_100().render()
