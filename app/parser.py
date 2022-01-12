from typing import List, Tuple
import typing
import xml.etree.ElementTree as ET
from model import Background

from model import Connector, Shape, Diagram

class XT:
    """XML tags namespace."""
    ASSOCIATION = 'Association'
    ATTRIBUTE = 'Attribute'
    CAPTION = 'Caption'
    CLASS = 'Class'
    CONNECTORS = 'Connectors'
    ELEMENTFONT = 'ElementFont'
    FROMEND = 'FromEnd'
    LINE = 'Line'
    MODELCHILDREN = 'ModelChildren'
    MODELRELATIONSHIPCONTAINER = 'ModelRelationshipContainer'
    MODELS = 'Models'
    OPERATION = 'Operation'
    POINTS = 'Points'
    SHAPES = 'Shapes'
    STEREOTYPES = 'Stereotypes'

class XA:
    """XML attributes namespace."""
    AGGREGATIONKIND = 'AggregationKind'
    BACKGROUND = 'Background'
    COLOR = 'Color'
    DIAGRAMBACKGROUND = 'DiagramBackground'
    HEIGHT = 'Height'
    ID = 'Id'
    MODEL = 'Model'
    NAME = 'Name'
    PRIMITIVESHAPETYPE = 'PrimitiveShapeType'
    SIZE = 'Size'
    VISIBLE = 'Visible'
    WEIGHT = 'Weight'
    WIDTH = 'Width'
    X = 'X'
    Y = 'Y'
    

class Parser:

    def __init__(self):
        #self.tree = ET.parse(path)
        #self.tree = ET.parse('./assets/class_diagram_3.xml') # per prova
        #self.root = self.tree.getroot()
        pass

    def parse(self) -> Diagram: # nell'argomento andrebbe inserito anche il path
        self.tree = ET.parse('./assets/class_diagram_3.xml')
        self.root = self.tree.getroot()
        self.background = self._make_background()
        self.shapes = self._make_shapes()
        self.connectors = self._make_connectors()
        return Diagram(self.background, self.shapes, self.connectors) 


    def _parse_background(self) -> typing.Tuple:
        self.bg_width = int(self.root[2][0].get(XA.WIDTH))
        self.bg_height = int(self.root[2][0].get(XA.HEIGHT))
        self.bg_color = self.root[2][0].get(XA.DIAGRAMBACKGROUND)
        return self.bg_width, self.bg_height, self.bg_color

    def _make_background(self) -> Background:
        attributes = self._parse_background()
        self.bg = Background(attributes[0],attributes[1],attributes[2])
        return self.bg
    
    # shapes:
    def _parse_line(self, line_tag: ET.Element) -> Tuple[str, float]:
        self.line_color = line_tag.get(XA.COLOR)
        self.line_weight = line_tag.get(XA.WEIGHT)
        return self.line_color, self.line_weight

    def _parse_element_font(self, element_font_tag: ET.Element) -> Tuple[str, int, str]:
        self.element_font_name = element_font_tag.get(XA.NAME)
        self.element_font_size = element_font_tag.get(XA.SIZE)
        self.element_font_color = element_font_tag.get(XA.COLOR)
        return self.element_font_name, self.element_font_size, self.element_font_color



    def _make_shapes(self) -> List[Shape]:
        _shape_list = []
        if self.root[2][0].find(XT.SHAPES):
            for index, element in enumerate(self.root[2][0].find(XT.SHAPES)):
                _outline = self._parse_line(element.find(XT.LINE))
                _element_font = self._parse_element_font(element.find(XT.ELEMENTFONT))
                _shape_list.append(Shape(element.get(XA.NAME), element.get(XA.MODEL), float(element.get(XA.X)), float(element.get(XA.Y)),
                    element.get(XA.BACKGROUND), float(element.get(XA.WIDTH)), float(element.get(XA.HEIGHT)),
                    element.get(XA.PRIMITIVESHAPETYPE), _outline[0], int(float(_outline[1])), _element_font[0], int(_element_font[1]), _element_font[2]))

                model = element.get(XA.MODEL)
                # nel tag 'Model' (root[1]), scorre tutti gli elementi finché non trova quello
                # corrispondente alla shape appena istanziata.
                for class_instance in self.root[1]:
                    if class_instance.get(XA.ID) == model:
                        # Trovata, scorre tutte le sottoclassi dell'elemento fino a trovare la sottoclasse 'Stereotypes'
                        for sub_class in class_instance:
                            if sub_class.tag == XT.STEREOTYPES:
                                _shape_list[index].match_stereotypes(sub_class)
                            if sub_class.tag == XT.MODELCHILDREN:
                                _shape_list[index].match_attributes_operations(sub_class)
        return _shape_list



        # connectors:
    def _make_connectors(self) -> List[Connector]:
        _connector_list = []
        if self.root[2][0].find(XT.CONNECTORS):
            for element in self.root[2][0].find(XT.CONNECTORS):
                for index, connector_tag in enumerate(element):
                    match connector_tag.tag:
                        case XT.LINE:
                            _color_and_weight = self._parse_line(connector_tag)
                        case XT.ELEMENTFONT:
                            _font_size = connector_tag.get(XA.SIZE)
                        case XT.CAPTION:
                            if connector_tag.get(XA.VISIBLE):
                                _caption_x = connector_tag.get(XA.X)
                                _caption_y = connector_tag.get(XA.Y)
                        case XT.POINTS:
                            _connector_coordinates = []
                            for n, _ in enumerate(connector_tag):
                                _connector_coordinates.append((float(element[index][n].get(XA.X)), float(element[index][n].get(XA.Y))))

                #    if connector_tag.tag == XT.LINE:
                #        _color_and_weight = self._parse_line(connector_tag)
                #    if connector_tag.tag == XT.ELEMENTFONT:
                #        _font_size = connector_tag.get(XA.SIZE)
                #    if connector_tag.tag == XT.CAPTION:
                #        if connector_tag.get(XA.VISIBLE):
                #            _caption_x = connector_tag.get(XA.X)
                #            _caption_y = connector_tag.get(XA.Y)
                #    if connector_tag.tag == XT.POINTS:
                #        _connector_coordinates = []
                #        for n, _ in enumerate(connector_tag):
                #            _connector_coordinates.append((float(element[index][n].get(XA.X)), float(element[index][n].get(XA.Y))))


                _aggregation_kind = 'None'

                if element.tag == 'Association':
                    _model = element.get(XA.MODEL)

                    for association in self.root.findall("./Models/ModelRelationshipContainer/ModelChildren//Association"):    
                        if association.get(XA.ID) == _model:
                            for x in association.find(XT.FROMEND):
                                _aggregation_kind = x.get(XA.AGGREGATIONKIND)

                _connector_list.append(Connector(element.tag, _connector_coordinates, _color_and_weight[0], int(float(_color_and_weight[1])), int(float( _font_size)), int(float(_caption_x)), int(float(_caption_y)), _aggregation_kind, element.get(XA.BACKGROUND)))

        return _connector_list
