"""
common/ml_objects.py

Higher-level, reusable compositions built on top of the existing
components.neural_network.NeuralNetwork class. Adds common
scene-level patterns (labeled networks, training-step animations,
loss annotations) without reimplementing network construction.
"""

from manim import VGroup, Text, DOWN, UP, Write, FadeIn

from common.styles import text_style
from common.colors import get_color


def labeled_network(network_mobject, label: str, chapter: str = None, label_buff: float = 0.5):
    """Attach a title label above a NeuralNetwork instance."""
    label_text = Text(label, **text_style("subtitle", chapter=chapter))
    label_text.next_to(network_mobject, UP, buff=label_buff)
    return VGroup(label_text, network_mobject)


def show_network(scene, network_mobject, run_time: float = 1.5):
    """Standard reveal animation for a network (wraps its own create_animation)."""
    scene.play(network_mobject.create_animation(), run_time=run_time)


def run_forward_pass(scene, network_mobject, chapter: str = None, run_time: float = 2.0):
    """
    Run the network's existing forward_pass animation using the
    chapter's accent color as the default signal color.
    """
    signal_color = get_color("accent", chapter=chapter)
    scene.play(
        network_mobject.animate_connections(color=signal_color)
        if hasattr(network_mobject, "animate_connections")
        else network_mobject.forward_pass(signal_color=signal_color),
        run_time=run_time,
    )


def highlight_layer_sequence(scene, network_mobject, layer_indices, chapter: str = None, run_time: float = 0.5):
    """
    Highlight a sequence of layers one after another (e.g. to
    narrate forward propagation layer-by-layer), then reset colors.
    """
    color = get_color("primary", chapter=chapter)
    for index in layer_indices:
        network_mobject.highlight_layer(index, color=color)
        scene.wait(run_time)
    network_mobject.reset_colors(color=get_color("neuron", chapter=chapter))


def add_loss_annotation(network_mobject, loss_value: float, chapter: str = None, decimals: int = 4):
    """
    Attach a small loss-value text label below a network, useful
    for training-progress figures.
    """
    from common.utils import format_number
    text = Text(
        f"Loss: {format_number(loss_value, decimals=decimals)}",
        **text_style("caption", chapter=chapter),
    )
    text.next_to(network_mobject, DOWN, buff=0.4)
    return VGroup(network_mobject, text)


def io_labels(network_mobject, input_labels, output_labels, chapter: str = None):
    """
    Add simple text labels for a network's input and output layers,
    positioned to the left/right of the network respectively.
    """
    from manim import LEFT, RIGHT
    labels = VGroup()
    for i, text in enumerate(input_labels):
        t = Text(text, **text_style("caption", chapter=chapter))
        labels.add(t)
    for i, text in enumerate(output_labels):
        t = Text(text, **text_style("caption", chapter=chapter))
        labels.add(t)
    return labels
