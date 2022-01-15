from typing import List, Tuple
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
        pass

        
    # il metodo parse() è da parametrizzare con l'indirizzo del file xml che invia l'utente
    def parse(self) -> Diagram: 
        #al posto dells stringa './assets/class_diagram_3.xml' va inserito l'indirizzo del file fornito dell'utente
        self.tree = ET.parse('./assets/class_diagram_3.xml')
        self.root = self.tree.getroot()
        self.shapes = self._make_shapes()
        self.connectors = self._make_connectors()
        self.background = self._make_background()
        return Diagram(self.background, self.shapes, self.connectors) 


    # definisce dimensioni dell'immagine in base alla posizione delle
    # shape che si trovano agli estremi del diagramma

    def _compute_bg_borders(self) -> Tuple:

        xmin = self.shapes[0].x
        xmax = self.shapes[0].x + self.shapes[0].width
        ymin = self.shapes[0].y
        ymax = self.shapes[0].y + self.shapes[0].height

        for shape in self.shapes:
            if shape.x < xmin:
                xmin = shape.x
            if shape.x + shape.width > xmax:
                xmax = shape.x + shape.width
            if shape.y < ymin:
                ymin = shape.y
            if shape.y + shape.height > ymax:
                ymax = shape.y + shape.height

        width = xmax + xmin
        height = ymax + ymin
        return width, height

    
    # crea oggetto Background
    def _make_background(self) -> Background:
        dimensioni = self._compute_bg_borders()
        bg_color = self.root[2][0].get(XA.DIAGRAMBACKGROUND)
        bg = Background(int(dimensioni[0]), int(dimensioni[1]), bg_color)
        return bg
    

    # colore e spessore della linea
    def _parse_line(self, line_tag: ET.Element) -> Tuple[str, float]:
        line_color = line_tag.get(XA.COLOR)
        line_weight = line_tag.get(XA.WEIGHT)
        return line_color, line_weight


    # nome del font, dimensione e colore del testo
    def _parse_element_font(self, element_font_tag: ET.Element) -> Tuple[str, int, str]:
        element_font_name = element_font_tag.get(XA.NAME)
        element_font_size = element_font_tag.get(XA.SIZE)
        element_font_color = element_font_tag.get(XA.COLOR)
        return element_font_name, element_font_size, element_font_color



    # crea una lista di shapes
    def _make_shapes(self) -> List[Shape]:
        shape_list = []
        if self.root[2][0].find(XT.SHAPES):
            for index, element in enumerate(self.root[2][0].find(XT.SHAPES)):
                outline = self._parse_line(element.find(XT.LINE))
                element_font = self._parse_element_font(element.find(XT.ELEMENTFONT))
                shape_list.append(Shape(element.get(XA.NAME), element.get(XA.MODEL), float(element.get(XA.X)), float(element.get(XA.Y)),
                    element.get(XA.BACKGROUND), float(element.get(XA.WIDTH)), float(element.get(XA.HEIGHT)),
                    element.get(XA.PRIMITIVESHAPETYPE), outline[0], int(float(outline[1])), element_font[0], int(element_font[1]), element_font[2]))

                model = element.get(XA.MODEL)

                for class_instance in self.root.findall("./Models/*[@Id='"+model+"']"):
                        # Trovata, scorre tutte le sottoclassi dell'elemento fino a trovare la sottoclasse 'Stereotypes'
                        for sub_class in class_instance:
                            if sub_class.tag == XT.STEREOTYPES:
                                shape_list[index].match_stereotypes(sub_class)
                            if sub_class.tag == XT.MODELCHILDREN:
                                shape_list[index].match_attributes_operations(sub_class)
        return shape_list



    # crea una lista di connectors
    def _make_connectors(self) -> List[Connector]:
        connector_list = []
        if self.root[2][0].find(XT.CONNECTORS):
            for element in self.root.findall("./Diagrams/ClassDiagram/Connectors/*"):
                for index, connector_tag in enumerate(element):
                    match connector_tag.tag:
                        case XT.LINE:
                            color_and_weight = self._parse_line(connector_tag)
                        case XT.ELEMENTFONT:
                            font_size = connector_tag.get(XA.SIZE)
                        case XT.CAPTION:
                            if connector_tag.get(XA.VISIBLE):
                                caption_x = connector_tag.get(XA.X)
                                caption_y = connector_tag.get(XA.Y)
                        case XT.POINTS:
                            connector_coordinates = []
                            for n, _ in enumerate(connector_tag):
                                connector_coordinates.append((float(element[index][n].get(XA.X)), float(element[index][n].get(XA.Y))))

                aggregation_kind = 'None'

                if element.tag == 'Association':
                    model = element.get(XA.MODEL)

                    for association in self.root.findall("./Models//Association[@Id='"+model+"']"):    
                        if association.get(XA.ID) == model:
                            for x in association.find(XT.FROMEND):
                                aggregation_kind = x.get(XA.AGGREGATIONKIND)

                connector_list.append(Connector(element.tag, connector_coordinates, color_and_weight[0],
                    int(float(color_and_weight[1])), int(float(font_size)), int(float(caption_x)), int(float(caption_y)), aggregation_kind, element.get(XA.BACKGROUND)))

        return connector_list
