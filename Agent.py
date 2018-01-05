from abc import ABCMeta, abstractmethod

cliffReward = -50
normalReward = -1
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
            return normalReward

    def update_status(self):
        reward = self.define_reward()
        state = self.define_state()
        action = self.ai.choose_action(state)

        if self.previous_action is not None:
            self.ai.learn(self.previous_state, self.previous_action, reward, state, action)

        self.previous_state = state
        self.previous_action = action

        if self.cell.cliff or self.cell.goal:
            self.cell = self.start
            self.previous_action = None
        else:
            if action is 1:
                self.move_up()
            if action is 2:
                self.move_left()
            if action is 3:
                self.move_right()
            if action is 4:
                self.move_down()

        return self.cell.name


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
