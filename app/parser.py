from typing import List, Tuple
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
    LINE = 'Line'
    SHAPES = 'Shapes'
    CONNECTORS = 'Connectors'
    ELEMENTFONT = 'ElementFont'

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
    COLOR = 'Color'
    WEIGHT = 'Weight'
    PRIMITIVESHAPETYPE = 'PrimitiveShapeType'
    SIZE = 'Size'

class Parser:

    def __init__(self):
        #self.tree = ET.parse(path)
        #self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        #self.root = self.tree.getroot()
        pass

    def parse(self) -> Diagram: # nell'argomento andrebbe inserito anche il path
        #self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        self.tree = ET.parse('./assets/class_diagram_3.xml')
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
    def parse_outline(self, line_tag: ET.Element) -> Tuple[str, float]:
        self.outline_color = line_tag.attrib[XA.COLOR]
        self.outline_weight = line_tag.attrib[XA.WEIGHT]
        return self.outline_color, self.outline_weight

    def parse_element_font(self, element_font_tag: ET.Element) -> Tuple[str, int, str]:
        self.element_font_name = element_font_tag.attrib[XA.NAME]
        self.element_font_size = element_font_tag.attrib[XA.SIZE]
        self.element_font_color = element_font_tag.attrib[XA.COLOR]
        return self.element_font_name, self.element_font_size, self.element_font_color



    def make_shapes(self) -> List[Shape]:
        self.shape_list = []
        if self.root[2][0].find(XT.SHAPES) != None:
            for index, element in enumerate(self.root[2][0].find(XT.SHAPES)):
                _outline = self.parse_outline(element.find(XT.LINE))
                _element_font = self.parse_element_font(element.find(XT.ELEMENTFONT))
                self.shape_list.append(Shape(element.attrib[XA.NAME], element.attrib[XA.MODEL], float(element.attrib[XA.X]), float(element.attrib[XA.Y]),
                    element.attrib[XA.BACKGROUND], float(element.attrib[XA.WIDTH]), float(element.attrib[XA.HEIGHT]),
                    element.attrib[XA.PRIMITIVESHAPETYPE], _outline[0], int(float(_outline[1])), _element_font[0], int(_element_font[1]), _element_font[2]))

                model = element.attrib[XA.MODEL]
                # nel tag 'Model' (root[1]), scorre tutti gli elementi finché non trova quello
                # corrispondente alla shape appena istanziata.
                for class_instance in self.root[1]:
                    if class_instance.attrib[XA.ID] == model:
                        # Trovata, scorre tutte le sottoclassi dell'elemento fino a trovare la sottoclasse 'Stereotypes'
                        for sub_class in class_instance:
                            if sub_class.tag == XT.STEREOTYPES:
                                self.shape_list[index].match_stereotypes(sub_class)
                            if sub_class.tag == XT.MODELCHILDREN:
                                self.shape_list[index].match_attributes_operations(sub_class)
        return self.shape_list



        # connectors:
    def make_connectors(self) -> List[Connector]:
        self.connector_list = []
        if self.root[2][0].find(XT.CONNECTORS) != None:
            for element in self.root[2][0].find(XT.CONNECTORS):
                for index, line in enumerate(element):
                    if line.tag == XT.POINTS:
                        line_coordinates = []
                        for n, _ in enumerate(line):
                            line_coordinates.append((float(element[index][n].attrib[XA.X]), float(element[index][n].attrib[XA.Y])))
                        self.connector_list.append(Connector(element.tag, line_coordinates, element.attrib[XA.BACKGROUND]))
        return self.connector_list
