'''
File: agent.py
Author: Kunologist
Description:
    This file contains an agent that can play the game of mahjong.

'''

import random

class Agent:
    '''
    Class: Agent

    ## Description

    A class that represents an agent that can play the game of mahjong.
    This class serves as a base class for other agents.
    '''
    def __init__(self, name):
        self.name = name

    def query(self, obs, action_space):
        # Random select
        return random.choice(action_space)

