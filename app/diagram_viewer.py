from generator import Generator
from parser import Parser


# file principale che richiama tutte le classi

parser = Parser()

# il metodo parse() è da parametrizzare con l'indirizzo del file xml che invia l'utente
parsed_data = parser.parse()

gen = Generator(parsed_data)

# il metodo mostra il diagramma a schermo con .show()
gen.draw_diagram()
