from abc import ABCMeta, abstractmethod

cliffReward = -100
step_costs = -1
goalReward = +50


class Agent(metaclass=ABCMeta):
    """
    :type start_cell : Cell.Cell

    """

    @abstractmethod
    def __init__(self, start_cell):

        self.score = 0
        self.deaths = 0
        self.actions = [1, 2, 3, 4]
        self.cell = start_cell
        self.start = start_cell
        self.previous_state = self.define_state()
        self.previous_action = None
        self.ai = None
        """
        :type self.ai Learner.Learner
        """

        # An agent also needs to be instantiated with an AI component, derived from the learner class

    def define_state(self):
        return self.cell.name

    def define_reward(self):
        if self.cell.cliff:
            self.deaths += 1
            return cliffReward

        elif self.cell.goal:
            self.score += 1
            return goalReward
        else:
            return step_costs




    def move_up(self):
        if self.cell.up is not None:
            self.cell = self.cell.up

    def move_down(self):
        if self.cell.down is not None:
            self.cell = self.cell.down

    def move_left(self):
        if self.cell.left is not None:
            self.cell = self.cell.left

    def move_right(self):
        if self.cell.right is not None:
            self.cell = self.cell.right
