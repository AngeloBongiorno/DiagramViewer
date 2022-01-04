from PIL import Image, ImageDraw
from generator import Generator
from parser import Parser
import math



parser = Parser()
gen = Generator(parser.parse())
gen.draw_diagram()
print('Hello')