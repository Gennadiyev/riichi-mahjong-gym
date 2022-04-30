'''
File: player.py
Author: Kunologist
Description:
    This file contains a player, or agent, that can play the game of mahjong.
'''

from env import action
from env.deck import Deck
from env.tiles import Tile
from env.action import Action
from env.agent import Agent
from env.utils import check_reach, check_agari

class Player():
    '''
    Class: Player
    
    ## Description
    
    A class that represents a player, or agent, that can play the game of mahjong.
    '''
    
    hand = None
    calls = None
    name = None
    is_manual = None
    agent = None
    incoming_tile = None

    def __init__(self, name: str, is_manual: bool = False, agent: Agent = None):
        '''
        Constructor: __init__
        
        ## Description
        
        The constructor of the Agent class.
        
        ## Parameters
        
        - `name`: `str`
            The name of the player.
        - `is_manual`: `bool`
            Whether the player is a human or not.
        - `agent`: `Agent`
            The agent that performs actions for the player.
        '''
        assert isinstance(name, str)
        assert isinstance(is_manual, bool)
        assert isinstance(agent, Agent)
        self.name = name
        self.is_manual = is_manual
        self.agent = agent
    
    def act(self, obs: dict):
        '''
        Method: act(obs)
        
        ## Description
        
        This method is called when the agent is supposed to act. The agent
        will be asked to act when the agent draws a tile, and when the agent
        has a chance to perform an action.
        
        ## Parameters
        
        - `obs`: `dict`
            The observation of the game.
        '''
        # Get action space
        action_space = self.get_action_space(obs)
        # Query for action
        if self.is_manual:
            return self.manual_act(obs, action_space)
        else:
            return self.agent.query(obs, action_space)
    
    def initialize(self):
        '''
        Method: initialize()
        
        ## Description

        This method is called when the agent is initialized.
        '''
        self.calls = []
        self.hand = []
        self.incoming_tile = None

    def set_hand(self, hand: Deck):
        '''
        Method: set_hand(hand)
        
        ## Description
        
        This method is called when the agent is supposed to set its hand.
        
        ## Parameters
        
        - `hand`: `Deck`
            The hand of the player.
        '''
        assert isinstance(hand, Deck)
        self.hand = hand
    
    def draw_tile(self, tile: Tile):
        '''
        Method: draw_tile(tile)
        
        ## Description
        
        This method is called when the agent is supposed to draw a tile.
        
        ## Parameters
        
        `tile`: `Tile`
            The tile that is drawn.
        '''
        assert isinstance(tile, Tile)
        self.incoming_tile = tile
    
    def get_action_space(self, obs: dict) -> list:
        '''
        Method: get_action_space()
        
        ## Description
        
        This method is called when the agent is supposed to get the action
        space.
        
        ## Parameters
        
        - `obs`: `dict`
            The observation of the game.

        ## Returns

        `list` of `Action`
            The action space of the agent. See `actions.md` documentation
            for more information.
        '''
  
        # Prepare action space
        action_space = []
        
        # Check if the player is active
        if self.incoming_tile is not None:
            # Merge the incoming tile to the current hand
            hand = self.hand.get_tiles().copy()
            hand.append(self.incoming_tile)
            calls = self.calls
            hand.sort()
            # Player with incoming tile can call: kan, akan, discard, replace, reach, tsumo

            # Check for kan
            for call in calls:
                if call.find("p"):
                    # Pon found, check for kan
                    tile_id = int(call[-2:])
                    if Tile(tile_id) in hand:
                        action_space.append(Action.KAN(call))
            
            # Check for akan
            same_tile = 0
            previous_tile = Tile()
            for tile in hand:
                if tile == previous_tile:
                    same_tile += 1
                else:
                    same_tile = 0
                if same_tile == 4:
                    action_space.append(Action.AKAN(tile.get_id()))
                previous_tile = tile

            # Default: allow discard
            action_space.append(Action.DISCARD())

            # Default: allow replace
            for tile in hand:
                action_space.append(Action.REPLACE(tile.get_id()))

            # Check for reach
            if obs["player_credit"][obs["player"]] >= 1000:
                reach_discard = check_reach(hand, calls)
                if reach_discard:
                    for reach_discard_tile in reach_discard:
                        # Check whether the tile is incoming
                        if reach_discard_tile == self.incoming_tile:
                            action_space.append(Action.REACH(0))
                            # If also in hand, allow another reach action
                            if reach_discard_tile in self.hand.get_tiles():
                                action_space.append(Action.REACH(reach_discard_tile.get_id()))
                        else:
                            action_space.append(Action.REACH(reach_discard_tile.get_id()))
            
            # Check for tsumo
            if check_agari(hand):
                action_space.append(Action.TSUMO())
            

