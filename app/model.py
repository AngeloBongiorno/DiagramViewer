from typing import List
from xml.etree.ElementTree import Element
from app.connector import Connector
from app.shape import Shape


class Background:

    def __init__(self, width: int, height: int, background_color: str):
        self.width = width
        self.height = height
        self.background_color = background_color
        #diagram = Diagram(self.root[2][0].attrib['Width'],
        #    self.root[2][0].attrib['Height'], self.root[2][0].attrib['DiagramBackground'])

class Shape:

    def __init__(self, name: str, model: str, x: int, y: int, bgcolor: str, width: int, height: int) -> None:
        self.name = name
        self.model = model
        self.x = x
        self.y = y
        self.bgcolor = bgcolor
        self.width = width
        self.height = height
        self.stereotypes = []

    # serve ad aggiungere alla shape eventuale elenco di stereotypes che implementa, questi sono necessari
    # perché mostrati nella rappresentazione grafica del diagramma
    # potrebbe non servire
    def matchStereotypes(self, stypes):
        for stereotype in stypes:
            self.stereotypes.append(stereotype.attrib['Name'])
            # print('questa è una ' + stereotype.attrib['Name'])

class Connector:

    def __init__(self, tag: str, startx: int, starty: int, endx: int, endy: int, bgcolor: str) -> None:
        self.tag = tag
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.bgcolor = bgcolor

class Diagram:

    def __init__(self, background: Background, shapes: List[Shape], connectors: List[Connector]):
        self.background = background
        self.shapes = []
        self.connectors = []

    def addConnector(self, element: Element, index: int):
        self.connectors.append(Connector(element.tag,element[index][0].attrib['X'],element[index][0].attrib['Y'],
            element[index][1].attrib['X'],element[index][1].attrib['Y'], element.attrib['Background']))
