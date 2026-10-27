"""
common/camera.py

Shared camera movement helpers for Manim scenes.
Note: these assume a MovingCameraScene (camera.frame must exist).
"""

from manim import ORIGIN, VGroup


def zoom_to(scene, mobject, margin: float = 1.2, run_time: float = 1.5):
    """Animate the camera frame to fit `mobject` with a margin multiplier."""
    target_width = mobject.width * margin
    target_height = mobject.height * margin
    scene.play(
        scene.camera.frame.animate.move_to(mobject.get_center()).set(
            width=max(target_width, target_height)
        ),
        run_time=run_time,
    )


def reset_camera(scene, run_time: float = 1.0):
    """Return the camera frame to its default centered, full-frame state."""
    default_width = scene.camera.frame.width
    scene.play(
        scene.camera.frame.animate.move_to(ORIGIN).set(width=default_width),
        run_time=run_time,
    )


def pan_to(scene, point, run_time: float = 1.0):
    """Move the camera frame's center to a specific point without zooming."""
    scene.play(scene.camera.frame.animate.move_to(point), run_time=run_time)


def frame_around(scene, mobjects, margin: float = 1.2, run_time: float = 1.5):
    """Zoom/pan the camera to fit a collection of mobjects together."""
    group = VGroup(*mobjects)
    zoom_to(scene, group, margin=margin, run_time=run_time)
