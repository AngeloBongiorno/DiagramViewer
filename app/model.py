from typing import List, Tuple
from xml.etree.ElementTree import Element


class Background:

    def __init__(self, width: int, height: int, background_color: str):
        self.width = width
        self.height = height
        self.background_color = background_color


class Shape:

    def __init__(self, name: str, model: str, x: int, y: int, bgcolor: str, width: int, height: int,
        primitive_shape_type: int, outline_color: str, outline_weight: float, element_font_name: str, font_size: int, text_color: str):

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
            self.stereotypes.append(stereotype.get('Name'))

    # serve ad aggiungere alla shape eventuale elenco di attributes e operations che implementa, questi sono necessari
    # perché mostrati nella rappresentazione grafica del diagramma
    def match_attributes_operations(self, model_children):
        for model_child in model_children:
            if model_child.tag == 'Attribute':
                attr = Attribute(model_child.get('Name'), model_child.get('Visibility'))
                self.attributes.append(attr)
            if model_child.tag == 'Operation':
                op = Operation(model_child.get('Name'), model_child.get('Visibility'))
                self.operations.append(op)

class Attribute:

    def __init__(self, name: str, visibility: str):
        self.name = name
        match visibility:
            case 'package':
                self.visibility = '~'
            case 'private':
                self.visibility = '-'
            case 'protected':
                self.visibility = '#'
            case 'public':
                self.visibility = '+'
            case _:
                self.visibility = '+'

class Operation:

    def __init__(self, name: str, visibility: str):
        self.name = name + '()'
        match visibility:
            case 'package':
                self.visibility = '~'
            case 'private':
                self.visibility = '-'
            case 'protected':
                self.visibility = '#'
            case 'public':
                self.visibility = '+'
            case _:
                self.visibility = '+'
            

class Connector:

    def __init__(self, tag: str, coordinates: List[Tuple], color: str, weight: float, font_size: int, caption_x: int, caption_y: int, aggregation_kind: str, bg_color: str = 'black'):
        self.tag = tag
        self.coordinates = coordinates
        self.color = color
        self.bg_color = bg_color
        self.weight = weight
        self.font_size = font_size
        self.caption_x = caption_x
        self.caption_y = caption_y
        self.aggregation_kind = aggregation_kind

class Diagram:

    def __init__(self, background: Background, shapes: List[Shape], connectors: List[Connector]):
        self.background = background
        self.shapes = shapes
        self.connectors = connectors
