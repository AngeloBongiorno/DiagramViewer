from typing import List


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
    def matchStereotypes(self, stypes):
        for stereotype in stypes:
            self.stereotypes.append(stereotype.attrib['Name'])
            # print('questa è una ' + stereotype.attrib['Name'])