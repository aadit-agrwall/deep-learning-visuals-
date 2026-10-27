import sys
from pathlib import Path

# Add the project root to Python's import path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from manim import *
from components.title import DLTitle


class Page001(Scene):
    def construct(self):
        title = DLTitle("Count 14 of 723")

        self.play(Write(title))
        self.wait()

        self.play(title.animate.scale(0.8))
        self.wait()