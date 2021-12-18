import xml.etree.ElementTree as ET


from diagram import Diagram
from connectors import Connector
from shape import Shape

#class Parser:
#   def __init__(self, path: str):
#       tree = ET.parse(path)
#       root = tree.getroot()

tree = ET.parse('./assets/class_diagram_3.xml')
root = tree.getroot()

diagram = Diagram(root[2][0].attrib['Width'], root[2][0].attrib['Height'])


# shapes:

for index, element in enumerate(root[2][0][0]):
    model = element.attrib['Model']
    
    diagram.shapes.append(Shape(element.attrib['Name'], element.attrib['Model'], element.attrib['X'], element.attrib['Y'], element.attrib['Background'], element.attrib['Width'], element.attrib['Height']))

    # nel tag model (root[1]), scorre tutti gli elementi finché non trova quello
    # corrispondente alla shape appena istanziata.
    for class_instance in root[1]:
        if class_instance.attrib['Id'] == model:
            # Trovata, scorre tutte le sottoclassi dell'elemento fino a trovare la sottoclasse 'Stereotypes'
            for sub_class in class_instance:
                if sub_class.tag == 'Stereotypes':
                    diagram.shapes[index].matchStereotypes(sub_class)


# connectors:
#   
for element in root[2][0][1]:
    print(element.tag)
    for index, point in enumerate(element):
        if point.tag == 'Points':
            diagram.connectors.append(Connector(element.tag,element[index][0].attrib['X'],element[index][0].attrib['Y'],element[index][1].attrib['X'],element[index][1].attrib['Y'], element.attrib['Background']))
            print("point in posizione " + str(index) + " trovato " + point.tag)
