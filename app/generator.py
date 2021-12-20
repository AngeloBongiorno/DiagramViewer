from typing import Any
import PIL

from app.model import Diagram

class Generatore:

    def __init__(self, diagram: Diagram) -> None:
        self.bg = self.setBackground(diagram)

    # funzione sfondo
    def setBackground(self, diagram: Diagram) -> Any:
        bg = PIL.Image.new('RGBA', diagram.size, diagram.color)
        
        return bg
        # v test
        bg.show()
        # ^ test

# funzione linea association

# funzione linea generalization

# funzione quadrato