from manim import *
import numpy as np
import random

# ============================================================
# PAGE 99 — REGRESSION, TRANSCRIPTION, MACHINE TRANSLATION,
#           STRUCTURED OUTPUT
# ============================================================

config.background_color = "#000000"
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60

random.seed(21)


class Page_99(MovingCameraScene):

    def construct(self):

        BLACK = "#000000"
        WHITE = "#F5F7FA"
        CYAN = "#4FD1FF"
        GREEN = "#65E572"
        YELLOW = "#FFD166"
        PURPLE = "#B388FF"
        RED = "#FF6B6B"

        self.camera.background_color = BLACK

        PAGE_NO = "99"

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
        # SCENE 1 — REGRESSION
        # ============================================================

        title1 = txt("Regression", 32, WHITE, BOLD)
        title1.to_edge(UP, buff=0.6)
        type_in(title1, run_time=1.0)

        statement1 = txt("predict a numerical value given some input", 19, CYAN)
        fit_width(statement1, 7.2)
        statement1.next_to(title1, DOWN, buff=0.5)
        type_in(statement1, run_time=1.2)

        func1 = formula(r"f: \mathbb{R}^n \rightarrow \mathbb{R}", 34, YELLOW)
        func1.next_to(statement1, DOWN, buff=0.6)
        self.play(Write(func1), run_time=1.0)

        note1 = txt("like classification, but the\noutput format is different", 18, WHITE)
        note1.next_to(func1, DOWN, buff=0.5)
        type_in(note1, run_time=1.1)

        self.wait(1.0)
        dust_wipe([title1, statement1, func1, note1])

        # ============================================================
        # SCENE 2 — REGRESSION EXAMPLES
        # ============================================================

        title2 = txt("Regression in practice", 28, WHITE, BOLD)
        title2.to_edge(UP, buff=0.6)
        type_in(title2, run_time=1.0)

        ex1 = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=GREEN, stroke_width=2.5)
        ex1.next_to(title2, DOWN, buff=0.55)
        ex1_text = txt("expected insurance claim amount\n(sets insurance premiums)", 16, WHITE)
        ex1_text.move_to(ex1.get_center())

        ex2 = RoundedRectangle(width=7.0, height=1.5, corner_radius=0.15, color=PURPLE, stroke_width=2.5)
        ex2.next_to(ex1, DOWN, buff=0.4)
        ex2_text = txt("future prices of securities\n(used in algorithmic trading)", 16, WHITE)
        ex2_text.move_to(ex2.get_center())

        self.play(Create(ex1), run_time=0.6)
        type_in(ex1_text, run_time=1.0)
        self.play(Create(ex2), run_time=0.6)
        type_in(ex2_text, run_time=1.0)

        self.wait(1.1)
        dust_wipe([title2, ex1, ex1_text, ex2, ex2_text])

        # ============================================================
        # SCENE 3 — TRANSCRIPTION: THE TASK
        # ============================================================

        title3 = txt("Transcription", 32, WHITE, BOLD)
        title3.to_edge(UP, buff=0.6)
        type_in(title3, run_time=1.0)

        statement3 = txt(
            "observe an unstructured representation\nand transcribe it into discrete text",
            19, CYAN,
        )
        statement3.next_to(title3, DOWN, buff=0.55)
        type_in(statement3, run_time=1.4)

        self.wait(1.0)
        dust_wipe([title3, statement3])

        # ============================================================
        # SCENE 4 — TRANSCRIPTION EXAMPLE: OCR
        # ============================================================

        title4 = txt("Example: optical character recognition", 22, WHITE, BOLD)
        title4.to_edge(UP, buff=0.6)
        type_in(title4, run_time=1.1)

        photo_box = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.12, color=WHITE, stroke_width=2.5)
        photo_box.move_to(LEFT * 2.2 + DOWN * 0.1)
        photo_text = txt("ABC", 26, WHITE, BOLD)
        photo_text.move_to(photo_box.get_center())
        photo_label = txt("photograph", 13, WHITE)
        photo_label.next_to(photo_box, DOWN, buff=0.2)

        arrow4 = Arrow(LEFT * 0.6, RIGHT * 0.4, color=YELLOW, stroke_width=4)
        arrow4.move_to(DOWN * 0.1)

        code_box = RoundedRectangle(width=2.8, height=1.6, corner_radius=0.12, color=GREEN, stroke_width=2.5)
        code_box.move_to(RIGHT * 2.3 + DOWN * 0.1)
        code_text = txt("\"A B C\"", 20, GREEN, BOLD, font="DejaVu Sans Mono")
        code_text.move_to(code_box.get_center())
        code_label = txt("ASCII / Unicode", 13, WHITE)
        code_label.next_to(code_box, DOWN, buff=0.2)

        self.play(Create(photo_box), Write(photo_text), run_time=0.9)
        type_in(photo_label, run_time=0.6)
        self.play(GrowArrow(arrow4), run_time=0.6)
        self.play(Create(code_box), Write(code_text), run_time=0.9)
        type_in(code_label, run_time=0.6)

        note4 = txt("Google Street View reads address\nnumbers this way", 16, WHITE)
        note4.next_to(VGroup(photo_box, code_box), DOWN, buff=0.9)
        type_in(note4, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title4, photo_box, photo_text, photo_label, arrow4, code_box, code_text, code_label, note4])

        # ============================================================
        # SCENE 5 — TRANSCRIPTION EXAMPLE: SPEECH RECOGNITION
        # ============================================================

        title5 = txt("Example: speech recognition", 26, WHITE, BOLD)
        title5.to_edge(UP, buff=0.6)
        type_in(title5, run_time=1.0)

        wave_axes = Axes(
            x_range=[0, 8, 2], y_range=[-1, 1, 1],
            x_length=6.4, y_length=1.8,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_numbers": False},
        )
        wave_axes.next_to(title5, DOWN, buff=0.5)

        waveform = wave_axes.plot(
            lambda x: 0.6 * np.sin(3 * x) * np.exp(-0.05 * x) + 0.2 * np.sin(9 * x),
            x_range=[0, 8], color=CYAN, stroke_width=3,
        )

        self.play(Create(wave_axes), run_time=0.6)
        self.play(Create(waveform), run_time=1.1)

        arrow5 = txt("↓", 26, YELLOW)
        arrow5.next_to(wave_axes, DOWN, buff=0.3)
        self.play(FadeIn(arrow5, shift=DOWN * 0.15), run_time=0.5)

        transcript = txt("\"turn on the lights\"", 18, GREEN, font="DejaVu Sans Mono")
        transcript.next_to(arrow5, DOWN, buff=0.3)
        type_in(transcript, run_time=1.0)

        note5 = txt("used at Microsoft, IBM, Google —\ndeep learning is central here", 15, WHITE)
        note5.next_to(transcript, DOWN, buff=0.4)
        type_in(note5, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title5, wave_axes, waveform, arrow5, transcript, note5])

        # ============================================================
        # SCENE 6 — MACHINE TRANSLATION
        # ============================================================

        title6 = txt("Machine translation", 30, WHITE, BOLD)
        title6.to_edge(UP, buff=0.6)
        type_in(title6, run_time=1.0)

        statement6 = txt(
            "convert a sequence of symbols in one\nlanguage into another language",
            19, CYAN,
        )
        statement6.next_to(title6, DOWN, buff=0.55)
        type_in(statement6, run_time=1.4)

        english = txt("\"Hello, world\"", 18, WHITE, font="DejaVu Sans Mono")
        english.next_to(statement6, DOWN, buff=0.6)
        type_in(english, run_time=0.9)

        arrow6 = txt("↓", 26, YELLOW)
        arrow6.next_to(english, DOWN, buff=0.3)
        self.play(FadeIn(arrow6, shift=DOWN * 0.15), run_time=0.5)

        french = txt("\"Bonjour, le monde\"", 18, GREEN, font="DejaVu Sans Mono")
        french.next_to(arrow6, DOWN, buff=0.3)
        type_in(french, run_time=1.0)

        note6 = txt("deep learning has recently begun to\nhave major impact here", 15, WHITE)
        note6.next_to(french, DOWN, buff=0.4)
        type_in(note6, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title6, statement6, english, arrow6, french, note6])

        # ============================================================
        # SCENE 7 — STRUCTURED OUTPUT
        # ============================================================

        title7 = txt("Structured output", 30, WHITE, BOLD)
        title7.to_edge(UP, buff=0.6)
        type_in(title7, run_time=1.0)

        statement7 = txt(
            "output is a vector or data structure\nwith important relationships between elements",
            18, CYAN,
        )
        statement7.next_to(title7, DOWN, buff=0.5)
        type_in(statement7, run_time=1.4)

        broad_note = txt("a broad category — subsumes\ntranscription and translation", 16, YELLOW)
        broad_note.next_to(statement7, DOWN, buff=0.5)
        type_in(broad_note, run_time=1.1)

        self.wait(1.0)
        dust_wipe([title7, statement7, broad_note])

        # ============================================================
        # SCENE 8 — STRUCTURED OUTPUT EXAMPLE: PARSING
        # ============================================================

        title8 = txt("Example: parsing", 28, WHITE, BOLD)
        title8.to_edge(UP, buff=0.6)
        type_in(title8, run_time=0.9)

        sentence = txt("\"the cat sat\"", 18, WHITE, font="DejaVu Sans Mono")
        sentence.next_to(title8, DOWN, buff=0.5)
        type_in(sentence, run_time=0.9)

        # simple parse tree
        root = Dot(color=YELLOW, radius=0.07)
        root.move_to(DOWN * 0.5)
        left_child = Dot(color=CYAN, radius=0.06)
        left_child.move_to(root.get_center() + LEFT * 1.4 + DOWN * 0.9)
        right_child = Dot(color=GREEN, radius=0.06)
        right_child.move_to(root.get_center() + RIGHT * 1.4 + DOWN * 0.9)

        line_l = Line(root.get_center(), left_child.get_center(), color=WHITE, stroke_width=2)
        line_r = Line(root.get_center(), right_child.get_center(), color=WHITE, stroke_width=2)

        root_label = txt("S", 14, YELLOW)
        root_label.next_to(root, UP, buff=0.12)
        left_label = txt("NP: \"the cat\"", 12, CYAN)
        left_label.next_to(left_child, DOWN, buff=0.15)
        right_label = txt("VP: \"sat\"", 12, GREEN)
        right_label.next_to(right_child, DOWN, buff=0.15)

        tree = VGroup(line_l, line_r, root, left_child, right_child, root_label, left_label, right_label)
        tree.next_to(sentence, DOWN, buff=0.6)

        self.play(Create(line_l), Create(line_r), run_time=0.6)
        self.play(FadeIn(root), FadeIn(left_child), FadeIn(right_child), run_time=0.5)
        type_in(root_label, run_time=0.4)
        type_in(left_label, run_time=0.6)
        type_in(right_label, run_time=0.6)

        note8 = txt("nodes tagged as noun phrase,\nverb phrase, and so on", 15, WHITE)
        note8.next_to(tree, DOWN, buff=0.4)
        type_in(note8, run_time=1.0)

        self.wait(1.2)
        dust_wipe([title8, sentence, tree, note8])

        # ============================================================
        # SCENE 9 — ANOTHER STRUCTURED OUTPUT EXAMPLE: SEGMENTATION
        # ============================================================

        title9 = txt("Example: pixel-wise segmentation", 24, WHITE, BOLD)
        title9.to_edge(UP, buff=0.6)
        type_in(title9, run_time=1.0)

        seg_grid = VGroup()
        colors_map = [
            [CYAN, CYAN, GREEN, GREEN],
            [CYAN, CYAN, GREEN, GREEN],
            [RED, RED, YELLOW, YELLOW],
            [RED, RED, YELLOW, YELLOW],
        ]
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=0.55, fill_color=colors_map[i][j], fill_opacity=0.6,
                              stroke_color=WHITE, stroke_width=1.5)
                cell.move_to(np.array([j * 0.55, -i * 0.55, 0]))
                seg_grid.add(cell)
        seg_grid.move_to(ORIGIN)
        seg_grid.next_to(title9, DOWN, buff=0.7)

        self.play(FadeIn(seg_grid, lag_ratio=0.05), run_time=1.1)

        note9 = txt("every pixel is assigned\nto a specific category", 17, WHITE)
        note9.next_to(seg_grid, DOWN, buff=0.5)
        type_in(note9, run_time=1.0)

        self.wait(1.1)
        dust_wipe([title9, seg_grid, note9])

        # ============================================================
        # SCENE 10 — FINAL MESSAGE
        # ============================================================

        final = txt(
            "From numbers to sequences to trees —\ntasks shape the output format.",
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
    Page_99().render()
