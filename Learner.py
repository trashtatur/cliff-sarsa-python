import random
from abc import ABCMeta, abstractmethod


class Learner(metaclass=ABCMeta):
    """
    :param actions : the actions the agent can take in its given state
    :param epsilon : the exploration value. Default is 0.1 which is 10%
    :param alpha : the immediate reward
    :param gamma : the restrain bla
    """
    @abstractmethod
    def __init__(self, actions, epsilon, alpha, gamma):

        self.qvalues = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions

    def get_qvalue(self, state, action):
        return self.qvalues.get((state, action), 0.0)

    def choose_action(self, state):

        # if this happens then do random exploration
        if random.random() < self.epsilon:
            action = random.choice(self.actions)

        else:

            qvalues = [self.get_qvalue(state, a) for a in self.actions]
            maximum_qvalue = max(qvalues)

            if qvalues.count(maximum_qvalue) > 1:
                best = [i for i in range(len(self.actions)) if qvalues[i] == maximum_qvalue]
                indicator = random.choice(best)
            else:
                # get that one maximum q value to determine the action
                indicator = qvalues.index(maximum_qvalue)
            # if not already happened determine the action
            action = self.actions[indicator]

        return action

    def learn_qvalues(self, state, action, reward, value):

        oldvalue = self.qvalues.get((state, action), None)
        if oldvalue is None:
            self.qvalues[(state, action)] = reward
        else:
            self.qvalues[(state, action)] = oldvalue + self.alpha * (value - oldvalue)

    @abstractmethod
    def learn(self, state1, action1, reward, state2, action2):
        pass
