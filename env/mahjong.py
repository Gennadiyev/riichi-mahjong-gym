'''
File: mahjong.py
Author: Kunologist
Description:
    The backend of the mahjong game.
'''

from env.deck import Deck, Wall
from env.ruleset import Ruleset
from env.player import Player
from env.action import Action
import random

class MahjongGame():
    '''
    Class: MahjongGame

    ## Description
    
    A class that represents a player that can play the game of mahjong.
    '''
    def __init__(self, ruleset: Ruleset, **kwargs):
        '''
        Constructor: __init__

        ## Description
        
        The constructor of the MahjongGame class.

        ## Parameters
        
        - `ruleset`: `Ruleset`
            The ruleset of the game.
        '''
        # Apply ruleset
        self.ruleset = ruleset
        # Initialize wall
        random_seed = kwargs.get('random_seed', None)
        self.wall = Wall(ruleset, random_seed=random_seed)
        # Initialize players
        self.players = []
        for i in range(ruleset.get_rule("players")):
            self.players.append(Player("Player {}".format(i+1), is_manual=True))
        # Initialize game state
        self.state = {}
    
    def initialize_game(self):
        '''
        Method: initialize_game()

        ## Description
        
        Initializes the game.
        '''
        self.state = {
            "dora_revealed": 1,
            "player": 0,
            "discarded_tiles": [
                [] for _ in range(len(self.players))
            ],
            "player_credit": [
                # self.ruleset.get_rule("starting_credits") for _ in range(len(self.players))
                25000 for _ in range(len(self.players))
            ],
            "wind": "E",
            "round": 1,
            "repeat": 0,
            "wind_e": random.randint(0, 3)
        }
        # Initialize players
        for i in range(len(self.players)):
            self.players[i].initialize()
            self.players[i].set_hand(self.wall.get_starting_hand(i))

    def step(self):
        '''
        Method: step()

        ## Description
        
        Performs a step in the game.
        '''
        # Get current player
        player = self.state["player"]
        # Get player
        player = self.players[player]
        # Draw a tile from the wall
        tile = self.wall.mountain.pop()
        player.draw_tile(tile)
        # Query player for action
        action = player.act(self.get_observation(player))
        # Perform action
        self.perform_action(action)
        # Query other players for action
        for i in range(len(self.players)):
            if i != player:
                self.players[i].act(self.get_observation(i))
        # Update game state
        self.state["player"] = (player + 1) % len(self.players)

    def perform_action(self, action: Action):
        '''
        Method: perform_action()

        ## Description
        
        Performs an action.
        '''
        assert isinstance(action, Action)
        # Get player
        player = self.state["player"]
        # Get player
        player = self.players[player]
        # Perform action
        if action.action_type == "kan":
            pass
        elif action.action_type == "mkan":
            pass
        elif action.action_type == "chi":
            pass
        elif action.action_type == "pon":
            pass
        elif action.action_type == "tsumo":
            pass
        elif action.action_type == "reach":
            pass
        elif action.action_type == "ron":
            pass
        elif action.action_type == "discard":
            pass
        elif action.action_type == "replace":
            pass
        elif action.action_type == "ten":
            pass
        elif action.action_type == "noten":
            pass

    def get_observation(self, player_idx: int) -> dict:
        '''
        Method: get_observation()

        ## Description
        
        Gets the observation of the player.
        '''
        # Get player
        player = self.players[player_idx]
        # Get player
        player = self.state["player"]
        # Create observation dictionary
        obs = {}
        # An player can see the hand
        obs["hand"] = player.get_hand()
        # An player can see the revealed dora indicators
        obs["dora_indicators"] = self.wall.dora_indicators[0:self.state["dora_revealed"]]
        # An player can see the discarded tiles from all players
        obs["discarded_tiles"] = self.state["discarded_tiles"]
        # An player can see which player is active
        obs["player"] = player
        # An player can see the wind
        obs["wind"] = self.state["wind"]
        # An player can see the repeat
        obs["repeat"] = self.state["repeat"]
        # An player can see the wind east
        obs["wind_e"] = self.state["wind_e"]
        # An player can see the player's credit
        obs["player_credit"] = self.state["player_credit"][player]
        return obs

        