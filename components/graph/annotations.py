from __future__ import annotations

from manim import *

from components.graph.labels import (
    AnnotationLabel,
    NumberBadge,
)

from components.graph.arrows import (
    AnnotationArrow,
)


# ==========================================================
# Base Annotation
# ==========================================================

class BaseAnnotation(VGroup):
    """
    Base class for every annotation.

    Contains

        Label
            ↓
          Arrow
            ↓
         Target
    """

    def __init__(
        self,
        label,
        arrow,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.label = label
        self.arrow = arrow

        self.add(
            label,
            arrow,
        )


# ==========================================================
# Label Annotation
# ==========================================================

class LabelAnnotation(BaseAnnotation):
    """
    Example

    Human
        ↘
          curve
    """

    def __init__(
        self,
        text,
        target,
        position,
        font_size=22,
        **kwargs,
    ):

        label = AnnotationLabel(
            text,
            font_size=font_size,
        )

        label.move_to(position)

        arrow = AnnotationArrow(
            label,
            target,
        )

        super().__init__(
            label,
            arrow,
            **kwargs,
        )


# ==========================================================
# Number Annotation
# ==========================================================

class NumberAnnotation(BaseAnnotation):
    """
    Figure 1.10 style

        (7)
          ↘
           point
    """

    def __init__(
        self,
        number,
        target,
        position,
        **kwargs,
    ):

        badge = NumberBadge(number)

        badge.move_to(position)

        arrow = AnnotationArrow(
            badge,
            target,
        )

        super().__init__(
            badge,
            arrow,
            **kwargs,
        )


# ==========================================================
# Box Annotation
# ==========================================================

class BoxAnnotation(BaseAnnotation):
    """
    Box label connected with arrow.
    """

    def __init__(
        self,
        box,
        target,
        position,
        **kwargs,
    ):

        box.move_to(position)

        arrow = AnnotationArrow(
            box,
            target,
        )

        super().__init__(
            box,
            arrow,
            **kwargs,
        )


# ==========================================================
# Coordinate Annotation
# ==========================================================

class CoordinateAnnotation(BaseAnnotation):
    """
    Annotation using graph coordinates.

    Example

    CoordinateAnnotation(
        graph,
        "Human",
        (1975,120),
        target
    )
    """

    def __init__(
        self,
        graph,
        text,
        coordinate,
        target,
        log_scale=False,
        font_size=22,
        **kwargs,
    ):

        label = AnnotationLabel(
            text,
            font_size=font_size,
        )

        if log_scale:
            label.move_to(
                graph.point(*coordinate)
            )
        else:
            label.move_to(
                graph.c2p(*coordinate)
            )

        arrow = AnnotationArrow(
            label,
            target,
        )

        super().__init__(
            label,
            arrow,
            **kwargs,
        )


# ==========================================================
# Multi Annotation
# ==========================================================

class AnnotationGroup(VGroup):
    """
    Collection of annotations.
    """

    def __init__(
        self,
        annotations,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.annotations = VGroup()

        for annotation in annotations:
            self.annotations.add(annotation)

        self.add(self.annotations)


# ==========================================================
# Figure 1.10 Annotation
# ==========================================================

class Figure110Annotation(LabelAnnotation):
    """
    Default annotation style
    used in Figure 1.10.
    """

    def __init__(
        self,
        text,
        target,
        position,
        **kwargs,
    ):

        super().__init__(
            text=text,
            target=target,
            position=position,
            font_size=22,
            **kwargs,
        )


# ==========================================================
# Figure 1.10 Number Annotation
# ==========================================================

class Figure110Number(NumberAnnotation):
    """
    Default numbered callout
    used in Figure 1.10.
    """

    def __init__(
        self,
        number,
        target,
        position,
        **kwargs,
    ):

        super().__init__(
            number=number,
            target=target,
            position=position,
            **kwargs,
        )