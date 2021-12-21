from typing import Any
from PIL import Image

from app.model import Background, Diagram

class Generator:

    def __init__(self, diagram: Diagram) -> None:
        pass

    def draw_diagram(self, diagram: Diagram):
        self.draw_background(diagram.background)

    # funzione sfondo
    def draw_background(self, bg_info: Background) -> Image:
        size = (bg_info.width, bg_info.height)
        bg = Image.new('RGBA', size, bg_info.color)
        return bg

        # v test
        bg.show()
        # ^ test

# funzione linea association

# funzione linea generalization

# funzione quadrato