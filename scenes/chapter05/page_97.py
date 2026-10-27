from manim import *
import numpy as np
import random

# ============================================================
# PAGE 97 — 5.1 LEARNING ALGORITHMS  &  5.1.1 THE TASK, T
# ============================================================

config.background_color = "#000000"
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60

random.seed(11)


class Page_97(MovingCameraScene):

    def construct(self):

        BLACK = "#000000"
        WHITE = "#F5F7FA"
        CYAN = "#4FD1FF"
        GREEN = "#65E572"
        YELLOW = "#FFD166"
        PURPLE = "#B388FF"
        RED = "#FF6B6B"

        self.camera.background_color = BLACK

        PAGE_NO = "97"

        # --------------------------------------------------------
        # Helpers
        # --------------------------------------------------------

        def txt(text, size=24, color=WHITE, weight=NORMAL, font="DejaVu Serif"):
            return Text(text, font=font, font_size=size, color=color, weight=weight)

        def formula(tex, size=30, color=WHITE):
            return MathTex(tex, font_size=size, color=color)

        def fit_width(obj, width=7.4):
            if obj.width > width:
                obj.scale_to_fit_width(width)
            return obj

        def type_in(mobj, run_time=1.2):
            self.play(AddTextLetterByLetter(mobj), run_time=run_time)

        def dust_wipe(mobjects, run_time=1.0):
            targets = []
            for m in mobjects:
                if len(m.submobjects) > 0:
                    targets.extend(m.family_members_with_points())
                else:
                    targets.append(m)
            if not targets:
                return
            anims = []
            for sm in targets:
                angle = random.uniform(0, TAU)
                dist = random.uniform(1.2, 2.6)
                direction = np.array([np.cos(angle), np.sin(angle), 0])
                anims.append(
                    sm.animate.shift(direction * dist)
                    .scale(0.15)
                    .set_opacity(0)
                )
            self.play(LaggedStart(*anims, lag_ratio=0.01), run_time=run_time)
            self.remove(*mobjects)

        def make_footer():
            f = txt(f"ML-{PAGE_NO}", 18, GREEN, font="DejaVu Sans Mono")
            f.to_edge(DOWN, buff=0.35)
            return f

        footer = make_footer()
        self.add(footer)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter_tag = txt("CHAPTER 5", 20, CYAN, BOLD, font="DejaVu Sans")
        chapter_tag.move_to(UP * 1.5)

        heading = txt("Machine Learning Basics", 30, WHITE, BOLD)
        heading.next_to(chapter_tag, DOWN, buff=0.35)

        section = txt("5.1  Learning Algorithms", 22, YELLOW)
        section.next_to(heading, DOWN, buff=0.4)

        type_in(chapter_tag, run_time=0.7)
        type_in(heading, run_time=1.0)
        type_in(section, run_time=0.8)

        self.wait(0.8)
        dust_wipe([chapter_tag, heading, section])

        # ============================================================
        # SCENE 2 — WHERE THIS CHAPTER IS HEADED (RECAP + 5.11 PREVIEW)
        # ============================================================

        title2 = txt("Building toward a full ML algorithm", 24, WHITE, BOLD)
        title2.to_edge(UP, buff=0.65)
        type_in(title2, run_time=1.1)

        pieces = [
            ("Optimization", CYAN),
            ("Cost function", GREEN),
            ("Model", YELLOW),
            ("Dataset", PURPLE),
        ]

        boxes = VGroup()
        for label, color in pieces:
            box = RoundedRectangle(width=1.55, height=1.1, corner_radius=0.14, color=color, stroke_width=2.5)
            label_txt = txt(label, 13, color, BOLD)
            label_txt.move_to(box.get_center())
            boxes.add(VGroup(box, label_txt))

        boxes.arrange(RIGHT, buff=0.35)
        boxes.next_to(title2, DOWN, buff=0.7)

        for group in boxes:
            self.play(Create(group[0]), run_time=0.4)
            type_in(group[1], run_time=0.4)

        arrow = txt("↓", 30, WHITE)
        arrow.next_to(boxes, DOWN, buff=0.35)
        self.play(FadeIn(arrow, shift=DOWN * 0.2), run_time=0.5)

        result = txt("a complete machine learning algorithm", 16, WHITE)
        fit_width(result, 6.8)
        result.next_to(arrow, DOWN, buff=0.3)
        type_in(result, run_time=1.0)

        note = txt("section 5.11: limits of traditional ML generalization", 14, RED)
        fit_width(note, 6.8)
        note.next_to(result, DOWN, buff=0.4)
        type_in(note, run_time=1.0)

        self.wait(1.0)
        dust_wipe([title2, boxes, arrow, result, note])

        # ============================================================
        # SCENE 3 — MITCHELL'S DEFINITION OF LEARNING
        # ============================================================

        title3 = txt("5.1  Learning Algorithms", 26, WHITE, BOLD)
        title3.to_edge(UP, buff=0.65)
        type_in(title3, run_time=1.0)

        statement = txt("an algorithm that is able to learn from data", 17, CYAN)
        fit_width(statement, 6.8)
        statement.next_to(title3, DOWN, buff=0.45)
        type_in(statement, run_time=1.1)

        self.wait(0.5)
        self.play(
            self.camera.frame.animate.scale(0.9).move_to(statement.get_center()),
            run_time=0.7,
        )
        self.play(self.camera.frame.animate.scale(1 / 0.9).move_to(ORIGIN), run_time=0.6)

        quote_box = RoundedRectangle(width=7.2, height=3.0, corner_radius=0.16, color=PURPLE, stroke_width=2.5)
        quote_box.next_to(statement, DOWN, buff=0.5)

        quote_text = txt(
            "\"A program learns from experience E\nw.r.t. tasks T and performance P,\nif performance at T, as measured by P,\nimproves with experience E.\"",
            15, WHITE,
        )
        quote_text.move_to(quote_box.get_center() + UP * 0.15)

        source = txt("— Mitchell (1997)", 13, GREEN)
        source.next_to(quote_text, DOWN, buff=0.25)

        self.play(Create(quote_box), run_time=0.7)
        type_in(quote_text, run_time=1.8)
        type_in(source, run_time=0.6)

        self.wait(1.1)
        dust_wipe([title3, statement, quote_box, quote_text, source])

        # ============================================================
        # SCENE 4 — THE THREE INGREDIENTS: E, T, P
        # ============================================================

        title4 = txt("Three ingredients: E, T, P", 27, WHITE, BOLD)
        title4.to_edge(UP, buff=0.65)
        type_in(title4, run_time=1.0)

        ingredients = [
            ("E", "Experience", CYAN),
            ("T", "Task", YELLOW),
            ("P", "Performance measure", GREEN),
        ]

        cards = VGroup()
        for symbol, label, color in ingredients:
            circle = Circle(radius=0.55, color=color, stroke_width=3, fill_color=color, fill_opacity=0.1)
            sym = formula(symbol, 30, color)
            sym.move_to(circle.get_center())
            lbl = txt(label, 14, WHITE)
            lbl.next_to(circle, DOWN, buff=0.2)
            cards.add(VGroup(circle, sym, lbl))

        cards.arrange(RIGHT, buff=0.9)
        cards.next_to(title4, DOWN, buff=0.8)

        for card in cards:
            self.play(Create(card[0]), FadeIn(card[1]), run_time=0.6)
            type_in(card[2], run_time=0.6)

        note = txt("intuitive descriptions and examples follow —\nno formal definition attempted", 15, WHITE)
        fit_width(note, 6.7)
        note.next_to(cards, DOWN, buff=0.6)
        type_in(note, run_time=1.1)

        self.wait(1.1)
        dust_wipe([title4, cards, note])

        # ============================================================
        # SCENE 5 — 5.1.1 THE TASK, T
        # ============================================================

        title5 = txt("5.1.1  The Task, T", 28, WHITE, BOLD)
        title5.to_edge(UP, buff=0.65)
        type_in(title5, run_time=1.0)

        statement5 = txt("tasks too difficult to solve with\nfixed, hand-designed programs", 17, YELLOW)
        statement5.next_to(title5, DOWN, buff=0.5)
        type_in(statement5, run_time=1.3)

        insight = txt("understanding ML → understanding the\nprinciples that underlie intelligence", 15, WHITE)
        fit_width(insight, 6.7)
        insight.next_to(statement5, DOWN, buff=0.55)
        type_in(insight, run_time=1.2)

        self.wait(1.0)
        dust_wipe([title5, statement5, insight])

        # ============================================================
        # SCENE 6 — LEARNING IS THE MEANS, NOT THE TASK
        # ============================================================

        title6 = txt("Learning is the means, not the task", 24, WHITE, BOLD)
        title6.to_edge(UP, buff=0.65)
        type_in(title6, run_time=1.1)

        walk_label = txt("Task: walking", 18, CYAN, BOLD)
        walk_label.next_to(title6, DOWN, buff=0.6)
        type_in(walk_label, run_time=0.8)

        path1_box = RoundedRectangle(width=3.1, height=1.6, corner_radius=0.15, color=GREEN, stroke_width=2.5)
        path1_title = txt("Learn to walk", 14, GREEN, BOLD)
        path1_title.move_to(path1_box.get_center() + UP * 0.4)
        path1_text = txt("robot trains via\na learning algorithm", 12, WHITE)
        path1_text.move_to(path1_box.get_center() + DOWN * 0.25)

        path2_box = RoundedRectangle(width=3.1, height=1.6, corner_radius=0.15, color=RED, stroke_width=2.5)
        path2_title = txt("Hand-program it", 14, RED, BOLD)
        path2_title.move_to(path2_box.get_center() + UP * 0.4)
        path2_text = txt("directly write the\nwalking specification", 12, WHITE)
        path2_text.move_to(path2_box.get_center() + DOWN * 0.25)

        paths = VGroup(
            VGroup(path1_box, path1_title, path1_text),
            VGroup(path2_box, path2_title, path2_text),
        ).arrange(RIGHT, buff=0.5)
        paths.next_to(walk_label, DOWN, buff=0.6)

        self.play(Create(path1_box), run_time=0.6)
        type_in(path1_title, run_time=0.5)
        type_in(path1_text, run_time=0.7)

        self.play(Create(path2_box), run_time=0.6)
        type_in(path2_title, run_time=0.5)
        type_in(path2_text, run_time=0.7)

        self.wait(1.1)
        dust_wipe([title6, walk_label, paths])

        # ============================================================
        # SCENE 7 — EXAMPLES AND FEATURES
        # ============================================================

        title7 = txt("Examples and features", 27, WHITE, BOLD)
        title7.to_edge(UP, buff=0.65)
        type_in(title7, run_time=1.0)

        vec_formula = formula(r"\mathbf{x} \in \mathbb{R}^n", 34, CYAN)
        vec_formula.next_to(title7, DOWN, buff=0.6)
        self.play(Write(vec_formula), run_time=0.9)

        note7 = txt("each entry xᵢ is a feature", 16, WHITE)
        note7.next_to(vec_formula, DOWN, buff=0.4)
        type_in(note7, run_time=0.9)

        pixel_grid = VGroup()
        random.seed(3)
        for i in range(4):
            for j in range(4):
                shade = random.uniform(0.15, 0.9)
                cell = Square(side_length=0.5, fill_color=WHITE, fill_opacity=shade, stroke_color=CYAN, stroke_width=1)
                cell.move_to(np.array([j * 0.5, -i * 0.5, 0]))
                pixel_grid.add(cell)
        pixel_grid.move_to(ORIGIN)
        pixel_grid.next_to(note7, DOWN, buff=0.5)

        self.play(FadeIn(pixel_grid, lag_ratio=0.05), run_time=1.0)

        img_note = txt("example: an image →\npixel values are the features", 15, YELLOW)
        img_note.next_to(pixel_grid, DOWN, buff=0.4)
        type_in(img_note, run_time=1.1)

        self.wait(1.2)
        dust_wipe([title7, vec_formula, note7, pixel_grid, img_note])

        # ============================================================
        # SCENE 8 — FINAL MESSAGE
        # ============================================================

        final = txt(
            "A task is what we want done;\nlearning is how the system gets there.",
            22, WHITE, BOLD,
        )
        fit_width(final, 7.0)
        final.move_to(ORIGIN)

        type_in(final, run_time=1.5)
        self.wait(0.3)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.play(self.camera.frame.animate.scale(0.9), run_time=0.8)
        self.wait(1.8)


if __name__ == "__main__":
    Page_97().render()
