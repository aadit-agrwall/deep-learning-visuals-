import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from manim import *


from manim import *

from components.matrix import Matrix2D


class TestMatrix(Scene):

    def construct(self):

        matrix = Matrix2D(
            [
                [1, 2],
                [3, 4],
            ]
        )

        self.play(matrix.create_animation())
        self.wait()

        self.play(matrix.highlight_element(0, 0))
        self.wait()

        self.play(matrix.highlight_row(1))
        self.wait()

        self.play(matrix.highlight_column(1))
        self.wait()

        self.play(matrix.update_value(0, 1, 10))
        self.wait()

        self.play(matrix.swap_rows(0, 1))
        self.wait()

        self.play(matrix.swap_columns(0, 1))
        self.wait()

        self.play(matrix.reset())
        self.wait(2)