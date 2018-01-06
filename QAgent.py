import Qlearn
import Agent


class QAgent(Agent.Agent):


    def __init__(self, start_cell, epsilon, alpha, gamma):
        super().__init__(start_cell)
        self.ai = Qlearn.Qlearn(self.actions, epsilon, alpha, gamma)

    def update_status(self):
        reward = self.define_reward()
        state = self.define_state()
        action = self.ai.choose_action(state)

        if self.previous_action is not None:
            self.ai.learn(self.previous_state, self.previous_action, reward, state)

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