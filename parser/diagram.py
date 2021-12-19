class Diagram:

    def __init__(self, width: int, height: int, background: str):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.background = background
        self.shapes = []
        self.connectors = []
