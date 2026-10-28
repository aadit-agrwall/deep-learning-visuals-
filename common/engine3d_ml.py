from manim import *
import numpy as np
from common.engine3d import *


# ------------------------------------------------------------------ helpers
def _u(v):
    v = np.array(v, dtype=float); n = np.linalg.norm(v)
    return v / n if n > 1e-9 else np.array([0.0, 0.0, 1.0])


def lit(m, op=0.85):
    """Blue 'active' state. Dots recolor; boxes/spheres/squares fill blue."""
    if isinstance(m, Dot3D):
        return m.animate.set_color(ACCENT)
    return m.animate.set_fill(ACCENT, opacity=op)


def unlit(m):
    if isinstance(m, Dot3D):
        return m.animate.set_color(K)
    return m.animate.set_fill(PAPER, opacity=0.9)


def tags(scene, items, size=24, run=0.4):
    """Flat text labels that stay readable in every camera view."""
    out = []
    for text, pos in items:
        t = Tex(text, color=K, font_size=size).move_to(np.array(pos, dtype=float))
        scene.add_fixed_orientation_mobjects(t)
        out.append(t)
    scene._items().extend(out)
    if out:
        scene.play(*[FadeIn(t) for t in out], run_time=run)
    return out


def flashes(scene, pairs, run=0.6, width=5):
    if not pairs:
        return
    scene.play(*[ShowPassingFlash(Line(np.array(a, dtype=float), np.array(b, dtype=float),
                                       color=ACCENT, stroke_width=width), time_width=0.7)
                 for a, b in pairs], run_time=run)


def _perc_reset(self, scene, run=0.5):
    parts = list(self.inputs) + [self.sum_node, self.out_node]
    scene.play(*[unlit(m) for m in parts], run_time=run)


Perceptron3D.reset = _perc_reset   # fixes boxes turning black after reset


# --------------------------------------------------------------------- CNN
class ConvSweep:
    def __init__(self, n=6, k=3, cell=0.42, gap_x=4.2, at=ORIGIN):
        at = np.array(at, dtype=float)
        self.n, self.k, self.cell, self.m = n, k, cell, n - k + 1
        self.in_at = at + np.array([-gap_x / 2, 0.0, 0.0])
        self.out_at = at + np.array([gap_x / 2, 0.0, 0.0])
        self.inp = matrix_grid(n, n, cell, self.in_at)
        self.out = matrix_grid(self.m, self.m, cell, self.out_at)
        self.window = Square(side_length=k * cell, color=ACCENT, stroke_width=5)
        self.window.set_fill(ACCENT, opacity=0.12)
        self.window.move_to(self._wc(0, 0))
        self.group = VGroup(self.inp, self.out, self.window)

    def _wc(self, i, j):
        x = (j + (self.k - 1) / 2 - (self.n - 1) / 2) * self.cell
        y = ((self.n - 1) / 2 - (i + (self.k - 1) / 2)) * self.cell
        return self.in_at + np.array([x, y, 0.02])

    def reveal(self, scene, run=1.2):
        scene.play(FadeIn(self.inp), FadeIn(self.out), run_time=run)
        scene.play(FadeIn(self.window), run_time=0.4)
        scene.keep(self.group)
        c = self.cell
        tags(scene, [("input", self.in_at + np.array([0, -(self.n * c / 2 + 0.45), 0])),
                     ("feature map", self.out_at + np.array([0, -(self.m * c / 2 + 0.45), 0]))])

    def sweep(self, scene, step=0.18):
        for i in range(self.m):
            for j in range(self.m):
                cell = grid_cell(self.out, self.m, i, j)
                scene.play(self.window.animate.move_to(self._wc(i, j)), lit(cell), run_time=step)

    def reset(self, scene, run=0.5):
        scene.play(*[unlit(c) for c in self.out], self.window.animate.move_to(self._wc(0, 0)), run_time=run)


class PoolDemo:
    def __init__(self, vals=None, cell=0.55, gap_x=3.8, at=ORIGIN):
        v = np.array(vals if vals is not None else
                     [[1, 3, 2, 1], [4, 6, 5, 2], [3, 1, 0, 7], [2, 8, 4, 3]], dtype=float)
        self.v, self.n, self.cell = v, v.shape[0], cell
        self.m = self.n // 2
        at = np.array(at, dtype=float)
        self.in_at = at + np.array([-gap_x / 2, 0.0, 0.0])
        self.out_at = at + np.array([gap_x / 2, 0.0, 0.0])
        self.inp = matrix_grid(self.n, self.n, cell, self.in_at)
        self.out = matrix_grid(self.m, self.m, cell, self.out_at)
        self.win = Square(side_length=2 * cell, color=ACCENT, stroke_width=5)
        self.win.set_fill(ACCENT, opacity=0.12)
        self.win.move_to(self._block(0, 0))
        self.group = VGroup(self.inp, self.out, self.win)

    def _cp(self, at, rows, cols, i, j, z=0.05):
        return at + np.array([(j - (cols - 1) / 2) * self.cell, ((rows - 1) / 2 - i) * self.cell, z])

    def _block(self, bi, bj):
        n, c = self.n, self.cell
        return self.in_at + np.array([(2 * bj + 0.5 - (n - 1) / 2) * c, ((n - 1) / 2 - (2 * bi + 0.5)) * c, 0.02])

    def reveal(self, scene, run=1.2):
        scene.play(FadeIn(self.inp), FadeIn(self.out), FadeIn(self.win), run_time=run)
        scene.keep(self.group)
        n = self.n
        tags(scene, [(str(int(self.v[i, j])), self._cp(self.in_at, n, n, i, j)) for i in range(n) for j in range(n)], 22)
        tags(scene, [("max pooling", self.out_at + np.array([0, -(self.m * self.cell / 2 + 0.5), 0]))])

    def pool(self, scene, step=0.7):
        for bi in range(self.m):
            for bj in range(self.m):
                scene.play(self.win.animate.move_to(self._block(bi, bj)), run_time=step * 0.5)
                blk = self.v[2 * bi:2 * bi + 2, 2 * bj:2 * bj + 2]
                mi, mj = np.unravel_index(np.argmax(blk), blk.shape)
                mc = grid_cell(self.inp, self.n, 2 * bi + mi, 2 * bj + mj)
                oc = grid_cell(self.out, self.m, bi, bj)
                scene.play(lit(mc), lit(oc), run_time=step * 0.4)
                tags(scene, [(str(int(blk.max())), self._cp(self.out_at, self.m, self.m, bi, bj))], 24, 0.2)


class CNN3D:
    def __init__(self, spec=None, gap=1.7, at=ORIGIN, max_slabs=5):
        spec = spec or (("conv", 1.8, 4), ("pool", 1.2, 4), ("conv", 1.0, 6), ("dense", 8), ("dense", 3))
        at = np.array(at, dtype=float); L = len(spec)
        self.spec, self.layers, self.centers, self.tag_z = spec, [], [], []
        for i, s in enumerate(spec):
            c = at + np.array([(i - (L - 1) / 2) * gap, 0.0, 0.0]); self.centers.append(c)
            if s[0] in ("conv", "pool"):
                size, m = s[1], min(s[2], max_slabs)
                grp = VGroup(*[box((0.1, size, size), c + np.array([(k - (m - 1) / 2) * 0.2, 0, 0]), sw=2)
                               for k in range(m)])
                self.tag_z.append(-(size / 2 + 0.45))
            else:
                h = min(0.14 * s[1], 3.0)
                grp = VGroup(box((0.18, 0.3, h), c, sw=2))
                self.tag_z.append(-(h / 2 + 0.45))
            self.layers.append(grp)
        self.links = [Line(self.centers[i], self.centers[i + 1], color=K, stroke_width=1.5, stroke_opacity=0.5)
                      for i in range(L - 1)]
        self.group = VGroup(*self.layers, *self.links)

    def reveal(self, scene, run=2.0):
        scene.play(LaggedStart(*[FadeIn(g) for g in self.layers], lag_ratio=0.3), run_time=run * 0.6)
        if self.links:
            scene.play(*[Create(l) for l in self.links], run_time=run * 0.4)
        scene.keep(self.group)
        names = {"conv": "conv", "pool": "pool", "dense": "fc"}
        tags(scene, [(names[s[0]], self.centers[i] + np.array([0, 0, self.tag_z[i]]))
                     for i, s in enumerate(self.spec)], 22)

    def forward(self, scene, step=0.6):
        for i, g in enumerate(self.layers):
            extra = []
            if i > 0:
                extra = [ShowPassingFlash(Line(self.centers[i - 1], self.centers[i], color=ACCENT, stroke_width=5),
                                          time_width=0.8)]
            scene.play(*[lit(m) for m in g], *extra, run_time=step)

    def reset(self, scene, run=0.5):
        scene.play(*[unlit(m) for g in self.layers for m in g], run_time=run)


# ---------------------------------------------------------------- sequences
class RNNUnrolled3D:
    def __init__(self, steps=4, gap=2.0, at=ORIGIN):
        at = np.array(at, dtype=float); self.steps = steps
        self.cp = [at + np.array([(t - (steps - 1) / 2) * gap, 0, 0]) for t in range(steps)]
        self.ip = [p + np.array([0, 0, -1.6]) for p in self.cp]
        self.op = [p + np.array([0, 0, 1.6]) for p in self.cp]
        z, x = np.array([0, 0, 0.45]), np.array([0.45, 0, 0])
        self.cells = VGroup(*[box((0.9, 0.9, 0.9), p) for p in self.cp])
        self.ins = VGroup(*[Dot3D(p, radius=0.15, color=K) for p in self.ip])
        self.outs = VGroup(*[Dot3D(p, radius=0.15, color=K) for p in self.op])
        self.ie = [(self.ip[t], self.cp[t] - z) for t in range(steps)]
        self.oe = [(self.cp[t] + z, self.op[t]) for t in range(steps)]
        self.he = [(self.cp[t] + x, self.cp[t + 1] - x) for t in range(steps - 1)]
        lines = [Line(a, b, color=K, stroke_width=3) for a, b in self.ie + self.oe + self.he]
        self.lines = VGroup(*lines)
        self.group = VGroup(self.cells, self.ins, self.outs, self.lines)

    def reveal(self, scene, run=2.0):
        scene.play(LaggedStart(*[FadeIn(c) for c in self.cells], lag_ratio=0.25), run_time=run * 0.5)
        scene.play(FadeIn(self.ins), FadeIn(self.outs), Create(self.lines), run_time=run * 0.5)
        scene.keep(self.group)
        items = []
        for t in range(self.steps):
            items.append((f"$x_{{{t + 1}}}$", self.ip[t] + np.array([0, 0, -0.45])))
            items.append((f"$y_{{{t + 1}}}$", self.op[t] + np.array([0, 0, 0.45])))
        tags(scene, items, 24)

    def run(self, scene, step=0.5):
        for t in range(self.steps):
            scene.play(lit(self.ins[t]), run_time=step * 0.4)
            pairs = [self.ie[t]] + ([self.he[t - 1]] if t > 0 else [])
            flashes(scene, pairs, run=step)
            scene.play(lit(self.cells[t]), run_time=step * 0.4)
            flashes(scene, [self.oe[t]], run=step * 0.8)
            scene.play(lit(self.outs[t]), run_time=step * 0.4)

    def reset(self, scene, run=0.5):
        scene.play(*[unlit(m) for m in list(self.ins) + list(self.cells) + list(self.outs)], run_time=run)


class LSTMCell3D:
    def __init__(self, at=ORIGIN):
        at = np.array(at, dtype=float)
        A = lambda x, z: at + np.array([x, 0.0, z])
        self.A = A
        self.frame = Polygon(A(-2.2, -1.1), A(2.2, -1.1), A(2.2, 1.1), A(-2.2, 1.1), color=K, stroke_width=3)
        self.frame.set_fill(PAPER, opacity=0.05)
        self.gx = {"f": -1.3, "i": -0.3, "o": 1.2}
        self.c_pair = (A(-2.9, 0.7), A(2.9, 0.7))
        self.c_line = Line(*self.c_pair, color=K, stroke_width=4)
        self.gates = {k: box((0.42, 0.42, 0.42), A(x, -0.2), sw=2) for k, x in self.gx.items()}
        self.x_in = Dot3D(A(-0.2, -1.9), radius=0.15, color=K)
        self.c_out = Dot3D(A(2.9, 0.7), radius=0.15, color=K)
        self.h_out = Dot3D(A(2.9, -0.2), radius=0.15, color=K)
        self.x_pairs = [(A(-0.2, -1.9), A(x, -0.42)) for x in self.gx.values()]
        self.g_pairs = [(A(self.gx["f"], 0.02), A(self.gx["f"], 0.7)), (A(self.gx["i"], 0.02), A(self.gx["i"], 0.7))]
        self.o_pair = (A(self.gx["o"] + 0.21, -0.2), A(2.9, -0.2))
        lines = [Line(a, b, color=K, stroke_width=2.5) for a, b in self.x_pairs + self.g_pairs + [self.o_pair]]
        self.lines = VGroup(*lines)
        self.group = VGroup(self.frame, self.c_line, self.lines, *self.gates.values(),
                            self.x_in, self.c_out, self.h_out)

    def reveal(self, scene, run=1.6):
        scene.play(Create(self.frame), Create(self.c_line), run_time=run * 0.4)
        scene.play(*[FadeIn(g) for g in self.gates.values()], FadeIn(self.x_in), FadeIn(self.c_out),
                   FadeIn(self.h_out), Create(self.lines), run_time=run * 0.6)
        scene.keep(self.group)
        A = self.A
        tags(scene, [("$f_t$", A(self.gx["f"] + 0.35, 0.25)), ("$i_t$", A(self.gx["i"] + 0.35, 0.25)),
                     ("$o_t$", A(self.gx["o"], 0.35)), ("$c_t$", A(2.9, 1.05)),
                     ("$x_t$", A(-0.2, -2.3)), ("$h_t$", A(2.9, -0.6))], 24)

    def fire(self, scene, step=0.5):
        scene.play(lit(self.x_in), run_time=step * 0.4)
        flashes(scene, self.x_pairs, run=step)
        scene.play(*[lit(g) for g in self.gates.values()], run_time=step * 0.4)
        flashes(scene, self.g_pairs + [self.c_pair], run=step * 1.4)
        scene.play(lit(self.c_out), run_time=step * 0.4)
        flashes(scene, [self.o_pair], run=step)
        scene.play(lit(self.h_out), run_time=step * 0.4)

    def reset(self, scene, run=0.5):
        parts = list(self.gates.values()) + [self.x_in, self.c_out, self.h_out]
        scene.play(*[unlit(m) for m in parts], run_time=run)


class Attention3D:
    def __init__(self, n=5, cell=0.45, gap=0.1, seed=1, sharp=2.2, at=ORIGIN):
        at = np.array(at, dtype=float)
        rng = np.random.default_rng(seed)
        S = rng.normal(0, 1, (n, n)) + sharp * np.eye(n)
        E = np.exp(S); self.W = E / E.sum(axis=1, keepdims=True)
        self.n, self.at, self.span = n, at, n * (cell + gap) / 2
        self.bars = bars3d(self.W, cell=cell, gap=gap, height_scale=3.0, at=at)
        self.group = VGroup(self.bars)

    def reveal(self, scene, run=1.6):
        scene.play(LaggedStart(*[FadeIn(b) for b in self.bars], lag_ratio=0.04), run_time=run)
        scene.keep(self.group)
        tags(scene, [("queries", self.at + np.array([-(self.span + 0.7), 0, 0.3])),
                     ("keys", self.at + np.array([0, -(self.span + 0.5), 0.0]))])

    def focus(self, scene, q, run=0.6):
        scene.play(*[lit(self.bars[q * self.n + j]) for j in range(self.n)], run_time=run)

    def unfocus(self, scene, q, run=0.4):
        scene.play(*[unlit(self.bars[q * self.n + j]) for j in range(self.n)], run_time=run)

    def sweep(self, scene, rows=None, run=0.6):
        for q in (range(self.n) if rows is None else rows):
            self.focus(scene, q, run); self.unfocus(scene, q)


# -------------------------------------------------------- training / graphs
class CompGraph3D:
    def __init__(self, nodes, edges, at=ORIGIN):
        at = np.array(at, dtype=float)
        self.pos, self.mob, self.label, self.edges = {}, {}, {}, list(edges)
        for name, (p, kind, label) in nodes.items():
            P = at + np.array(p, dtype=float); self.pos[name] = P; self.label[name] = label
            if kind == "var":
                self.mob[name] = box((0.4, 0.4, 0.4), P)
            elif kind == "op":
                self.mob[name] = sphere(0.28, P)
            else:
                self.mob[name] = box((0.55, 0.55, 0.55), P)
        self.lines = {e: Line(self.pos[e[0]], self.pos[e[1]], color=K, stroke_width=3) for e in self.edges}
        self.group = VGroup(*self.mob.values(), *self.lines.values())
        self.order = self._topo()

    @staticmethod
    def linear_loss(at=ORIGIN):
        nodes = {"x": ([-3, 0, 1.2], "var", "$x$"), "w": ([-3, 0, -1.2], "var", "$w$"),
                 "m": ([-1, 0, 0], "op", r"$\times$"), "b": ([-1, 0, -1.8], "var", "$b$"),
                 "a": ([1, 0, -0.2], "op", "$+$"), "y": ([1, 0, 1.8], "var", "$y$"),
                 "L": ([3, 0, 0.8], "loss", "$L$")}
        edges = [("x", "m"), ("w", "m"), ("m", "a"), ("b", "a"), ("a", "L"), ("y", "L")]
        return CompGraph3D(nodes, edges, at)

    def _topo(self):
        indeg = {n: 0 for n in self.pos}
        for a, b in self.edges:
            indeg[b] += 1
        queue = [n for n, d in indeg.items() if d == 0]; out = []
        while queue:
            n = queue.pop(0); out.append(n)
            for a, b in self.edges:
                if a == n:
                    indeg[b] -= 1
                    if indeg[b] == 0:
                        queue.append(b)
        return out

    def reveal(self, scene, run=1.6):
        scene.play(*[FadeIn(m) for m in self.mob.values()], *[Create(l) for l in self.lines.values()], run_time=run)
        scene.keep(self.group)
        tags(scene, [(self.label[n], self.pos[n] + np.array([0, 0, 0.55])) for n in self.pos], 26)

    def forward(self, scene, step=0.5):
        for n in self.order:
            incoming = [(self.pos[a], self.pos[b]) for a, b in self.edges if b == n]
            flashes(scene, incoming, run=step)
            scene.play(lit(self.mob[n]), run_time=step * 0.4)

    def backward(self, scene, step=0.5):
        for n in reversed(self.order):
            parents = [(self.pos[b], self.pos[a]) for a, b in self.edges if b == n]
            if parents:
                flashes(scene, parents, run=step)
                scene.play(*[lit(self.mob[a]) for a, b in self.edges if b == n], run_time=step * 0.4)

    def reset(self, scene, run=0.5):
        scene.play(*[unlit(m) for m in self.mob.values()], run_time=run)


def descent_path(fn, start, lr=0.1, steps=30, momentum=0.0, eps=1e-4):
    x = np.array(start, dtype=float); v = np.zeros(2); pts = [x.copy()]
    for _ in range(steps):
        g = np.array([(fn(x[0] + eps, x[1]) - fn(x[0] - eps, x[1])) / (2 * eps),
                      (fn(x[0], x[1] + eps) - fn(x[0], x[1] - eps)) / (2 * eps)])
        v = momentum * v - lr * g
        x = x + v; pts.append(x.copy())
    return pts


class LossLandscape:
    def __init__(self, fn=None, rng=2.5, res=(22, 22)):
        self.fn = fn or (lambda u, v: 0.1 * u * u + 0.3 * v * v)
        self.axes = axes3d((-rng, rng, 1), (-rng, rng, 1), (0, 3, 1), (2 * rng, 2 * rng, 3))
        self.surf = surface(self.fn, (-rng, rng), (-rng, rng), res)
        self.group = VGroup(self.axes, self.surf)

    def reveal(self, scene, run=1.6):
        scene.play(Create(self.axes), Create(self.surf), run_time=run)
        scene.keep(self.group)

    def descend(self, scene, start=(2.2, 1.8), lr=2.4, steps=10, momentum=0.0, step_run=0.3, dashed=False):
        pts = descent_path(self.fn, start, lr, steps, momentum)
        P = [np.array([p[0], p[1], self.fn(p[0], p[1]) + 0.07]) for p in pts]
        dot = Dot3D(P[0], radius=0.14, color=ACCENT)
        scene.play(FadeIn(dot), run_time=0.4)
        trail = VGroup()
        for a, b in zip(P[:-1], P[1:]):
            seg = segment(a, b, width=4, dashed=dashed)
            scene.play(dot.animate.move_to(b), Create(seg), run_time=step_run)
            trail.add(seg)
        scene.keep(dot, trail)
        return dot, trail, P


def gradient_arrow(fn, p, scale=1.5, eps=1e-4, descent=True):
    g = np.array([(fn(p[0] + eps, p[1]) - fn(p[0] - eps, p[1])) / (2 * eps),
                  (fn(p[0], p[1] + eps) - fn(p[0], p[1] - eps)) / (2 * eps)])
    n = np.linalg.norm(g)
    d = (g / n if n > 1e-9 else np.zeros(2)) * (-1 if descent else 1) * scale
    a = np.array([p[0], p[1], fn(p[0], p[1]) + 0.07])
    return arrow3d(a, a + np.array([d[0], d[1], 0.0]), color=ACCENT)


class Autoencoder3D(Net3D):
    def __init__(self, enc=(6, 4), code=2, **kw):
        super().__init__(tuple(enc) + (code,) + tuple(reversed(enc)), **kw)
        self.code_idx = len(enc)

    def reveal(self, scene, run=3.0):
        Net3D.reveal(self, scene, run)
        scene.keep(self.group)
        zt = max(p[2] for pts in self.pos for p in pts) + 0.9
        y0 = self.pos[self.code_idx][0][1]
        ex = np.mean([self.pos[i][0][0] for i in range(self.code_idx)])
        dx = np.mean([self.pos[i][0][0] for i in range(self.code_idx + 1, len(self.layers))])
        cx = self.pos[self.code_idx][0][0]
        tags(scene, [("encoder", [ex, y0, zt]), ("code", [cx, y0, zt]), ("decoder", [dx, y0, zt])], 26)

    def squeeze(self, scene, run=0.8):
        scene.play(*[lit(d) for d in self.nodes[self.code_idx]], run_time=run)


def dropout(scene, net, layer, idx, run=0.6):
    scene.play(*[net.nodes[layer][k].animate.set_opacity(0.12) for k in idx], run_time=run)


def undrop(scene, net, layer, idx, run=0.5):
    scene.play(*[net.nodes[layer][k].animate.set_opacity(1.0) for k in idx], run_time=run)


def backprop(scene, net, step=0.6):
    L = len(net.layers)
    scene.play(*[lit(d) for d in net.nodes[L - 1]], run_time=step * 0.6)
    for i in range(L - 1, 0, -1):
        pairs = [(q, p) for p in net.pos[i - 1] for q in net.pos[i]]
        pairs = pairs[::max(1, int(np.ceil(len(pairs) / 60)))]
        scene.play(*[lit(d) for d in net.nodes[i - 1]],
                   *[ShowPassingFlash(Line(a, b, color=ACCENT, stroke_width=3.5), time_width=0.8) for a, b in pairs],
                   run_time=step)


class ResBlock3D:
    def __init__(self, at=ORIGIN, gap=1.8):
        at = np.array(at, dtype=float)
        xs = [(k - 1.5) * gap for k in range(4)]
        self.P = [at + np.array([x, 0, 0]) for x in xs]
        self.at = at
        self.inp = Dot3D(self.P[0], radius=0.16, color=K)
        self.l1 = box((0.5, 1.0, 1.0), self.P[1]); self.l2 = box((0.5, 1.0, 1.0), self.P[2])
        self.add_node = sphere(0.3, self.P[3])
        R = (xs[3] - xs[0]) / 2; cx = at + np.array([(xs[0] + xs[3]) / 2, 0, 0])
        self.skip = curve3d(lambda t: [cx[0] - R * np.cos(t), cx[1], cx[2] + 1.6 * np.sin(t)], (0, PI), K, 4)
        dx = np.array([0.25, 0, 0])
        self.segs = [(self.P[0], self.P[1] - dx), (self.P[1] + dx, self.P[2] - dx),
                     (self.P[2] + dx, self.P[3] - np.array([0.3, 0, 0]))]
        self.lines = VGroup(*[Line(a, b, color=K, stroke_width=3) for a, b in self.segs])
        self.group = VGroup(self.inp, self.l1, self.l2, self.add_node, self.lines, self.skip)

    def reveal(self, scene, run=1.6):
        scene.play(FadeIn(self.inp), FadeIn(self.l1), FadeIn(self.l2), FadeIn(self.add_node),
                   Create(self.lines), Create(self.skip), run_time=run)
        scene.keep(self.group)
        tags(scene, [("$x$", self.P[0] + np.array([0, 0, -0.5])), ("$F(x)$", self.P[1] + np.array([0.9, 0, 0.9])),
                     ("$x+F(x)$", self.P[3] + np.array([0, 0, 0.6])), ("skip", self.at + np.array([0, 0, 2.0]))], 24)

    def fire(self, scene, step=0.6):
        scene.play(lit(self.inp), run_time=step * 0.4)
        flashes(scene, [self.segs[0]], run=step); scene.play(lit(self.l1), run_time=step * 0.4)
        flashes(scene, [self.segs[1]], run=step); scene.play(lit(self.l2), run_time=step * 0.4)
        flashes(scene, [self.segs[2]], run=step)
        scene.play(ShowPassingFlash(self.skip.copy().set_stroke(ACCENT, width=6), time_width=0.6), run_time=step * 1.6)
        scene.play(lit(self.add_node), run_time=step * 0.4)

    def reset(self, scene, run=0.5):
        scene.play(*[unlit(m) for m in (self.inp, self.l1, self.l2, self.add_node)], run_time=run)


# ------------------------------------------------------------- classic ML
def sigmoid_surface(w=(1.2, 0.8), b=0.0, rng=3.0, height=2.0, res=(24, 24)):
    f = lambda u, v: height / (1 + np.exp(-(w[0] * u + w[1] * v + b)))
    return surface(f, (-rng, rng), (-rng, rng), res)


def boundary_line(w=(1.2, 0.8), b=0.0, rng=3.0, z=0.0, dashed=False, width=5):
    n = np.array(w, dtype=float); p0 = -b * n / np.dot(n, n)
    d = np.array([-n[1], n[0]]) / np.linalg.norm(n)
    ts = np.linspace(-12, 12, 4801)
    pts = p0[None, :] + ts[:, None] * d[None, :]
    mask = (np.abs(pts) <= rng).all(axis=1)
    if not mask.any():
        raise ValueError("boundary_line: line is outside the plotted range")
    a, c = pts[mask][0], pts[mask][-1]
    return segment([a[0], a[1], z], [c[0], c[1], z], width=width, dashed=dashed)


def blobs2d(n=12, seed=2, sep=2.4, spread=0.55, direction=(1, 1), z=0.06):
    rng = np.random.default_rng(seed); d = _u(list(direction) + [0.0])[:2]
    pos_pts = [np.array([*(d * sep / 2 + rng.normal(0, spread, 2)), z]) for _ in range(n)]
    neg_pts = [np.array([*(-d * sep / 2 + rng.normal(0, spread, 2)), z]) for _ in range(n)]
    pos = VGroup(*[Dot3D(p, radius=0.11, color=K) for p in pos_pts])
    neg = VGroup(*[box((0.22, 0.22, 0.22), p, sw=1.5) for p in neg_pts])
    return pos, neg, pos_pts, neg_pts


class KMeans3D:
    def __init__(self, k=3, per=8, seed=4, spread=0.45, at=ORIGIN):
        at = np.array(at, dtype=float); rng = np.random.default_rng(seed)
        preset = [(-2, -1, 0.5), (2, -1, 0.0), (0, 2, 1.0), (0, -2, 1.5)]
        centers = np.array(preset[:k], dtype=float)
        pts = np.vstack([c + rng.normal(0, spread, (per, 3)) for c in centers]) + at
        self.k, self.pts = k, pts
        cent = pts[[0, 1, per, per + 1][:k]].copy()
        self.init = [c.copy() for c in cent]; self.steps = []
        for _ in range(6):
            d = np.linalg.norm(pts[:, None, :] - cent[None, :, :], axis=2); a = d.argmin(1)
            new = np.array([pts[a == j].mean(0) if (a == j).any() else cent[j] for j in range(k)])
            self.steps.append((a.copy(), new.copy()))
            if np.allclose(new, cent):
                break
            cent = new
        self.dots = VGroup(*[Dot3D(p, radius=0.1, color=K) for p in pts])
        self.cents = [box((0.3, 0.3, 0.3), c) for c in self.init]
        self.cur = [c.copy() for c in self.init]
        self.group = VGroup(self.dots, *self.cents)

    def reveal(self, scene, run=1.2):
        scene.play(FadeIn(self.dots), run_time=run)
        scene.play(*[GrowFromCenter(c) for c in self.cents], run_time=0.6)
        scene.keep(self.group)

    def step(self, scene, i, run=1.0):
        a, new = self.steps[i]
        lines = VGroup(*[Line(self.pts[n], self.cur[a[n]], color=K, stroke_width=1.5, stroke_opacity=0.6)
                         for n in range(len(self.pts))])
        scene.play(Create(lines, lag_ratio=0.02), run_time=run * 0.6)
        scene.play(*[self.cents[j].animate.move_to(new[j]).set_fill(ACCENT, opacity=0.9) for j in range(self.k)],
                   run_time=run * 0.8)
        scene.play(FadeOut(lines), *[unlit(c) for c in self.cents], run_time=run * 0.4)
        self.cur = [new[j].copy() for j in range(self.k)]


class SVMMargin3D:
    def __init__(self, n=8, seed=3, sep=3.0, spread=0.4, size=2.8, at=ORIGIN):
        at = np.array(at, dtype=float); u = _u((1, 1, 1)); self.u = u
        self.pos, self.neg, pp, nn = scatter_classes(n, seed, sep, spread, at)
        dp = np.array([float(np.dot(p - at, u)) for p in pp])
        dn = np.array([float(np.dot(p - at, u)) for p in nn])
        self.ip = int(np.argmin(np.abs(dp))); self.in_ = int(np.argmin(np.abs(dn)))
        m_pos, m_neg = abs(dp[self.ip]), abs(dn[self.in_])
        off = (m_pos - m_neg) / 2
        self.plane = plane_poly(at + u * off, u, size, 0.22)
        half = max((m_pos + m_neg) / 2, 0.1)
        self.mp = [plane_poly(at + u * (off + half), u, size, 0.08), plane_poly(at + u * (off - half), u, size, 0.08)]
        self.group = VGroup(self.pos, self.neg, self.plane)

    def reveal(self, scene, run=1.4):
        scene.play(FadeIn(self.pos), FadeIn(self.neg), FadeIn(self.plane), run_time=run)
        scene.keep(self.group)

    def show_margin(self, scene, run=1.0):
        scene.play(*[FadeIn(p) for p in self.mp], run_time=run)
        scene.keep(*self.mp)

    def highlight_support(self, scene, run=0.8):
        scene.play(lit(self.pos[self.ip]), lit(self.neg[self.in_]), run_time=run)


class DecisionTree3D:
    def __init__(self, depth=3, width=6.0, drop=1.4, at=ORIGIN):
        at = np.array(at, dtype=float); self.depth = depth; self.pos = {}
        for d in range(depth + 1):
            for i in range(2 ** d):
                self.pos[(d, i)] = at + np.array([(i + 0.5) * width / 2 ** d - width / 2, 0, 1.6 - d * drop])
        self.mob = {k: (sphere(0.22, p) if k[0] < depth else box((0.3, 0.3, 0.3), p)) for k, p in self.pos.items()}
        self.lines = {}
        for (d, i), p in self.pos.items():
            if d < depth:
                for c in (0, 1):
                    ch = (d + 1, 2 * i + c)
                    self.lines[((d, i), ch)] = Line(p, self.pos[ch], color=K, stroke_width=3)
        self.group = VGroup(*self.mob.values(), *self.lines.values())

    def reveal(self, scene, run=1.6):
        scene.play(*[FadeIn(m) for m in self.mob.values()], *[Create(l) for l in self.lines.values()], run_time=run)
        scene.keep(self.group)
        tags(scene, [("$x_1<t$", self.pos[(0, 0)] + np.array([0, 0, 0.5]))], 24)

    def fire_path(self, scene, path=(0, 1, 0), step=0.6):
        if len(path) > self.depth:
            raise ValueError("path longer than tree depth")
        key = (0, 0)
        scene.play(lit(self.mob[key]), run_time=step * 0.4)
        for c in path:
            child = (key[0] + 1, 2 * key[1] + c)
            flashes(scene, [(self.pos[key], self.pos[child])], run=step)
            scene.play(lit(self.mob[child]), run_time=step * 0.4)
            key = child

    def reset(self, scene, run=0.5):
        scene.play(*[unlit(m) for m in self.mob.values()], run_time=run)


def embedding_cloud(k=3, per=9, seed=5, spread=0.5, rng_=2.2, at=ORIGIN):
    at = np.array(at, dtype=float); rng = np.random.default_rng(seed)
    centers = rng.uniform(-rng_, rng_, (k, 3))
    pts = [at + centers[j] + rng.normal(0, spread, 3) for j in range(k) for _ in range(per)]
    return VGroup(*[Dot3D(p, radius=0.09, color=K) for p in pts]), pts


def show_neighbors(scene, grp, pts, idx=0, k=3, run=1.0):
    d = [float(np.linalg.norm(p - pts[idx])) for p in pts]
    order = [int(j) for j in np.argsort(d)[1:k + 1]]
    lines = VGroup(*[Line(pts[idx], pts[j], color=ACCENT, stroke_width=3) for j in order])
    scene.play(lit(grp[idx]), *[lit(grp[j]) for j in order], *[Create(l) for l in lines], run_time=run)
    scene.keep(lines)
    return lines


def batch_stack(n=4, size=4, cell=0.32, gap_z=0.5, at=ORIGIN):
    return VGroup(*[matrix_grid(size, size, cell, at, z=(k - (n - 1) / 2) * gap_z) for k in range(n)])
