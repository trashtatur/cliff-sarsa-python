class Cell:

    def __init__(self, x, y, name):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.goal = False
        self.start = False
        self.cliff = False
        self.field = False
        self.name = name

    def __str__(self):
        lname = ""
        rname = ""
        upname= ""
        downname= ""
        if self.down is not None:
            downname=self.down.name
        if self.up is not None:
            upname=self.up.name
        if self.left is not None:
            lname=self.left.name
        if self.right is not None:
            rname=self.right.name
        return "|| C: " + self.name + " l: " + lname + " r:" + rname + " u:" + upname + " d:" + downname
