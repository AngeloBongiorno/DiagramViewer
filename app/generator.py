from typing import Any, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from model import Connector, Shape
import re
import numpy as np
import math
from model import Background, Diagram

class Generator:

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram
        pass

    def draw_diagram(self):
        
        img = self.draw_background(self.diagram.background)
        if len(self.diagram.shapes) != 0:
            img = self.draw_shapes(img, self.diagram.shapes)
        if len(self.diagram.connectors) != 0:
            img = self.draw_connectors(img, self.diagram.connectors)
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

            match connector.tag:
                case 'Generalization':
                    self.draw_generalization(connector, img)
                case 'Composition':
                    self.draw_composition(connector, img)
                case 'Realization':
                    self.draw_realization(connector, img)
                case 'Dependency':
                    self.draw_dependency(connector, img)
                case 'Association':
                    self.draw_association(connector, img)
                case 'Aggregation':
                    self.draw_aggregation(connector, img)
                case _:
                    self.draw_association(connector, img)
             
            #for index, current_coordinates in enumerate(connector.coordinates):
            #    if index + 1 < len(connector.coordinates):

            #        self.dashed_line(img, current_coordinates[0], current_coordinates[1],
            #        connector.coordinates[index+1][0], connector.coordinates[index+1][1])
            #   oppure
            #        img.line([(current_coordinates[0], current_coordinates[1]),
            #            (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill='red', width = 0)
  
        return base_img

    def draw_realization(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index!= 0:
                    self.dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                else:
                    self.dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                    #angle = self.angle_between((coordinates[0],coordinates[1]), (connector.coordinates[index+1][0],connector.coordinates[index+1][1]))

                    self.draw_triangle(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'red', connector.color)
                    #img.regular_polygon((coordinates[0], coordinates[1], 8), 3, rotation=angle, fill='red', outline='Black')
                    # ^ questo triangolo è storto perché il metodo angle_between va fixato


    # TODO implementare correttamente

    def angle_between(self, a: Tuple, b: Tuple):
        return np.rad2deg(np.arctan2(abs(b[1]-a[1]),b[0]-a[0]))


    def draw_dependency(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
                if index + 1 < len(connector.coordinates):
                    self.dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                    #aggiungere freccia non chiusa

    def draw_composition(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index != 0:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                else:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                    self.draw_rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'black', connector.color)


    def draw_association(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index != 0:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                else:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                    if connector.aggregation_kind == 'Shared':
                        self.draw_rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'white', connector.color)
                    elif connector.aggregation_kind == 'Composited':
                        self.draw_rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'black', connector.color)
                    
                

    def draw_aggregation(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index != 0:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                else:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                    self.draw_rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'white', connector.color)

    def draw_generalization(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index != 0:
                    img.line([(coordinates[0], coordinates[1]),
                            (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                else:
                    img.line([(coordinates[0], coordinates[1]),
                        (connector.coordinates[index+1][0], connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                    #angle = self.angle_between((coordinates[0],coordinates[1]), (connector.coordinates[index+1][0],connector.coordinates[index+1][1]))
                    
                    self.draw_triangle(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'white', connector.color)
                    #img.regular_polygon((coordinates[0], coordinates[1], 8), 3, rotation=angle, fill='white', outline=connector.color)
                    # ^ questo triangolo è storto perché il metodo angle_between va fixato

    def draw_triangle(self,  img: ImageDraw, ptA: Tuple, ptB: Tuple, color: str, outline: str):
        #coordinate punti
        x0, y0 = ptA
        x1, y1 = ptB

        #coordinate dell'intersezione linea - base del triangolo
        xb = 0.70*(x1-x0)+x0
        yb = 0.70*(y1-y0)+y0

        #controlla se la linea è verticale o orizzontale
        if x0==x1:
           vtx0 = (xb-5, yb)
           vtx1 = (xb+5, yb)
        elif y0==y1:
           vtx0 = (xb, yb+5)
           vtx1 = (xb, yb-5)
        else:
           alpha = math.atan2(y1-y0,x1-x0) - 90*math.pi/180
           a = 6*math.cos(alpha)
           b = 6*math.sin(alpha)
           vtx0 = (xb+a, yb+b)
           vtx1 = (xb-a, yb-b)

        img.polygon([vtx0, vtx1, ptB], fill=color, outline=outline)

    def draw_rhombus(self,  img: ImageDraw, ptA: Tuple, ptB: Tuple, color: str, outline: str):

        #coordinate punti inizio ultima linea
        x0, y0 = ptA
        #coorinate punta freccia
        x1, y1 = ptB

        #coordinate dell'intersezione linea - base del triangolo
        xb = 0.80*(x1-x0)+x0
        yb = 0.80*(y1-y0)+y0

        #controlla se la linea è verticale o orizzontale
        if x0==x1:
           vtx0 = (xb-5, yb)
           vtx1 = (xb+5, yb)
        elif y0==y1:
           vtx0 = (xb, yb+5)
           vtx1 = (xb, yb-5)
        else:
           alpha = math.atan2(y1-y0,x1-x0) - 90*math.pi/180
           a = 6*math.cos(alpha)
           b = 6*math.sin(alpha)
           vtx0 = (xb+a, yb+b)
           vtx1 = (xb-a, yb-b)

        deltax = xb-x1
        deltay = yb-y1

        rx = xb + deltax
        ry = yb + deltay
        r = (rx, ry)

        img.polygon([vtx0, r, vtx1, ptB], fill=color, outline=outline)



    def dashed_line(self, base_img: ImageDraw, x0, y0, x1, y1, color='black', dashlen=5, ratio=2): 
        dx=x1-x0 # delta x
        dy=y1-y0 # delta y
        # calcolo lunghezza segmento
        if dy==0:
            len=abs(dx)
        elif dx==0:
            len=abs(dy)
        else:
            len=math.sqrt(dx*dx+dy*dy)
        xa=dx/len # x add for 1px line length
        ya=dy/len # y add for 1px line length
        step=dashlen*ratio # lunghezza spazio tra trattini
        a0=0
        while a0<len:
            a1=a0+dashlen
            if a1>len:
                a1=len
            base_img.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = color, width = 1)
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
                case _:
                    img.rectangle([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)

            font = ImageFont.truetype("./assets/fonts/arial.ttf",  shape.font_size)

            w, h = img.textsize(shape.name)
            img.text([shape.x+ (shape.width-w)/2, shape.y], shape.name, fill=shape.text_color, font=font)
            #self.rgba_2_rgb(shape.outline_color)
            img.line([shape.x, shape.y+h, shape.x+shape.width, shape.y+h], fill = shape.outline_color)

            if shape.stereotypes:
                for stereotype in shape.stereotypes:
                    w, h = img.textsize(stereotype)
                    img.text([shape.x+ (shape.width-w)/2, shape.y-h], "<<"+stereotype+">>", fill=shape.text_color, font=font)

            a=0

            if shape.attributes:
                for attribute in shape.attributes:
                    w, h = img.textsize(attribute.name)
                    img.text([shape.x, shape.y+h+a], attribute.visibility+' '+attribute.name, fill=shape.text_color, font=font, anchor='lt')
                    a+=h+1
                img.line([shape.x, shape.y+h+a, shape.x+shape.width, shape.y+h+a], fill = shape.outline_color)

            if shape.operations:
                for operation in shape.operations:
                    w, h = img.textsize(operation.name)
                    img.text([shape.x, shape.y+h+a], operation.visibility+' '+operation.name, fill=shape.text_color, font=font, anchor='lt')
                    a+=h+1

        return base_img
