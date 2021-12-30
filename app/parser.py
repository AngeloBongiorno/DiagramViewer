from typing import List
import typing
import xml.etree.ElementTree as ET
from model import Background

from model import Connector, Shape, Diagram

class XT:
    """XML tags namespace."""
    CLASS = 'Class'
    POINTS = 'Points'
    STEREOTYPES = 'Stereotypes'
    MODELCHILDREN = 'ModelChildren'
    ATTRIBUTE = 'Attribute'
    OPERATION = 'Operation'

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
    ID = 'Id'


class Parser:

    def __init__(self):
        #self.tree = ET.parse(path)
        #self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        #self.root = self.tree.getroot()
        pass

    def parse(self) -> Diagram: # nell'argomento andrebbe inserito anche il path
        self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        self.root = self.tree.getroot()
        self.background = self.make_background()
        self.shapes = self.make_shapes()
        self.connectors = self.make_connectors()
        return Diagram(self.background, self.shapes, self.connectors)
        #self.parsed_connectors = 


    def parse_background(self) -> typing.Tuple:
        self.bg_width = int(self.root[2][0].attrib[XA.WIDTH])
        self.bg_height = int(self.root[2][0].attrib[XA.HEIGHT])
        self.bg_color = self.root[2][0].attrib[XA.DIAGRAMBACKGROUND]
        return self.bg_width, self.bg_height, self.bg_color

    def make_background(self) -> Background:
        attributes = self.parse_background()
        self.bg = Background(attributes[0],attributes[1],attributes[2])
        return self.bg
    
    # shapes:

    def make_shapes(self) -> List[Shape]:
        self.shape_list = []
        for index, element in enumerate(self.root[2][0][0]):
            
            self.shape_list.append(Shape(element.attrib[XA.NAME], element.attrib[XA.MODEL], float(element.attrib[XA.X]), float(element.attrib[XA.Y]),
                element.attrib[XA.BACKGROUND], float(element.attrib[XA.WIDTH]), float(element.attrib[XA.HEIGHT])))

            model = element.attrib[XA.MODEL]
            # nel tag model (root[1]), scorre tutti gli elementi finché non trova quello
            # corrispondente alla shape appena istanziata.
            for class_instance in self.root[1]:
                if class_instance.attrib[XA.ID] == model:
                    # Trovata, scorre tutte le sottoclassi dell'elemento fino a trovare la sottoclasse 'Stereotypes'
                    for sub_class in class_instance:
                        if sub_class.tag == XT.STEREOTYPES:
                            self.shape_list[index].match_stereotypes(sub_class)
                        if sub_class.tag == XT.MODELCHILDREN:
                            self.shape_list[index].match_attributes_operations(sub_class)
                            print('ciao')
        return self.shape_list



        # connectors:
    def make_connectors(self) -> List[Connector]:
        self.connector_list = []   
        for element in self.root[2][0][1]:
            #print(element.tag)
            for index, line in enumerate(element):
                if line.tag == XT.POINTS:
                    line_coordinates = []
                    for n, _ in enumerate(line):
                        line_coordinates.append((float(element[index][n].attrib['X']), float(element[index][n].attrib['Y'])))
                    self.connector_list.append(Connector(element.tag, line_coordinates, element.attrib['Background']))
                    
                        
                    #self.connector_list.append(Connector(element.tag,float(element[index][0].attrib['X']),float(element[index][0].attrib['Y']),
                    #    float(element[index][1].attrib['X']),float(element[index][1].attrib['Y']), element.attrib['Background']))
                    #print("point in posizione " + str(index) + " trovato " + point.tag)
        return self.connector_list




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
#CiaoAntonella




    




