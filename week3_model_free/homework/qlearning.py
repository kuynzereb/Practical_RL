"""
Q-learning
This file contains the same q-learning agent you implemented in the previous assignment.
The only difference is that it doesn't need any other files with it, so you can use it as a standalone module.

Here's an example:
>>>from qlearning import QLearningAgent

>>>agent = QLearningAgent(alpha=0.5,epsilon=0.25,discount=0.99,
                                             getLegalActions = lambda s: actions_from_that_state)
>>>action = agent.getAction(state)
>>>agent.update(state,action, next_state,reward)
>>>agent.epsilon *= 0.99
"""

import random, math

import numpy as np
from collections import defaultdict

def flipCoin(p):
  r = random.random()
  return r < p 

class QLearningAgent():
    """
        Q-Learning Agent

        The two main methods are 
        - self.getAction(state) - returns agent's action in that state
        - self.update(state,action,nextState,reward) - returns agent's next action

        Functions you should use
            - self.getLegalActions(state)
                which returns legal actions for a state
            - self.getQValue(state,action)
                which returns Q(state,action)
            - self.setQValue(state,action,value)
                which sets Q(state,action) := value
        
        !!!Important!!!
        NOTE: please avoid using self._qValues directly to make code cleaner
    """
    def __init__(self,alpha,epsilon,discount,getLegalActions):
        "We initialize agent and Q-values here."
        self.getLegalActions= getLegalActions
        self._qValues = defaultdict(lambda:defaultdict(lambda:0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount

    def getQValue(self, state, action):
        """
            Returns Q(state,action)
        """
        return self._qValues[state][action]

    def setQValue(self,state,action,value):
        """
            Sets the Qvalue for [state,action] to the given value
        """
        self._qValues[state][action] = value

#---------------------#start of your code#---------------------#

    def getValue(self, state):
        """
            Returns max_action Q(state,action)
            where the max is over legal actions.
        """
        
        possibleActions = self.getLegalActions(state)
        #If there are no legal actions, return 0.0
        if len(possibleActions) == 0:
            return 0.0

        max_value = self.getQValue(state, possibleActions[0])
        for action in possibleActions:
            value = self.getQValue(state, action)
            max_value = value if value > max_value else max_value

        return max_value
        
    def getPolicy(self, state):
        """
            Compute the best action to take in a state. 
            
        """
        possibleActions = self.getLegalActions(state)

        #If there are no legal actions, return None
        if len(possibleActions) == 0:
            return None
        
        max_value = self.getValue(state)
        for action in possibleActions:
            if self.getQValue(state, action) == max_value:
                return action

        return None

    def getAction(self, state):
        """
            Compute the action to take in the current state, including exploration.  
            
            With probability self.epsilon, we should take a random action.
            otherwise - the best policy action (self.getPolicy).

            HINT: You might want to use util.flipCoin(prob)
            HINT: To pick randomly from a list, use random.choice(list)

        """
        
        # Pick Action
        possibleActions = self.getLegalActions(state)
        action = None
        
        #If there are no legal actions, return None
        if len(possibleActions) == 0:
            return None

        #agent parameters:
        epsilon = self.epsilon

        if flipCoin(epsilon):
            action = random.choice(possibleActions)
        else:
            action = self.getPolicy(state)   

        return action

    def update(self, state, action, nextState, reward):
        """
            You should do your Q-Value update here

            NOTE: You should never call this function,
            it will be called on your behalf


        """
        #agent parameters
        gamma = self.discount
        lr = self.alpha

        reference_qvalue = reward + gamma * self.getValue(nextState)
        updated_qvalue = (1 - lr) * self.getQValue(state, action) + \
                         lr * reference_qvalue

        self.setQValue(state, action, updated_qvalue)


#---------------------#end of your code#---------------------#

