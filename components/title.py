from manim import *
from themes.deep_learning import *

class DLTitle(Text):
    def __init__(self, text):
        super().__init__(
            text,
            font_size=TITLE_SIZE,
            color=TEXT,
            weight=BOLD,
        )
        self.to_edge(UP)