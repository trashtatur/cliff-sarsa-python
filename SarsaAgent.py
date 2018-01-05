import Sarsa
import Agent


class SarsaAgent(Agent.Agent):


    def __init__(self, start_cell, epsilon, alpha, gamma):
        super().__init__(start_cell)
        self.ai = Sarsa.Sarsa(self.actions, epsilon, alpha, gamma)


