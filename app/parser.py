from typing import List
import xml.etree.ElementTree as ET



from connector import Connector
from shape import Shape
from diagram import Diagram
# capire come fare import da directory sorella

class XT:
    """XML tags namespace."""
    CLASS = 'Class'
    POINTS = 'Points'

class XA:
    """XML attributes namespace."""


class Parser:
    def __init__(self):
        self._diagram = Diagram()
        #self.tree = ET.parse(path)
        #self.tree = ET.parse('./assets/class_diagram_3.xml')
        #self.root = self.tree.getroot()
        #self.diagram = self.makeDiagram()

    def makeDiagram(self) -> Diagram:
        diagram = Diagram(self.root[2][0].attrib['Width'], self.root[2][0].attrib['Height'], self.root[2][0].attrib['DiagramBackground'])
        print(diagram)
        return diagram



    def parse_shapes(self):
        self.root[2][0][0].findall(XT.CLASS)


# shapes:
    def findShapes(self, diagram: Diagram) -> List:
        for index, element in enumerate(self.root[2][0][0]):
            
            
            diagram.shapes.append(Shape(element.attrib['Name'], element.attrib['Model'], element.attrib['X'], element.attrib['Y'],
                element.attrib['Background'], element.attrib['Width'], element.attrib['Height']))

            model = element.attrib['Model']
            # nel tag model (root[1]), scorre tutti gli elementi finché non trova quello
            # corrispondente alla shape appena istanziata.
            for class_instance in self.root[1]:
                if class_instance.attrib['Id'] == model:
                    # Trovata, scorre tutte le sottoclassi dell'elemento fino a trovare la sottoclasse 'Stereotypes'
                    for sub_class in class_instance:
                        if sub_class.tag == 'Stereotypes':
                            diagram.shapes[index].matchStereotypes(sub_class)


        # connectors:
        #   
    for element in self.root[2][0][1]:
        #print(element.tag)
        for index, point in enumerate(element):
            if point.tag == 'Points':
                #diagram.connectors.append(Connector(element.tag,element[index][0].attrib['X'],element[index][0].attrib['Y'],element[index][1].attrib['X'],element[index][1].attrib['Y'], element.attrib['Background']))
                diagram.addConnector(element,index)
                #print("point in posizione " + str(index) + " trovato " + point.tag)

