import numpy as np
from icecream import ic


# TODO:(Xiaoyang) REFACTOR THIS CLASS SOON...
# Note: if any of you want to modify this one, please lmk first.
class Agent(object):

    def __init__(self, num_actions):
        self.use_raw = False
        self.num_actions = num_actions
        # Values
        self.Q = None

    def step(self, state):
        legal_actions = list(state['legal_actions'].keys())
        return np.random.choice(legal_actions)

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        probs = [0 for _ in range(self.num_actions)]
        for i in state['legal_actions']:
            probs[i] = 1/len(state['legal_actions'])

        info = {}
        info['probs'] = {state['raw_legal_actions'][i]: probs[list(
            state['legal_actions'].keys())[i]] for i in range(len(state['legal_actions']))}

        return self.step(state), info
