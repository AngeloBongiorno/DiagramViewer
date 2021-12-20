from typing import List
from xml.etree.ElementTree import Element


class Background:

    def __init__(self, width: int, height: int, background_color: str):
        self.width = width
        self.height = height
        self.background_color = background_color
        #diagram = Diagram(self.root[2][0].attrib['Width'],
        #    self.root[2][0].attrib['Height'], self.root[2][0].attrib['DiagramBackground'])

#test
bg=Background(100,100,'rgb(255,255,255)')

class Shape:

    def __init__(self, name: str, model: str, x: int, y: int, bgcolor: str, width: int, height: int, stereotypes: List[str]) -> None:
        self.name = name
        self.model = model
        self.x = x
        self.y = y
        self.bgcolor = bgcolor
        self.width = width
        self.height = height
        self.stereotypes = stereotypes

    # serve ad aggiungere alla shape eventuale elenco di stereotypes che implementa, questi sono necessari
    # perché mostrati nella rappresentazione grafica del diagramma
    # potrebbe non servire
    def matchStereotypes(self, stypes):
        for stereotype in stypes:
            self.stereotypes.append(stereotype.attrib['Name'])
            # print('questa è una ' + stereotype.attrib['Name'])

#test
sh1=Shape('lollo','1234asdf',5,5,'rgb(1,2,3)',20,20,['Interface','boh'])
sh2=Shape('vecio','1234asdf',5,5,'rgb(1,2,3)',20,20,['boh','qwerty'])

class Connector:

    def __init__(self, tag: str, startx: int, starty: int, endx: int, endy: int, bgcolor: str) -> None:
        self.tag = tag
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.bgcolor = bgcolor

#test
cn1=Connector('lolla',6,6,9,9,'rgb(1,2,3)')
cn2=Connector('vecia',6,6,9,9,'rgb(1,2,3)')

class Diagram:

    def __init__(self, background: Background, shapes: List[Shape], connectors: List[Connector]):
        self.background = background
        self.shapes = shapes
        self.connectors = connectors

    #def add_background(self):
        

    def addConnector(self, element: Element, index: int):
        self.connectors.append(Connector(element.tag,element[index][0].attrib['X'],element[index][0].attrib['Y'],
            element[index][1].attrib['X'],element[index][1].attrib['Y'], element.attrib['Background']))


# serve ad aggiungere alla shape eventuale elenco di stereotypes che implementa, questi sono necessari
    # perché mostrati nella rappresentazione grafica del diagramma
#    def matchStereotypes(self, stypes):
#        for stereotype in stypes:
#            self.stereotypes.append(stereotype.attrib['Name'])
#            # print('questa è una ' + stereotype.attrib['Name'])
#test
sh_list=(sh1,sh2)
cn_list=(cn1,cn2)
dg=Diagram(bg,sh_list,cn_list)
print('hello')
