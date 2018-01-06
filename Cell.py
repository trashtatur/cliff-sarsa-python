class Cell:

    def __init__(self, name):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.goal = False
        self.start = False
        self.cliff = False
        self.field = False
        self.name = name
