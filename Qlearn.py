import Learner


class Qlearn(Learner.Learner):

    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        super().__init__(actions, epsilon, alpha, gamma)

    def learn(self, state1, action1, reward, state2):
        # finds the highest q value for the next state from all possible actions
        max_new_qvalue = max([self.get_qvalue(state2, action) for action in self.actions])
        self.learn_qvalues(state1, action1, reward, reward + self.gamma * max_new_qvalue)
