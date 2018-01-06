import random
from abc import ABCMeta, abstractmethod

import numpy


class Learner(metaclass=ABCMeta):
    """
    :param actions : the actions the agent can take in its given state
    :param epsilon : the exploration value. Default is 0.1 which is 10%
    :param alpha : the learning value. Should be between 0 and 1. Closer to 0 than 1
                   indicates how much a utility value is updated when an action is taken
    :param gamma : the discount factor. Encourages the agent to go for bigger future rewards.
                   Should be between 0 and 1. Preferably 0.9 or 0.99
    """
    @abstractmethod
    def __init__(self, actions, epsilon, alpha, gamma):

        self.qvalues = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.explore = 0

    def get_qvalue(self, state, action):
        return self.qvalues.get((state, action), 0.0)

    def choose_action(self, state):

        # if this happens then do random exploration
        if random.choice(numpy.arange(0.01, 1, 0.01)) < self.epsilon:
            action = random.choice(self.actions)
            self.explore += 1
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

