from generator import Generator
from model import Diagram
from parser import Parser

parser = Parser()
gen = Generator(parser.parse())
gen.draw_diagram()
print('Hello')