from manim import *

config.background_color = WHITE


class Figure209(Scene):

    # ==========================================================
    # HELPERS
    # ==========================================================

    def title(self, text):
        return Text(
            text,
            font_size=30,
            color=BLACK,
        ).to_edge(
            UP,
            buff=0.35,
        )

    def grid(self):
        return NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.2,
            background_line_style={
                "stroke_color": GRAY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.25,
            },
            axis_config={
                "color": GRAY_D,
                "stroke_width": 1.5,
                "include_tip": False,
            },
        )

    def flash(self, mob, color=YELLOW, run_time=0.35):
        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.1,
            ),
            run_time=run_time,
        )

    def clear(self, group):
        if len(group) > 0:
            self.play(
                *[FadeOut(mob) for mob in group],
                run_time=0.45,
            )

    # ==========================================================
    # SCENE
    # ==========================================================

    def construct(self):

        # ======================================================
        # 1. WHAT IS A NORM?
        # ======================================================

        g = VGroup()

        heading = self.title(
            "A norm measures the size of a vector"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        plane = self.grid()

        self.play(
            Create(plane),
            run_time=0.7,
        )

        origin = plane.c2p(0, 0)
        point = plane.c2p(2.7, 1.8)

        vector = Arrow(
            origin,
            point,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        origin_dot = Dot(
            origin,
            radius=0.07,
            color=BLACK,
        )

        point_dot = Dot(
            point,
            radius=0.1,
            color=BLACK,
        )

        vector_label = MathTex(
            r"\mathbf{x}",
            font_size=32,
            color=BLACK,
        )

        vector_label.next_to(
            point_dot,
            RIGHT,
            buff=0.15,
        )

        origin_label = Text(
            "origin",
            font_size=21,
            color=GRAY_D,
        )

        origin_label.next_to(
            origin_dot,
            DOWN,
            buff=0.15,
        )

        self.play(
            FadeIn(origin_dot),
            Write(origin_label),
            run_time=0.5,
        )

        self.play(
            GrowArrow(vector),
            FadeIn(point_dot),
            Write(vector_label),
            run_time=0.8,
        )

        self.flash(
            vector,
            color=YELLOW,
        )

        norm_label = MathTex(
            r"\|\mathbf{x}\|",
            font_size=38,
            color=BLACK,
        )

        norm_label.next_to(
            vector.get_center(),
            UP + LEFT,
            buff=0.2,
        )

        self.play(
            Write(norm_label),
            run_time=0.6,
        )

        explanation = Text(
            "Distance from the origin to x",
            font_size=24,
            color=BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        g.add(
            heading,
            plane,
            vector,
            origin_dot,
            point_dot,
            vector_label,
            origin_label,
            norm_label,
            explanation,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 2. GENERAL Lp NORM
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The general Lp norm"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        formula = MathTex(
            r"\|\mathbf{x}\|_p"
            r"="
            r"\left("
            r"\sum_i |x_i|^p"
            r"\right)^{1/p}",
            font_size=42,
            color=BLACK,
        )

        formula.move_to(
            UP * 0.8
        )

        condition = MathTex(
            r"p\in\mathbb{R},\qquad p\geq1",
            font_size=30,
            color=GRAY_D,
        )

        condition.next_to(
            formula,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(formula),
            run_time=0.9,
        )

        self.flash(
            formula,
            color=YELLOW,
        )

        self.play(
            Write(condition),
            run_time=0.6,
        )

        meaning = Text(
            "Different values of p produce different ways of measuring size.",
            font_size=24,
            color=BLACK,
        )

        meaning.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(meaning),
            run_time=0.8,
        )

        g.add(
            heading,
            formula,
            condition,
            meaning,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 3. L2 NORM — EUCLIDEAN DISTANCE
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The L2 norm is the Euclidean norm"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        plane = self.grid()

        self.play(
            Create(plane),
            run_time=0.6,
        )

        origin = plane.c2p(0, 0)
        point = plane.c2p(2.8, 1.8)

        horizontal = Line(
            origin,
            plane.c2p(2.8, 0),
            color=GRAY_D,
            stroke_width=2,
        )

        vertical = Line(
            plane.c2p(2.8, 0),
            point,
            color=GRAY_D,
            stroke_width=2,
        )

        vector = Arrow(
            origin,
            point,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        dot = Dot(
            point,
            radius=0.1,
            color=BLACK,
        )

        x_label = MathTex(
            r"x_1",
            font_size=27,
        )

        x_label.next_to(
            horizontal.get_center(),
            DOWN,
            buff=0.15,
        )

        y_label = MathTex(
            r"x_2",
            font_size=27,
        )

        y_label.next_to(
            vertical.get_center(),
            RIGHT,
            buff=0.15,
        )

        self.play(
            Create(horizontal),
            Create(vertical),
            run_time=0.5,
        )

        self.play(
            GrowArrow(vector),
            FadeIn(dot),
            run_time=0.7,
        )

        self.play(
            Write(x_label),
            Write(y_label),
            run_time=0.5,
        )

        self.flash(
            vector,
            color=YELLOW,
        )

        l2 = MathTex(
            r"\|\mathbf{x}\|_2"
            r"="
            r"\sqrt{x_1^2+x_2^2}",
            font_size=34,
            color=BLACK,
        )

        l2.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(l2),
            run_time=0.8,
        )

        self.flash(
            l2,
            color=GREEN,
        )

        g.add(
            heading,
            plane,
            horizontal,
            vertical,
            vector,
            dot,
            x_label,
            y_label,
            l2,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 4. NORM AS DISTANCE
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The norm turns geometry into a number"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        plane = self.grid()

        self.play(
            Create(plane),
            run_time=0.6,
        )

        origin = plane.c2p(0, 0)
        points = [
            plane.c2p(1.5, 1.0),
            plane.c2p(2.2, 1.45),
            plane.c2p(2.8, 1.85),
        ]

        vector = Arrow(
            origin,
            points[0],
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        dot = Dot(
            points[0],
            radius=0.1,
            color=BLACK,
        )

        label = MathTex(
            r"\|\mathbf{x}\|_2",
            font_size=34,
        )

        label.next_to(
            points[0],
            UP + RIGHT,
            buff=0.15,
        )

        self.play(
            GrowArrow(vector),
            FadeIn(dot),
            Write(label),
            run_time=0.7,
        )

        for p in points[1:]:

            self.flash(
                dot,
                color=YELLOW,
                run_time=0.25,
            )

            self.play(
                vector.animate.put_start_and_end_on(
                    origin,
                    p,
                ),
                dot.animate.move_to(p),
                label.animate.next_to(
                    p,
                    UP + RIGHT,
                    buff=0.15,
                ),
                run_time=0.65,
            )

        statement = Text(
            "Farther from the origin → larger norm",
            font_size=25,
            color=BLACK,
        )

        statement.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(statement),
            run_time=0.7,
        )

        self.flash(
            vector,
            color=GREEN,
        )

        g.add(
            heading,
            plane,
            vector,
            dot,
            label,
            statement,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 5. SQUARED L2 NORM
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The squared L2 norm"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        l2 = MathTex(
            r"\|\mathbf{x}\|_2"
            r"="
            r"\sqrt{\mathbf{x}^{T}\mathbf{x}}",
            font_size=38,
            color=BLACK,
        )

        squared = MathTex(
            r"\|\mathbf{x}\|_2^2"
            r"="
            r"\mathbf{x}^{T}\mathbf{x}",
            font_size=42,
            color=BLUE_E,
        )

        l2.move_to(
            UP * 0.75
        )

        squared.move_to(
            DOWN * 0.35
        )

        self.play(
            Write(l2),
            run_time=0.8,
        )

        self.flash(
            l2,
            color=YELLOW,
        )

        self.play(
            TransformMatchingTex(
                l2.copy(),
                squared,
            ),
            run_time=0.9,
        )

        self.flash(
            squared,
            color=BLUE,
        )

        explanation = Text(
            "The square removes the square root.",
            font_size=24,
            color=BLACK,
        )

        explanation.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        g.add(
            heading,
            l2,
            squared,
            explanation,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 6. WHY SQUARED L2 IS CONVENIENT
        # ======================================================

        g = VGroup()

        heading = self.title(
            "Why use the squared L2 norm?"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        normal = MathTex(
            r"\|\mathbf{x}\|_2"
            r"="
            r"\sqrt{x_1^2+x_2^2+\cdots+x_n^2}",
            font_size=34,
            color=BLACK,
        )

        squared = MathTex(
            r"\|\mathbf{x}\|_2^2"
            r"="
            r"x_1^2+x_2^2+\cdots+x_n^2",
            font_size=34,
            color=BLUE_E,
        )

        normal.move_to(
            UP * 0.85
        )

        squared.move_to(
            DOWN * 0.1
        )

        self.play(
            Write(normal),
            run_time=0.8,
        )

        self.flash(
            normal,
            color=YELLOW,
        )

        self.play(
            Write(squared),
            run_time=0.8,
        )

        self.flash(
            squared,
            color=BLUE,
        )

        # Simple derivative visual
        derivative = MathTex(
            r"\frac{\partial}{\partial x_i}"
            r"\|\mathbf{x}\|_2^2"
            r"="
            r"2x_i",
            font_size=33,
            color=GREEN_E,
        )

        derivative.move_to(
            DOWN * 1.0
        )

        self.play(
            Write(derivative),
            run_time=0.8,
        )

        self.flash(
            derivative,
            color=GREEN,
        )

        statement = Text(
            "Each derivative depends directly on the corresponding element.",
            font_size=22,
            color=BLACK,
        )

        statement.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(statement),
            run_time=0.7,
        )

        g.add(
            heading,
            normal,
            squared,
            derivative,
            statement,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 7. THREE PROPERTIES OF A NORM
        # ======================================================

        g = VGroup()

        heading = self.title(
            "A norm must satisfy three fundamental properties"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        property1 = MathTex(
            r"\|\mathbf{x}\|=0"
            r"\quad\Longrightarrow\quad"
            r"\mathbf{x}=0",
            font_size=32,
            color=BLACK,
        )

        property2 = MathTex(
            r"\|\mathbf{x}+\mathbf{y}\|"
            r"\leq"
            r"\|\mathbf{x}\|+\|\mathbf{y}\|",
            font_size=32,
            color=BLACK,
        )

        property3 = MathTex(
            r"\|\alpha\mathbf{x}\|"
            r"="
            r"|\alpha|\,\|\mathbf{x}\|",
            font_size=32,
            color=BLACK,
        )

        property1.move_to(
            UP * 1.0
        )

        property2.move_to(
            ORIGIN
        )

        property3.move_to(
            DOWN * 1.0
        )

        self.play(
            Write(property1),
            run_time=0.7,
        )

        self.flash(
            property1,
            color=YELLOW,
        )

        self.play(
            Write(property2),
            run_time=0.7,
        )

        self.flash(
            property2,
            color=YELLOW,
        )

        self.play(
            Write(property3),
            run_time=0.7,
        )

        self.flash(
            property3,
            color=YELLOW,
        )

        labels = VGroup(
            Text(
                "zero only at the origin",
                font_size=19,
                color=GRAY_D,
            ).next_to(
                property1,
                RIGHT,
                buff=0.25,
            ),
            Text(
                "triangle inequality",
                font_size=19,
                color=GRAY_D,
            ).next_to(
                property2,
                RIGHT,
                buff=0.25,
            ),
            Text(
                "scaling",
                font_size=19,
                color=GRAY_D,
            ).next_to(
                property3,
                RIGHT,
                buff=0.25,
            ),
        )

        self.play(
            *[Write(label) for label in labels],
            run_time=0.8,
        )

        g.add(
            heading,
            property1,
            property2,
            property3,
            labels,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 8. TRIANGLE INEQUALITY VISUAL
        # ======================================================

        g = VGroup()

        heading = self.title(
            "Triangle inequality"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        plane = self.grid()

        self.play(
            Create(plane),
            run_time=0.6,
        )

        origin = plane.c2p(0, 0)
        p1 = plane.c2p(1.8, 1.0)
        p2 = plane.c2p(3.0, 2.3)

        v1 = Arrow(
            origin,
            p1,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v2 = Arrow(
            p1,
            p2,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        direct = Arrow(
            origin,
            p2,
            color=BLUE_E,
            stroke_width=5,
            buff=0,
        )

        self.play(
            GrowArrow(v1),
            run_time=0.6,
        )

        self.flash(
            v1,
            color=YELLOW,
        )

        self.play(
            GrowArrow(v2),
            run_time=0.6,
        )

        self.flash(
            v2,
            color=YELLOW,
        )

        self.play(
            GrowArrow(direct),
            run_time=0.7,
        )

        self.flash(
            direct,
            color=BLUE,
        )

        formula = MathTex(
            r"\|\mathbf{x}+\mathbf{y}\|"
            r"\leq"
            r"\|\mathbf{x}\|+\|\mathbf{y}\|",
            font_size=34,
            color=BLACK,
        )

        formula.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(formula),
            run_time=0.8,
        )

        g.add(
            heading,
            plane,
            v1,
            v2,
            direct,
            formula,
        )

        self.wait(1)

        self.clear(g)

        # ======================================================
        # 9. FINAL SUMMARY
        # ======================================================

        heading = self.title(
            "The norm: a mathematical measure of vector size"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        lp = MathTex(
            r"\|\mathbf{x}\|_p"
            r"="
            r"\left("
            r"\sum_i|x_i|^p"
            r"\right)^{1/p}",
            font_size=36,
            color=BLACK,
        )

        euclidean = MathTex(
            r"\|\mathbf{x}\|_2"
            r"="
            r"\sqrt{\mathbf{x}^{T}\mathbf{x}}",
            font_size=34,
            color=BLACK,
        )

        squared = MathTex(
            r"\|\mathbf{x}\|_2^2"
            r"="
            r"\mathbf{x}^{T}\mathbf{x}",
            font_size=34,
            color=BLUE_E,
        )

        lp.move_to(
            UP * 0.9
        )

        euclidean.move_to(
            ORIGIN
        )

        squared.move_to(
            DOWN * 0.9
        )

        self.play(
            Write(lp),
            run_time=0.8,
        )

        self.flash(
            lp,
            color=YELLOW,
        )

        self.play(
            Write(euclidean),
            run_time=0.7,
        )

        self.flash(
            euclidean,
            color=GREEN,
        )

        self.play(
            Write(squared),
            run_time=0.7,
        )

        self.flash(
            squared,
            color=BLUE,
        )

        final_text = Text(
            "Size → distance → geometry → optimization",
            font_size=24,
            color=BLACK,
        )

        final_text.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(final_text),
            run_time=0.8,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure209().render()
