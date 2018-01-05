import Learner


class Sarsa(Learner.Learner):

    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        super().__init__(actions, epsilon, alpha, gamma)

    def learn(self, state1, action1, reward, state2, action2):
        # Find the q value for the next action
        next_qvalue = self.qvalues.get((state2, action2), 0)
        self.learn_qvalues(state1, action1, reward, reward + self.gamma * next_qvalue)
