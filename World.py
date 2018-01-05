import Cell
import QAgent
import SarsaAgent



class World:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.agent = None
        self.gamegrid = []
        self.start_cell = None

    def build_gamegrid(self):
        for currentY in range(self.y):
            for currentX in range(self.x):
                name = currentX, currentY
                new_cell = Cell.Cell(currentX, currentY, name.__str__())

                previous_cell = self.find_previous_cell(currentX)
                """
                :type previous_cell : Cell.Cell
                """

                # to ensure border cells don't have cells in the next row
                # as right or left neighbors
                if currentX is not 0:
                    previous_cell.right = new_cell
                    new_cell.left = previous_cell

                if currentY is 0 and currentX is not 0 and currentX is not self.x - 1:
                    new_cell.cliff = True
                if currentY is 0 and currentX is self.x-1:
                    new_cell.goal = True
                if currentY is 0 and currentX is 0:
                    self.start_cell = new_cell
                    new_cell.start = True
                if currentY >= 1:
                    new_cell.field = True

                if currentY > 0:
                    # calculates the cell that is above the current one on the grid,
                    # it has to be on the x axis exactly above, hence the subtraction
                    # no -1 because the cell hasn't been appended yet

                    above_cell = self.gamegrid[len(self.gamegrid) - self.x]
                    new_cell.up = above_cell
                    above_cell.down = new_cell

                self.gamegrid.append(new_cell)

    def find_previous_cell(self, currentx):
        # Beginning of new row
        if currentx is 0:
            return None
        else:
            indicator = len(self.gamegrid) - 1
            return self.gamegrid[indicator]

    def do_pretraining(self, duration):

        for i in range(duration):
            self.agent.update_status()

    def add_agent(self, agent_type, epsilon=0.1, alpha=0.2, gamma=0.9):

        if agent_type is "qlearn":
            self.agent = QAgent.QAgent(self.start_cell, epsilon, alpha, gamma)
        if agent_type is "sarsa":
            self.agent = SarsaAgent.SarsaAgent(self.start_cell, epsilon, alpha, gamma)


    def print_grid(self):
        i = 0
        string = ""
        for cell in self.gamegrid:
            if i % self.x is 0:

                string+="\n"
            string += str(cell)
            i += 1

