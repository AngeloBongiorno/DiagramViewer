from typing import Any, List
from PIL import Image, ImageDraw
from model import Connector, Shape

from model import Background, Diagram

class Generator:

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram
        pass

    def draw_diagram(self):
        img = self.draw_background(self.diagram.background)
        if len(self.diagram.connectors) != 0:
            img = self.draw_connectors(img, self.diagram.connectors)
        if len(self.diagram.shapes) != 0:
            img = self.draw_shapes(img, self.diagram.shapes)
        img.show()

    # funzione sfondo
    def draw_background(self, bg_info: Background) -> Image:
        size = (bg_info.width, bg_info.height)
        bg = Image.new('RGBA', size, bg_info.background_color)
        #bg_info.background_color
        return bg

        # v test
        bg.show()
        # ^ test
    
    def draw_connectors(self, base_img: Image, connectors: List[Connector]) -> Image:
        img = ImageDraw.Draw(base_img)
        for connector in connectors:
            # Connector contiene coordinate e tipo di riga
            #generalization
            #composition
            #realization
            #dependency
            #match connector.tag:
            #    case 'Generalization':
            #        self.draw_generalization(connector, img)
            #    case 'Composition':
            #        pass
            #    case 'Realization':
            #        pass
            #    case 'Dependency':
            #        pass

            for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill='red', width = 0)
        return base_img

    def draw_generalization(self, connector: Connector, img: Image) -> Image:
        for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill='red', width = 0)

    def draw_shapes(self, base_img: Image, shapes: List[Shape]) -> Image:
        img = ImageDraw.Draw(base_img)
        for shape in shapes:
            # aggiungere altre shapes (triangolo, ottagono, esagono, trapezio, rombo)
            match shape.primitive_shape_type:
                case '0':   # disegna rettangolo
                    img.rectangle([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)
                case '2':   # disegna rettangolo arrotondato
                    img.rounded_rectangle([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], radius = 4, fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)
                case '3':   # disegna ellisse
                    img.ellipse([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)
        return base_img

# funzione linea association

# funzione linea generalization

# funzione quadrato