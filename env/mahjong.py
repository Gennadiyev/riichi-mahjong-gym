'''
File: mahjong.py
Author: Kunologist
Description:
    The backend of the mahjong game.
'''

from multiprocessing.sharedctypes import Value
from env.deck import Deck, Wall
from env.ruleset import Ruleset
from env.player import Player
from env.action import Action
from env.tiles import Tile
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
            "player_idx": 0,
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
            "wind_e": random.randint(0, 3),
            "calls": [
                [] for _ in range(len(self.players))
            ]
        }
        # Initialize players
        for i in range(len(self.players)):
            self.players[i].initialize()
        # Initialize player hands
        self.hands = [self.wall.get_starting_hand(i) for i in range(len(self.players))]

    def step(self):
        '''
        Method: step()

        ## Description
        
        Performs a step in the game.
        '''
        # Get current player
        player_idx = self.state["player_idx"]
        # Get player
        player = self.players[player_idx]
        # Draw a tile from the wall
        tile = self.wall.mountain.pop()
        # Query player for action: active
        obs = self.get_observation(player_idx, {
            "player_state": "active",
            "incoming_tile": tile
        })
        action = player.act(obs)
        # Perform action
        discarded_tile = self.perform_action(action, obs)
        # Query other players for action
        for i in range(len(self.players)):
            if i != player_idx:
                self.players[i].act(self.get_observation(i, {
            "player_state": "passive",
            "incoming_tile": tile
        }))
        # Update game state
        self.state["player_idx"] = (player_idx + 1) % len(self.players)

    def perform_action(self, action: Action, obs: dict = None):
        '''
        Method: perform_action()

        ## Description
        
        Performs an action.
        '''
        assert isinstance(action, Action)
        # Get player
        player = self.state["player_idx"]
        # Get player
        player = self.players[player]
        # Perform action
        if action == "kan":
            pass
        elif action == "mkan":
            pass
        elif action == "chi":
            pass
        elif action == "pon":
            pass
        elif action == "tsumo":
            pass
        elif action == "reach":
            pass
        elif action == "ron":
            pass
        elif action == "discard":
            pass
        elif action.action_type == "replace":
            # Get the tile to cut
            tile_id = action.action_string
            tile = Tile(int(tile_id))
            try:
                self.hands[obs["player_idx"]].remove_tile(tile)
            except ValueError:
                raise ValueError("Player {} does not have the tile {}.".format(obs["player_idx"], tile))
            self.hands[obs["player_idx"]].add_tile(obs["incoming_tile"])
            return tile
        elif action == "ten":
            pass
        elif action == "noten":
            pass

    def get_observation(self, player_idx: int, additional_dict: dict = []) -> dict:
        '''
        Method: get_observation()

        ## Description
        
        Gets the observation of the player.
        '''
        
        obs = {}
        # Get player
        obs["active_player"] = self.state["player_idx"]
        # Get player
        obs["player_idx"] = player_idx
        # Create observation dictionary
        # A player can see the hand
        obs["hand"] = self.hands[player_idx]
        # A player can see the revealed dora indicators
        obs["dora_indicators"] = self.wall.dora_indicators[0:self.state["dora_revealed"]]
        # A player can see the discarded tiles from all players
        obs["discarded_tiles"] = self.state["discarded_tiles"]
        # A player can see the calls from all players
        obs["calls"] = self.state["calls"]
        # A player can see the wind
        obs["wind"] = self.state["wind"]
        # A player can see the repeat
        obs["repeat"] = self.state["repeat"]
        # A player can see the wind east
        obs["wind_e"] = self.state["wind_e"]
        # A player can see all players' credit
        obs["player_credit"] = self.state["player_credit"]
        # Merge additional dict
        obs.update(additional_dict)
        return obs

    def play(self):
        '''
        Method: play()

        ## Description
        
        Plays the game.
        '''
        # Initialize game
        self.initialize_game()
        # Play game
        while True:
            self.step()
            # Check if game is over
            if self.is_over():
                break
    
    def is_over(self):
        '''
        Method: is_over()

        ## Description
        
        Checks if the game is over.
        '''
        # Case 1: Mountain is empty
        if len(self.wall.mountain) == 0:
            return True