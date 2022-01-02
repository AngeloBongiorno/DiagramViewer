from typing import List, Tuple
from xml.etree.ElementTree import Element


class Background:

    def __init__(self, width: int, height: int, background_color: str):
        self.width = width
        self.height = height
        self.background_color = background_color
        #diagram = Diagram(self.root[2][0].attrib['Width'],
        #    self.root[2][0].attrib['Height'], self.root[2][0].attrib['DiagramBackground'])

#test
#bg=Background(100,100,'rgb(255,255,255)')

class Shape:

    def __init__(self, name: str, model: str, x: int, y: int, bgcolor: str, width: int, height: int,
        primitive_shape_type: int, outline_color: str, outline_weight: float, element_font_name: str, font_size: int, text_color: str) -> None:

        self.name = name
        self.model = model
        self.x = x
        self.y = y
        self.bgcolor = bgcolor
        self.width = width
        self.height = height
        self.primitive_shape_type = primitive_shape_type
        self.outline_color = outline_color
        self.outline_weight = outline_weight
        self.element_font_name = element_font_name
        self.font_size = font_size
        self.text_color = text_color
        self.operations = []
        self.attributes = []
        self.stereotypes = []

    # serve ad aggiungere alla shape eventuale elenco di stereotypes che implementa, questi sono necessari
    # perché mostrati nella rappresentazione grafica del diagramma
    def match_stereotypes(self, stypes):
        for stereotype in stypes:
            self.stereotypes.append(stereotype.attrib['Name'])

    # serve ad aggiungere alla shape eventuale elenco di attributes e operations che implementa, questi sono necessari
    # perché mostrati nella rappresentazione grafica del diagramma
    def match_attributes_operations(self, model_children):
        for model_child in model_children:
            if model_child.tag == 'Attribute':
                self.attributes.append(model_child.attrib['Name'])
            if model_child.tag == 'Operation':
                self.operations.append(model_child.attrib['Name'])

    

class Connector:

    def __init__(self, tag: str, coordinates: List[Tuple], bgcolor: str) -> None:
        self.tag = tag
        self.coordinates = coordinates
        self.bgcolor = bgcolor

class Diagram:

    def __init__(self, background: Background, shapes: List[Shape], connectors: List[Connector]):
        self.background = background
        self.shapes = shapes
        self.connectors = connectors


