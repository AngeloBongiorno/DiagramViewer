import xml.etree.ElementTree as ET


from diagram import Diagram
from connectors import Connector
from shape import Shape

tree = ET.parse('./assets/project.xml')
root = tree.getroot()

diagram = Diagram(root[2][0].attrib['Width'], root[2][0].attrib['Height'])

# shapes
for element in root[2][0][0]:
    diagram.shapes.append(Shape(element.attrib['Name'], element.attrib['X'], element.attrib['Y'], element.attrib['Background'], element.attrib['Width'], element.attrib['Height']))

# connectors    
for element in root[2][0][1]:
    print(element.tag)
    for index, point in enumerate(element):
        if point.tag == 'Points':
            diagram.connectors.append(Connector(element.tag,element[index][0].attrib['X'],element[index][0].attrib['Y'],element[index][1].attrib['X'],element[index][1].attrib['Y'], element.attrib['Background']))
            print("point in posizione " + str(index) + " trovato " + point.tag)
