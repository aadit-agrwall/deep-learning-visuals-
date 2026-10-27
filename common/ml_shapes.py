"""
common/ml_shapes.py

Reusable ML/DL diagram-piece library for Chapter 5+ animations. Every
function returns a plain VGroup (or similar), centered near its own
local origin, so the caller positions it with .move_to() / .next_to() /
.to_edge() as usual. Functions here do NOT call self.play() — building
the mobject and animating it in are kept separate so the same shape can
be revealed with Create, FadeIn, type_in, or a custom build-up.

Optional "animate_*" helpers at the bottom DO take a Scene and perform a
standard reveal sequence for the more complex composite shapes (e.g. a
neural net revealing layer by layer).

Usage:

    from common.ml_shapes import neuron_node, neural_net, dataset_table, \
        loss_curve, gradient_arrow, matrix_grid, pixel_grid, tree_node, \
        animate_neural_net_buildup
    from common import palette as pal

    net = neural_net([3, 4, 4, 2], colors=[pal.INPUT, pal.FORMULA, pal.FORMULA, pal.OUTPUT])
    net.move_to(ORIGIN)
    animate_neural_net_buildup(self, net)
"""

import numpy as np
from manim import *

from common import palette as pal


# ====================================================================
# 1. SINGLE NEURON / NODE
# ====================================================================

def neuron_node(label="", color=None, radius=0.32, fill_opacity=0.15,
                 label_size=18, label_color=None):
    """A single circular neuron/node, optionally labeled."""
    if color is None:
        color = pal.INPUT
    if label_color is None:
        label_color = pal.TEXT

    circle = Circle(radius=radius, color=color, stroke_width=2.6,
                     fill_color=color, fill_opacity=fill_opacity)
    group = VGroup(circle)
    if label:
        lbl = Text(label, font="DejaVu Sans", font_size=label_size, color=label_color)
        lbl.move_to(circle.get_center())
        group.add(lbl)
    group.circle_ref = circle
    return group


# ====================================================================
# 2. SMALL NEURAL NETWORK (fully connected, layer by layer)
# ====================================================================

def neural_net(layer_sizes, colors=None, node_radius=0.22,
                h_spacing=1.5, v_spacing=0.55, edge_color=None,
                edge_opacity=0.35, edge_stroke_width=1.2):
    """
    Builds a fully-connected feedforward net diagram.

    layer_sizes: list of ints, e.g. [3, 4, 4, 2]
    colors: optional list of colors, one per layer (defaults to a
            input->hidden->output gradient using the palette)
    Returns a VGroup with attributes:
        .layers -> list of VGroup(node, node, ...) per layer
        .edges  -> VGroup of all connecting Lines
    """
    n_layers = len(layer_sizes)
    if colors is None:
        if n_layers == 1:
            colors = [pal.INPUT]
        else:
            colors = [pal.INPUT] + [pal.FORMULA] * (n_layers - 2) + [pal.OUTPUT]
    if edge_color is None:
        edge_color = pal.TEXT_DIM

    layers = []
    for li, size in enumerate(layer_sizes):
        layer_nodes = VGroup()
        for ni in range(size):
            node = neuron_node(color=colors[li], radius=node_radius)
            y = (size - 1) / 2 * v_spacing - ni * v_spacing
            x = li * h_spacing
            node.move_to(np.array([x, y, 0]))
            layer_nodes.add(node)
        layers.append(layer_nodes)

    edges = VGroup()
    for li in range(n_layers - 1):
        for a in layers[li]:
            for b in layers[li + 1]:
                line = Line(
                    a.circle_ref.get_center(), b.circle_ref.get_center(),
                    color=edge_color, stroke_width=edge_stroke_width,
                    stroke_opacity=edge_opacity,
                )
                edges.add(line)

    net = VGroup(edges, *layers)
    net.layers = layers
    net.edges = edges
    net.move_to(ORIGIN)
    return net


# ====================================================================
# 3. DATASET TABLE
# ====================================================================

def dataset_table(headers, rows, col_width=1.3, row_height=0.55,
                   header_color=None, cell_color=None, line_color=None,
                   font_size=14):
    """
    Simple grid-line table for showing a dataset.

    headers: list[str], e.g. ["x1", "x2", "y"]
    rows: list[list[str]], e.g. [["1.2", "0.4", "A"], ["0.8", "1.1", "B"]]
    """
    if header_color is None:
        header_color = pal.FORMULA
    if cell_color is None:
        cell_color = pal.TEXT
    if line_color is None:
        line_color = pal.TEXT_DIM

    n_cols = len(headers)
    n_rows = len(rows) + 1  # +1 for header row

    width = col_width * n_cols
    height = row_height * n_rows

    outline = Rectangle(width=width, height=height, color=line_color, stroke_width=2)

    h_lines = VGroup()
    for i in range(1, n_rows):
        y = height / 2 - i * row_height
        h_lines.add(Line(
            np.array([-width / 2, y, 0]), np.array([width / 2, y, 0]),
            color=line_color, stroke_width=1.2,
        ))

    v_lines = VGroup()
    for j in range(1, n_cols):
        x = -width / 2 + j * col_width
        v_lines.add(Line(
            np.array([x, height / 2, 0]), np.array([x, -height / 2, 0]),
            color=line_color, stroke_width=1.2,
        ))

    text_group = VGroup()
    for j, h in enumerate(headers):
        cell_x = -width / 2 + col_width * (j + 0.5)
        cell_y = height / 2 - row_height * 0.5
        t = Text(str(h), font="DejaVu Sans Mono", font_size=font_size,
                  color=header_color, weight=BOLD)
        t.move_to(np.array([cell_x, cell_y, 0]))
        text_group.add(t)

    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell_x = -width / 2 + col_width * (j + 0.5)
            cell_y = height / 2 - row_height * (i + 1.5)
            t = Text(str(val), font="DejaVu Sans Mono", font_size=font_size, color=cell_color)
            t.move_to(np.array([cell_x, cell_y, 0]))
            text_group.add(t)

    table = VGroup(outline, h_lines, v_lines, text_group)
    table.move_to(ORIGIN)
    return table


# ====================================================================
# 4. LOSS / TRAINING CURVE
# ====================================================================

def loss_curve(x_range=(0, 10, 2), y_range=(0, 1, 0.25), width=6.0, height=3.0,
                func=None, color=None, stroke_width=3.5, axis_color=None,
                x_label="epoch", y_label="loss", label_size=14):
    """
    Axes + a plotted curve, defaulting to a decaying-loss shape if no
    func is given. Returns VGroup with .axes and .curve attributes.
    """
    if color is None:
        color = pal.ERROR
    if axis_color is None:
        axis_color = pal.TEXT_DIM
    if func is None:
        x0, x1, _ = x_range
        func = lambda x: 0.9 * np.exp(-0.35 * x) + 0.05

    axes = Axes(
        x_range=list(x_range), y_range=list(y_range),
        x_length=width, y_length=height,
        axis_config={"color": axis_color, "stroke_width": 1.4, "include_numbers": False},
    )
    curve = axes.plot(func, x_range=[x_range[0], x_range[1]], color=color, stroke_width=stroke_width)

    group = VGroup(axes, curve)

    if x_label:
        xl = Text(x_label, font="DejaVu Sans", font_size=label_size, color=pal.TEXT)
        xl.next_to(axes.x_axis, DOWN, buff=0.2)
        group.add(xl)
    if y_label:
        yl = Text(y_label, font="DejaVu Sans", font_size=label_size, color=pal.TEXT)
        yl.rotate(PI / 2)
        yl.next_to(axes.y_axis, LEFT, buff=0.25)
        group.add(yl)

    group.axes = axes
    group.curve = curve
    group.move_to(ORIGIN)
    return group


# ====================================================================
# 5. GRADIENT ARROW
# ====================================================================

def gradient_arrow(start_point, end_point, color=None, stroke_width=3.5,
                    label="", label_size=16, label_color=None, buff=0.08):
    """A single directional arrow for gradient-descent-style visuals."""
    if color is None:
        color = pal.FORMULA
    if label_color is None:
        label_color = color

    arrow = Arrow(start_point, end_point, color=color, stroke_width=stroke_width, buff=buff)
    group = VGroup(arrow)
    if label:
        lbl = Text(label, font="DejaVu Sans", font_size=label_size, color=label_color)
        lbl.next_to(arrow.get_center(), UP, buff=0.15)
        group.add(lbl)
    group.arrow_ref = arrow
    return group


# ====================================================================
# 6. MATRIX / VECTOR GRID (labeled cells, e.g. for showing x vectors)
# ====================================================================

def matrix_grid(values, cell_size=0.8, color=None, highlight_indices=None,
                 highlight_color=None, font_size=18):
    """
    A horizontal row of labeled cells, e.g. for a feature vector.

    values: list[str], e.g. ["2.1", "0.4", "?", "5.3"]
    highlight_indices: optional list[int] of cells to color differently
                        (e.g. the missing entry)
    """
    if color is None:
        color = pal.TEXT
    if highlight_color is None:
        highlight_color = pal.ERROR
    if highlight_indices is None:
        highlight_indices = []

    cells = VGroup()
    for i, v in enumerate(values):
        is_hl = i in highlight_indices
        c = highlight_color if is_hl else pal.TEXT
        box = Square(side_length=cell_size, stroke_color=c, stroke_width=2.4,
                     fill_color=c, fill_opacity=0.15 if is_hl else 0)
        label = Text(str(v), font="DejaVu Sans", font_size=font_size, color=c, weight=BOLD)
        label.move_to(box.get_center())
        cells.add(VGroup(box, label))

    cells.arrange(RIGHT, buff=0.18)
    cells.move_to(ORIGIN)
    return cells


# ====================================================================
# 7. PIXEL GRID (image-style NxM shaded grid)
# ====================================================================

def pixel_grid(rows=4, cols=4, color=None, cell_size=0.42, seed=None,
                shade_range=(0.15, 0.9), stroke_color=None, stroke_width=1):
    """
    An NxM grid of shaded squares, for representing an image/feature map.
    Pass a fixed seed for deterministic shading across renders.
    """
    import random as _random
    if color is None:
        color = pal.INPUT
    if stroke_color is None:
        stroke_color = pal.TEXT
    rng = _random.Random(seed)

    grid = VGroup()
    for i in range(rows):
        for j in range(cols):
            shade = rng.uniform(*shade_range)
            cell = Square(side_length=cell_size, fill_color=color, fill_opacity=shade,
                         stroke_color=stroke_color, stroke_width=stroke_width)
            cell.move_to(np.array([j * cell_size, -i * cell_size, 0]))
            grid.add(cell)
    grid.move_to(ORIGIN)
    return grid


def segmentation_grid(category_map, color_map, cell_size=0.55,
                       stroke_color=None, stroke_width=1.5, fill_opacity=0.6):
    """
    Like pixel_grid but each cell's color is semantic (category-based)
    rather than randomly shaded. For pixel-wise segmentation visuals.

    category_map: 2D list of category keys, e.g. [["a","a","b"],["c","c","b"]]
    color_map: dict mapping category key -> color
    """
    if stroke_color is None:
        stroke_color = pal.TEXT

    grid = VGroup()
    rows = len(category_map)
    for i, row in enumerate(category_map):
        for j, key in enumerate(row):
            c = color_map.get(key, pal.TEXT_DIM)
            cell = Square(side_length=cell_size, fill_color=c, fill_opacity=fill_opacity,
                         stroke_color=stroke_color, stroke_width=stroke_width)
            cell.move_to(np.array([j * cell_size, -i * cell_size, 0]))
            grid.add(cell)
    grid.move_to(ORIGIN)
    return grid


# ====================================================================
# 8. TREE NODE (for parse trees / decision trees / hierarchies)
# ====================================================================

def tree_node(label="", color=None, radius=0.22, label_size=14, label_color=None):
    """A single tree node — small labeled dot, for building trees manually
    by connecting with Line() between .node_ref centers."""
    if color is None:
        color = pal.FORMULA
    if label_color is None:
        label_color = pal.TEXT

    dot = Dot(radius=radius, color=color)
    group = VGroup(dot)
    if label:
        lbl = Text(label, font="DejaVu Sans", font_size=label_size, color=label_color)
        lbl.next_to(dot, DOWN, buff=0.12)
        group.add(lbl)
    group.node_ref = dot
    return group


def simple_binary_tree(root_label, left_label, right_label,
                        root_color=None, left_color=None, right_color=None,
                        h_spacing=1.4, v_spacing=0.9, line_color=None):
    """
    Quick 3-node (root + 2 children) tree, common for parsing/decision
    examples. Returns VGroup with .root, .left, .right, .lines attrs.
    """
    if root_color is None:
        root_color = pal.FORMULA
    if left_color is None:
        left_color = pal.INPUT
    if right_color is None:
        right_color = pal.OUTPUT
    if line_color is None:
        line_color = pal.TEXT

    root = tree_node(root_label, color=root_color)
    root.move_to(ORIGIN)

    left = tree_node(left_label, color=left_color)
    left.move_to(np.array([-h_spacing, -v_spacing, 0]))

    right = tree_node(right_label, color=right_color)
    right.move_to(np.array([h_spacing, -v_spacing, 0]))

    line_l = Line(root.node_ref.get_center(), left.node_ref.get_center(),
                  color=line_color, stroke_width=2)
    line_r = Line(root.node_ref.get_center(), right.node_ref.get_center(),
                  color=line_color, stroke_width=2)

    tree = VGroup(line_l, line_r, root, left, right)
    tree.root, tree.left, tree.right = root, left, right
    tree.lines = VGroup(line_l, line_r)
    tree.move_to(ORIGIN)
    return tree


# ====================================================================
# ANIMATE-IN HELPERS (take a Scene, perform a standard reveal)
# ====================================================================

def animate_neural_net_buildup(scene, net, layer_run_time=0.5, edge_run_time=0.5):
    """
    Reveal a neural_net() VGroup layer by layer: nodes in a layer fade in
    together, then the edges connecting to the NEXT layer draw in, then
    repeat. Requires net.layers and net.edges as set by neural_net().
    """
    layers = net.layers
    all_edges = net.edges

    # figure out how many edges connect each consecutive layer pair
    edges_per_gap = []
    idx = 0
    for li in range(len(layers) - 1):
        count = len(layers[li]) * len(layers[li + 1])
        edges_per_gap.append(all_edges[idx:idx + count])
        idx += count

    scene.play(FadeIn(layers[0], lag_ratio=0.1), run_time=layer_run_time)
    for li in range(1, len(layers)):
        scene.play(Create(edges_per_gap[li - 1]), run_time=edge_run_time)
        scene.play(FadeIn(layers[li], lag_ratio=0.1), run_time=layer_run_time)


def animate_highlight_pulse(scene, target, color=None, scale_factor=1.15,
                             run_time_in=0.3, hold=0.3, run_time_out=0.3):
    """
    Briefly scale + color-flash a mobject (e.g. one formula term or one
    diagram box) to draw attention to it, then settle back.
    """
    if color is None:
        color = pal.FORMULA

    original_color = getattr(target, "color", None)
    scene.play(
        target.animate.scale(scale_factor).set_color(color),
        run_time=run_time_in,
    )
    scene.wait(hold)
    restore_kwargs = {"color": original_color} if original_color else {}
    scene.play(
        target.animate.scale(1 / scale_factor),
        run_time=run_time_out,
    )
