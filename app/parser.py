import typing
import xml.etree.ElementTree as ET
from model import Background

from model import Connector, Shape, Diagram

class XT:
    """XML tags namespace."""
    CLASS = 'Class'
    POINTS = 'Points'

class XA:
    """XML attributes namespace."""
    NAME = 'Name'
    MODEL = 'Model'
    X = 'X'
    Y = 'Y'
    WIDTH = 'Width'
    HEIGHT = 'Height'
    DIAGRAMBACKGROUND = 'DiagramBackground'
    BACKGROUND = 'Background'


class Parser:

    def __init__(self):
        #self.tree = ET.parse(path)
        #self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        #self.root = self.tree.getroot()
        pass

    def parse(self): # nell'argomento andrebbe inserito anche il path
        self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        self.root = self.tree.getroot()
        self.background = self.make_background()
        #self.parsed_connectors = 


    def parse_background(self) -> typing.Tuple:
        self.bg_width = self.root[2][0].attrib[XA.WIDTH]
        self.bg_height = self.root[2][0].attrib[XA.HEIGHT]
        self.bg_color = self.root[2][0].attrib[XA.DIAGRAMBACKGROUND]
        return self.bg_width, self.bg_height, self.bg_color

    def make_background(self) -> Background:
        attributes = self.parse_background()
        self.bg = Background(attributes[0],attributes[1],attributes[2])
        return self.bg



    

    # shapes:
    def findShapes(self, diagram: Diagram):
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
    def find_connector():    #   
        for element in self.root[2][0][1]:
            #print(element.tag)
            for index, point in enumerate(element):
                if point.tag == 'Points':
                    #diagram.connectors.append(Connector(element.tag,element[index][0].attrib['X'],element[index][0].attrib['Y'],element[index][1].attrib['X'],element[index][1].attrib['Y'], element.attrib['Background']))
                    diagram.addConnector(element,index)
                    #print("point in posizione " + str(index) + " trovato " + point.tag)

    #def make_shapes(self):
    #    for shape in self.root[2][0][0].findall(XT.CLASS):
    #        self.name = shape.attrib[XA.NAME]
    #        self.model = shape.attrib[XA.MODEL]
    #        self.x = shape.attrib[XA.X]
    #        self.y = shape.attrib[XA.Y]
    #        self.bgcolor = shape.attrib[XA.BACKGROUND]
    #        self.width = shape.attrib[XA.WIDTH]
    #        self.height = shape.attrib[XA.HEIGHT]
    #        for shape_data in self.root[1]:



    #def make_connectors(self):
        
                        




    

    #def make_diagram(self, bg: Background) -> Diagram:
    #    diagram = Diagram(bg,)
     #   return diagram


#test




    




