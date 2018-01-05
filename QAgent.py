import Qlearn
import Agent


class QAgent(Agent.Agent):


    def __init__(self, start_cell, epsilon, alpha, gamma):
        super().__init__(start_cell)
        self.ai = Qlearn.Qlearn(self.actions, epsilon, alpha, gamma)
