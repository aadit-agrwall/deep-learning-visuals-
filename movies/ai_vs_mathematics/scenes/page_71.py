from manim import *
from engine.core.base_scene import MovieManimScene


class Page71Scene(MovieManimScene):
    def construct(self):
        BLACK_C = "#111111"

        # ---------- TITLE ----------
        chapter_num = Text("3.13", font="Georgia", weight=BOLD, color=BLACK_C).scale(1.1)
        chapter_title = Text("Information Theory", font="Georgia", weight=BOLD, color=BLACK_C).scale(1.5)
        title_group = VGroup(chapter_num, chapter_title).arrange(RIGHT, buff=0.5)
        title_group.move_to(UP * 2.6)
        underline = Line(title_group.get_left(), title_group.get_right(), color=BLACK_C, stroke_width=2)
        underline.next_to(title_group, DOWN, buff=0.25)

        self.play(Write(title_group), run_time=1.6)
        self.play(Create(underline), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(title_group), FadeOut(underline), run_time=0.8)

        # ---------- CAPTION HELPER ----------
        current_caption = [None]

        def show_caption(text_str, scale=0.62, y=3.2):
            new_cap = Text(text_str, font="Georgia", color=BLACK_C, line_spacing=1.2).scale(scale)
            if new_cap.width > 12.5:
                new_cap.scale_to_fit_width(12.5)
            new_cap.move_to(UP * y)
            if current_caption[0] is not None:
                self.play(FadeOut(current_caption[0], shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(new_cap, shift=UP * 0.2), run_time=0.7)
            current_caption[0] = new_cap
            return new_cap

        def clear_caption():
            if current_caption[0] is not None:
                self.play(FadeOut(current_caption[0], shift=UP * 0.2), run_time=0.5)
                current_caption[0] = None

        # ---------- INTRO ----------
        show_caption("Information theory quantifies how much\ninformation a signal carries.", y=2.6)
        self.wait(1.4)

        show_caption("The core idea: learning an unlikely event\noccurred is more informative than a likely one.", y=2.6)
        self.wait(1.6)
        clear_caption()

        # ---------- SUN vs ECLIPSE EXAMPLE ----------
        sun_circle = Circle(radius=0.55, color="#D9A400", stroke_width=6, fill_color="#F5D97A", fill_opacity=1)
        sun_rays = VGroup(*[
            Line(ORIGIN, RIGHT * 0.9, color="#D9A400", stroke_width=5).rotate(i * PI / 6)
            for i in range(12)
        ])
        sun_icon = VGroup(sun_rays, sun_circle)
        sun_label = Text("\"The sun rose today.\"", font="Georgia", color=BLACK_C).scale(0.5)
        sun_sub = Text("low information", font="Georgia", color="#8A8A8A", slant=ITALIC).scale(0.4)
        sun_group = VGroup(sun_icon, sun_label, sun_sub).arrange(DOWN, buff=0.35)
        sun_group.move_to(LEFT * 3.6)

        outer = Circle(radius=0.6, color=BLACK_C, stroke_width=6)
        eclipse_mask = Circle(radius=0.6, color=WHITE, stroke_width=0, fill_color=WHITE, fill_opacity=1)
        eclipse_mask.move_to(outer.get_center() + RIGHT * 0.35)
        eclipse_icon = VGroup(outer.copy().set_fill(BLACK_C, opacity=1), eclipse_mask)
        eclipse_label = Text("\"There was a solar eclipse today.\"", font="Georgia", color=BLACK_C).scale(0.5)
        eclipse_sub = Text("high information", font="Georgia", color="#8A8A8A", slant=ITALIC).scale(0.4)
        eclipse_group = VGroup(eclipse_icon, eclipse_label, eclipse_sub).arrange(DOWN, buff=0.35)
        eclipse_group.move_to(RIGHT * 3.6)

        divider = DashedLine(UP * 1.6, DOWN * 1.6, color="#CCCCCC", stroke_width=2).move_to(ORIGIN)

        self.play(
            FadeIn(sun_group, shift=UP * 0.3),
            Create(divider),
            FadeIn(eclipse_group, shift=UP * 0.3),
            run_time=1.6,
        )
        self.wait(2.0)
        self.play(FadeOut(sun_group), FadeOut(eclipse_group), FadeOut(divider), run_time=0.8)

        # ---------- THREE PROPERTIES ----------
        show_caption("To formalize this intuition, information\nshould satisfy three properties:", y=3.0)
        self.wait(1.0)

        props = [
            "Likely events have low information;\ncertain events have none.",
            "Less likely events carry\nhigher information.",
            "Independent events have\nadditive information.",
        ]

        prop_group = VGroup()
        for i, p in enumerate(props):
            bullet = Dot(radius=0.07, color=BLACK_C)
            txt = Text(p, font="Georgia", color=BLACK_C, line_spacing=1.1).scale(0.42)
            row = VGroup(bullet, txt).arrange(RIGHT, buff=0.3, aligned_edge=UP)
            prop_group.add(row)

        prop_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        prop_group.move_to(DOWN * 0.6)

        for row in prop_group:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.7)

        self.wait(1.0)
        self.play(FadeOut(prop_group), run_time=0.8)
        clear_caption()

        # ---------- COIN FLIP ADDITIVITY VISUAL ----------
        coin1 = Circle(radius=0.4, color=BLACK_C, fill_color="#EAEAEA", fill_opacity=1, stroke_width=4)
        head1 = Text("H", font="Georgia", weight=BOLD, color=BLACK_C).scale(0.5).move_to(coin1)
        coin_a = VGroup(coin1, head1)

        coin2 = coin_a.copy()
        plus = Text("+", font="Georgia", color=BLACK_C).scale(0.9)
        pair = VGroup(coin_a, plus, coin2).arrange(RIGHT, buff=0.5)
        pair_label = Text("Two heads in a row = twice the information", font="Georgia", color=BLACK_C).scale(0.42)
        pair_full = VGroup(pair, pair_label).arrange(DOWN, buff=0.5)
        pair_full.move_to(ORIGIN)

        self.play(FadeIn(pair_full, shift=UP * 0.2), run_time=1.2)
        self.wait(1.8)
        self.play(FadeOut(pair_full), run_time=0.8)

        # ---------- SELF-INFORMATION FORMULA ----------
        formula_title = Text("self-information", font="Georgia", weight=BOLD, color=BLACK_C).scale(0.6)
        formula = MathTex(r"I(x) = -\log P(x)", color=BLACK_C).scale(1.5)
        eq_num = Text("(3.48)", font="Georgia", color="#8A8A8A").scale(0.5)

        formula_group = VGroup(formula_title, formula).arrange(DOWN, buff=0.5)
        formula_group.move_to(UP * 0.3)
        eq_num.next_to(formula, RIGHT, buff=1.2)

        self.play(Write(formula_title), run_time=0.8)
        self.play(Write(formula), FadeIn(eq_num), run_time=1.4)
        self.wait(1.5)

        box = SurroundingRectangle(formula, color="#B00020", buff=0.3, stroke_width=3)
        self.play(Create(box), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(box), run_time=0.5)

        self.play(
            formula_group.animate.move_to(UP * 2.0),
            FadeOut(eq_num),
            run_time=1.0,
        )

        # ---------- NATS EXPLANATION ----------
        nats_text = Text(
            "log here means the natural logarithm (base e).\nInformation is therefore measured in nats.",
            font="Georgia", color=BLACK_C, line_spacing=1.3
        ).scale(0.5)
        nats_text.move_to(DOWN * 0.8)
        self.play(FadeIn(nats_text, shift=UP * 0.2), run_time=1.0)
        self.wait(1.6)

        nat_def = MathTex(r"1 \text{ nat} = \text{information from an event of probability } \tfrac{1}{e}",
                           color="#8A8A8A").scale(0.55)
        nat_def.next_to(nats_text, DOWN, buff=0.6)
        if nat_def.width > 12.5:
            nat_def.scale_to_fit_width(12.5)
        self.play(FadeIn(nat_def, shift=UP * 0.15), run_time=0.9)
        self.wait(2.2)

        self.play(FadeOut(formula_group), FadeOut(nats_text), FadeOut(nat_def), run_time=1.0)
        self.wait(0.3)
