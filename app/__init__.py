from generator import Generator
from parser import Parser



parser = Parser()

gen = Generator(parser.parse())
gen.draw_diagram()
print('Hello')