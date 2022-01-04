from typing import Any, List
from PIL import Image, ImageDraw, ImageFont
from model import Connector, Shape
import re
import math
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
    
    def draw_connectors(self, base_img: Image, connectors: List[Connector]) -> Image:
        img = ImageDraw.Draw(base_img)
        for connector in connectors:
            # Connector contiene coordinate e tipo di riga
            #generalization
            #composition
            #realization
            #dependency

            match connector.tag:
            #    case 'Generalization':
            #        self.draw_generalization(connector, img)
            #    case 'Composition':
            #        pass
            #    case 'Realization':
            #        self.draw_realization(connector, img)
            #    case 'Dependency':
            #        self.draw_dependency(connector, img)
            #    case 'Association':
            #        self.draw_association(connector, img)
                case _:
                    self.draw_association(connector, img)
             
            #for index, current_coordinates in enumerate(connector.coordinates):
            #    if index + 1 < len(connector.coordinates):
            #        img.line([(current_coordinates[0], current_coordinates[1]),
            #            (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill='red', width = 0)


                    # da integrare
                    #cur_x = 0
                    #cur_y = 0
                    #image_width = 600
                    #for x in range(cur_x, image_width, 4):
                     #   draw.line([(x, cur_y), (x + 2, cur_y)], fill='red', width = 0)
  
        return base_img

    def draw_realization(self, connector: Connector, img: Image) -> Image:
        for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    self.dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1])
                    #aggiungere freccia blu alla fine

    def draw_dependency(self, connector: Connector, img: Image) -> Image:
        for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    self.dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1])
                    #aggiungere freccia non chiusa


    def draw_association(self, connector: Connector, img: Image) -> Image:
        for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill='red', width = 0)

    def draw_generalization(self, connector: Connector, img: Image) -> Image:
        for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill='red', width = 0)


    def dashed_line(self, base_img: ImageDraw, x0, y0, x1, y1, dashlen=2, ratio=2): 
        dx=x1-x0 # delta x
        dy=y1-y0 # delta y
        # check whether we can avoid sqrt
        if dy==0:
            len=dx
        elif dx==0:
            len=dy
        else:
            len=math.sqrt(dx*dx+dy*dy) # length of line
        xa=dx/len # x add for 1px line length
        ya=dy/len # y add for 1px line length
        step=dashlen*ratio # step to the next dash
        a0=0
        while a0<len:
            a1=a0+dashlen
            #if a1>len:
            #    a1=len
            base_img.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = 'black', width = 1)
            a0+=step


    # da implementare
    #def rgba_2_rgb(self, rgba_string: str) -> str:
    #    pattern = re.compile('^(rgba)')
    #    if pattern.search(rgba_string):
    #        rgb_string = re.sub(   , ')', rgba_string)

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
            if shape.name != '':
                font = ImageFont.truetype("./assets/fonts/arial.ttf",  shape.font_size)
                w, h = img.textsize(shape.name)
                img.text([shape.x+ (shape.width-w)/2, shape.y], shape.name, fill=shape.text_color, font=font)
                #self.rgba_2_rgb(shape.outline_color)
                img.line([shape.x, shape.y+h, shape.x+shape.width, shape.y+h], fill = shape.outline_color )           
        return base_img
