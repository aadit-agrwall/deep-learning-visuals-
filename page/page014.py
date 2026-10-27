from manim import *

class Page014(Scene):

    def construct(self):

        # ---------------- TITLE ----------------

        title = Text(
            "Early Linear Models",
            font_size=52,
            color=BLUE
        )

        title.to_edge(UP)

        self.play(Write(title))

        self.wait(1)

        # ---------------- INPUTS ----------------

        x1 = MathTex("x_1")
        x2 = MathTex("x_2")
        xn = MathTex("x_n")

        inputs = VGroup(x1,x2,xn)

        inputs.arrange(DOWN,buff=1)

        inputs.shift(LEFT*5)

        self.play(Write(inputs))

        # ---------------- MODEL ----------------

        model = RoundedRectangle(
            width=3,
            height=2,
            corner_radius=0.2,
            color=GREEN
        )

        model.move_to(ORIGIN)

        model_text = Text(
            "Linear\nModel",
            font_size=32
        )

        model_text.move_to(model)

        self.play(Create(model))

        self.play(Write(model_text))

        # ---------------- OUTPUT ----------------

        output = MathTex("y")

        output.shift(RIGHT*5)

        self.play(Write(output))

        # ---------------- CONNECTIONS ----------------

        arrows = VGroup()

        for obj in inputs:

            arrows.add(

                Arrow(
                    obj.get_right(),
                    model.get_left(),
                    buff=0.2
                )

            )

        out_arrow = Arrow(
            model.get_right(),
            output.get_left(),
            buff=0.2
        )

        self.play(Create(arrows))

        self.play(Create(out_arrow))

        self.wait()

        # ---------------- EQUATION ----------------

        equation = MathTex(
            "f(x,w)=",
            "x_1w_1",
            "+",
            "x_2w_2",
            "+",
            "...",
            "+",
            "x_nw_n"
        )

        equation.scale(0.9)

        equation.to_edge(DOWN)

        self.play(Write(equation))

        self.wait(2)

        # ---------------- WEIGHTS ----------------

        weight_title = Text(
            "Learning the Weights",
            font_size=38,
            color=YELLOW
        )

        weight_title.next_to(model,UP)

        self.play(FadeIn(weight_title))

        weights = VGroup(

            MathTex("w_1"),

            MathTex("w_2"),

            MathTex("w_n")

        )

        weights.arrange(DOWN,buff=.8)

        weights.move_to(RIGHT*2)

        self.play(Write(weights))

        self.wait()

        # ---------------- PERCEPTRON ----------------

        perceptron = Text(
            "Perceptron",
            font_size=42,
            color=RED
        )

        perceptron.to_edge(DOWN)

        self.play(

            Transform(
                equation,
                perceptron
            )

        )

        yes = Text(
            "YES",
            color=GREEN,
            font_size=40
        )

        no = Text(
            "NO",
            color=RED,
            font_size=40
        )

        yes.shift(RIGHT*5+UP)

        no.shift(RIGHT*5+DOWN)

        self.play(FadeIn(yes))

        self.play(FadeIn(no))

        self.wait(2)

        self.play(*[
            FadeOut(mob)
            for mob in self.mobjects
        ])