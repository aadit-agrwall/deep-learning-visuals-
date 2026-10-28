from manim import *
import numpy as np
from common.engine3d import *


class Test3D(Stage3D):
    def construct(self):
        self.setup_stage("iso")
        report = []

        def log(line):
            report.append(line)
            open("/tmp/engine3d_test.txt", "w").write("\n".join(report) + "\n")

        def shot(name, fn):
            try:
                fn(); log("OK    " + name)
            except Exception as e:
                log(f"FAIL  {name}: {type(e).__name__}: {e}")
                try:
                    self.remove(*self.mobjects)
                except Exception:
                    pass
                self._stage = []; self._cap = None

        def primitives():
            self.caption("Primitives")
            ax = axes3d()
            objs = [box((1, 1, 1), [-3.0, 0, 0.5]), cylinder(0.5, 1.4, [-1.5, 0, 0.7]),
                    sphere(0.6, [0, 0, 0.6]), cone(0.55, 1.3, [1.5, 0, 0.65]),
                    torus(0.6, 0.22, [3.0, 0, 0.5]), arrow3d([0, 2, 0], [1.5, 2, 1.5])]
            self.reveal(ax, anim="create", run=0.8)
            self.reveal(*objs, run=1.0)
            self.tour(["top", "side", "iso"], run=1.0, hold=0.2)
            self.clear_scene()

        def surfaces():
            self.caption("Surfaces and descent")
            ax = axes3d(); bowl = bowl_surface()
            path = curve3d(lambda s: [2.2 * (1 - s) * np.cos(5 * s), 2.2 * (1 - s) * np.sin(5 * s),
                                      0.15 * (2.2 * (1 - s)) ** 2 + 0.06], (0, 1), K, 5)
            dot = Dot3D(path.get_start(), radius=0.14, color=K)
            self.reveal(ax, bowl, anim="create", run=1.2)
            self.reveal(dot, path, run=0.6)
            self.play(MoveAlongPath(dot, path), run_time=2.0, rate_func=smooth)
            self.blue(dot)
            self.view("top", 1.2)
            self.clear_scene()
            self.view("iso", 0.8)
            g = gaussian_surface(); s2 = saddle_surface()
            self.reveal(g, anim="create", run=1.0); self.clear_scene(0.5)
            self.reveal(s2, anim="create", run=1.0); self.clear_scene(0.5)

        def network():
            self.caption("Forward pass")
            net = Net3D((3, 4, 3, 2))
            net.reveal(self, run=2.0); self.keep(net.group)
            self.view("front", 1.2)
            net.forward_pass(self, step=0.6); net.reset(self)
            self.view("iso", 1.2)
            self.clear_scene()

        def perceptron():
            self.caption("Perceptron fires")
            pc = Perceptron3D(3)
            pc.reveal(self); self.keep(pc.group)
            pc.fire(self, step=0.6); pc.reset(self)
            self.clear_scene()

        def scatter():
            self.caption("Classes and hyperplane")
            pos, neg, pp, nn = scatter_classes()
            pl = plane_poly(ORIGIN, (1, 1, 1), 2.6)
            self.reveal(pos, neg, pl, run=1.2)
            self.view("side", 1.4)
            self.pulse(pos[0]); self.pulse(neg[0])
            self.view("iso", 1.2)
            self.clear_scene()

        def blocks():
            self.caption("Bars, matrix, CNN")
            bars = bars3d(np.array([[1, 2, 3], [2, 3, 4], [1, 4, 2]]) * 0.3, at=[0, 0, 0])
            self.reveal(bars, run=1.0); self.clear_scene(0.5)
            mg = matrix_grid(4, 4)
            self.reveal(mg, run=0.8)
            self.play(grid_cell(mg, 4, 1, 2).animate.set_fill(ACCENT, opacity=0.9), run_time=0.6)
            self.clear_scene(0.5)
            cs = cnn_stack(4); self.reveal(cs, run=0.8)
            self.view("front", 1.0); self.view("iso", 1.0)
            vx = voxels((2, 2, 2)); self.reveal(vx, run=0.6)
            self.clear_scene()

        def flat_2d():
            from PIL import Image
            Image.new("RGB", (200, 260), (235, 235, 235)).save("/tmp/_t3d.png")
            self.view("flat", 0.5)
            img = ImageMobject("/tmp/_t3d.png"); img.scale_to_fit_height(3.0).move_to([-2, 0, 0])
            tx = Tex("2D text in a 3D scene", color=K, font_size=34).move_to([2, 0, 0])
            self.reveal(img, tx, run=0.8)
            self.view("iso", 1.2); self.view("flat", 1.2)
            self.clear_scene()
            self.view("iso", 0.8)

        shot("primitives", primitives)
        shot("surfaces", surfaces)
        shot("neural network (blue firing)", network)
        shot("perceptron (blue firing)", perceptron)
        shot("scatter + hyperplane", scatter)
        shot("bars/matrix/cnn/voxels", blocks)
        shot("flat 2D inside 3D scene", flat_2d)
        self.wait(0.5)
