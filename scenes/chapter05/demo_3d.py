from manim import *
import numpy as np
from common.engine3d import *


class Demo3D(Stage3D):
    def construct(self):
        self.setup_stage("iso")

        # shot A: primitives, then top / side / iso views
        t = self.hud("Cube, cylinder, sphere"); self.play(Write(t), run_time=0.8)
        ax = axes3d()
        cube = box((1.2, 1.2, 1.2), [-2.4, 0, 0.6])
        cyl = cylinder(0.6, 1.6, [0, 0, 0.8])
        sph = sphere(0.7, [2.4, 0, 0.7])
        self.play(Create(ax), run_time=1.0)
        self.play(FadeIn(cube), FadeIn(cyl), FadeIn(sph), run_time=1.2)
        self.view("top", 2.4); self.wait(0.4)
        self.view("side", 2.4); self.wait(0.4)
        self.view("iso", 2.4); self.wait(0.3)
        self.play(FadeOut(t), FadeOut(ax), FadeOut(cube), FadeOut(cyl), FadeOut(sph), run_time=0.7)

        # shot B: neural network with a slow orbit
        t = self.hud("Neural network, orbiting camera"); self.play(Write(t), run_time=0.8)
        layers, edges, pos = neural_net((3, 5, 5, 2))
        self.play(LaggedStart(*[FadeIn(g) for g in layers], lag_ratio=0.25), run_time=1.6)
        self.play(Create(edges, lag_ratio=0.02), run_time=2.0)
        self.view("front", 2.0)
        self.orbit(PI / 2, 4.0)
        self.view("iso", 2.0)
        self.play(FadeOut(t), FadeOut(layers), FadeOut(edges), run_time=0.7)

        # shot C: loss surface with a descending point
        t = self.hud("Loss surface, gradient descent"); self.play(Write(t), run_time=0.8)
        ax = axes3d()
        bowl = surface(lambda u, v: 0.15 * (u * u + v * v))
        self.play(Create(ax), Create(bowl), run_time=2.0)
        path = ParametricFunction(
            lambda s: np.array([2.2 * (1 - s) * np.cos(5 * s), 2.2 * (1 - s) * np.sin(5 * s),
                                0.15 * (2.2 * (1 - s)) ** 2 + 0.06]),
            t_range=[0, 1], color=K, stroke_width=5)
        dot = Dot3D(path.get_start(), radius=0.14, color=K)
        self.play(FadeIn(dot), Create(path), run_time=0.8)
        self.play(MoveAlongPath(dot, path), run_time=3.0, rate_func=smooth)
        self.view("top", 2.4); self.wait(0.3)
        self.view("side", 2.4); self.wait(0.3)
        self.view("back34", 2.4); self.wait(0.8)
