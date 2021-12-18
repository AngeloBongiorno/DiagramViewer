class Connector:

    def __init__(self, tag: str, startx: int, starty: int, endx: int, endy: int, bgcolor: str) -> None:
        self.tag = tag
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.bgcolor = bgcolor