from manim import *
import numpy as np
import random

# ============================================================
# PAGE 96 — CHAPTER 5: MACHINE LEARNING BASICS (INTRO)
# ============================================================

config.background_color = "#000000"
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60

random.seed(7)


class Page_96(MovingCameraScene):

    def construct(self):

        BLACK = "#000000"
        WHITE = "#F5F7FA"
        CYAN = "#4FD1FF"
        GREEN = "#65E572"
        YELLOW = "#FFD166"
        PURPLE = "#B388FF"
        RED = "#FF6B6B"

        self.camera.background_color = BLACK

        PAGE_NO = "96"

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

        def type_group(mobjs, run_time_each=0.9, lag=0.25):
            for m in mobjs:
                type_in(m, run_time=run_time_each)
                self.wait(lag)

        def dust_wipe(mobjects, run_time=1.0):
            """Shatter given mobjects into their submobjects and disperse them
            outward like dust, then remove from scene."""
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
        # SCENE 1 — CHAPTER TITLE
        # ============================================================

        chapter_tag = txt("CHAPTER 5", 22, CYAN, BOLD, font="DejaVu Sans")
        chapter_tag.move_to(UP * 1.4)

        heading = txt("Machine Learning Basics", 40, WHITE, BOLD)
        heading.next_to(chapter_tag, DOWN, buff=0.5)

        type_in(chapter_tag, run_time=0.8)
        self.wait(0.2)
        type_in(heading, run_time=1.3)

        self.play(
            self.camera.frame.animate.scale(0.85).move_to(heading.get_center()),
            run_time=1.0,
        )
        self.wait(0.6)
        self.play(self.camera.frame.animate.scale(1 / 0.85).move_to(ORIGIN), run_time=0.8)

        self.wait(0.8)
        dust_wipe([chapter_tag, heading])

        # ============================================================
        # SCENE 2 — DEEP LEARNING IS A KIND OF MACHINE LEARNING
        # ============================================================

        title2 = txt("Deep learning is a specific kind\nof machine learning", 24, WHITE, BOLD)
        title2.to_edge(UP, buff=0.7)
        type_in(title2, run_time=1.3)

        outer_circle = Circle(radius=1.9, color=CYAN, stroke_width=3)
        outer_circle.move_to(DOWN * 0.6)
        outer_label = txt("Machine Learning", 16, CYAN)
        outer_label.move_to(outer_circle.get_top() + DOWN * 0.4)

        inner_circle = Circle(radius=0.9, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.12)
        inner_circle.move_to(outer_circle.get_center() + DOWN * 0.4)
        inner_label = txt("Deep\nLearning", 15, YELLOW)
        inner_label.move_to(inner_circle.get_center())

        self.play(Create(outer_circle), run_time=0.8)
        type_in(outer_label, run_time=0.6)
        self.play(Create(inner_circle), run_time=0.7)
        type_in(inner_label, run_time=0.6)

        self.wait(1.0)
        dust_wipe([title2, outer_circle, outer_label, inner_circle, inner_label])

        # ============================================================
        # SCENE 3 — WHY THIS CHAPTER, AND WHERE TO SKIP TO
        # ============================================================

        title3 = txt("This chapter: the essentials", 26, WHITE, BOLD)
        title3.to_edge(UP, buff=0.7)
        type_in(title3, run_time=1.0)

        purpose_box = RoundedRectangle(width=6.7, height=1.7, corner_radius=0.16, color=CYAN, stroke_width=2.5)
        purpose_box.next_to(title3, DOWN, buff=0.5)
        purpose_text = txt("general principles used\nthroughout the rest of the book", 16, WHITE)
        purpose_text.move_to(purpose_box.get_center())

        self.play(Create(purpose_box), run_time=0.6)
        type_in(purpose_text, run_time=1.0)

        further_reading = txt("For more depth: Murphy (2012) or Bishop (2006)", 15, GREEN)
        fit_width(further_reading, 6.6)
        further_reading.next_to(purpose_box, DOWN, buff=0.5)
        type_in(further_reading, run_time=1.1)

        skip_note = txt("Already know the basics? Skip ahead to section 5.11", 15, YELLOW)
        fit_width(skip_note, 6.6)
        skip_note.next_to(further_reading, DOWN, buff=0.35)
        type_in(skip_note, run_time=1.1)

        self.wait(1.0)
        dust_wipe([title3, purpose_box, purpose_text, further_reading, skip_note])

        # ============================================================
        # SCENE 4 — WHAT SECTION 5.11 COVERS
        # ============================================================

        title4 = txt("Section 5.11 previews traditional ML", 23, WHITE, BOLD)
        title4.to_edge(UP, buff=0.7)
        type_in(title4, run_time=1.1)

        trad_box = RoundedRectangle(width=6.8, height=1.9, corner_radius=0.16, color=PURPLE, stroke_width=2.5)
        trad_box.next_to(title4, DOWN, buff=0.6)
        trad_text = txt(
            "perspectives on classical ML techniques\nthat shaped deep learning's development",
            16, WHITE,
        )
        trad_text.move_to(trad_box.get_center())

        self.play(Create(trad_box), run_time=0.7)
        type_in(trad_text, run_time=1.1)

        self.wait(1.0)
        dust_wipe([title4, trad_box, trad_text])

        # ============================================================
        # SCENE 5 — ROADMAP OF THE CHAPTER
        # ============================================================

        title5 = txt("What this chapter covers", 27, WHITE, BOLD)
        title5.to_edge(UP, buff=0.65)
        type_in(title5, run_time=1.0)

        items = [
            ("Learning algorithms", "definition + linear regression example", CYAN),
            ("Fitting vs. generalization", "training data vs. patterns that transfer", GREEN),
            ("Hyperparameters", "settings tuned outside the learning algorithm", YELLOW),
            ("Frequentist vs. Bayesian", "the two central approaches to statistics", PURPLE),
            ("Supervised vs. unsupervised", "the two broad learning categories", RED),
            ("Stochastic gradient descent", "the optimizer behind most deep learning", CYAN),
        ]

        rows = VGroup()
        for label, desc, color in items:
            dot = Dot(radius=0.06, color=color)
            label_txt = txt(label, 15, color, BOLD)
            desc_txt = txt(desc, 13, WHITE)
            row = VGroup(dot, label_txt, desc_txt).arrange(RIGHT, buff=0.18, aligned_edge=UP)
            fit_width(row, 7.3)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        rows.next_to(title5, DOWN, buff=0.5)

        for row in rows:
            self.play(FadeIn(row[0], scale=1.5), run_time=0.25)
            type_in(row[1], run_time=0.5)
            type_in(row[2], run_time=0.6)
            self.wait(0.1)

        self.wait(1.1)
        dust_wipe([title5, rows])

        # ============================================================
        # SCENE 6 — FINAL MESSAGE
        # ============================================================

        final = txt(
            "Deep learning stands on machine learning's\nfoundations — this chapter lays them down.",
            22, WHITE, BOLD,
        )
        fit_width(final, 7.0)
        final.move_to(ORIGIN)

        type_in(final, run_time=1.6)
        self.wait(0.3)

        line = Underline(final, color=CYAN, stroke_width=3, buff=0.18)
        self.play(Create(line), run_time=0.5)

        self.play(self.camera.frame.animate.scale(0.9), run_time=0.8)
        self.wait(1.8)


if __name__ == "__main__":
    Page_96().render()
