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
from env.utils import fu_count
import random
import pickle
import random
import os

class MahjongRuleError(Exception):
    
    def __init__(self, message, world_state):
        self.message = message
        self.world_state = world_state

    def __str__(self):
        # Create a random 4-letter code for the error
        error_id = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(5))
        # Dump the world state to a pickle file
        os.makedirs('errors_log', exist_ok=True)
        with open('error_log/' + error_id + '.pkl', 'wb') as f:
            pickle.dump(self.world_state, f)
        return "MahjongRuleError: {}\nError ID: {} (state dumped to error_log/{}.pkl)".format(self.message, error_id, error_id)

class MahjongEndGame(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return "MahjongEndGame: {}".format(self.message)

def get_tiles_from_call(call_str: str) -> Tile:
    '''
    Function: get_tiles_from_call

    ## Description

    Returns the tiles corresponding to the call string. All tiles will
    be found and returned in a list.

    ## Parameters

    - `call_str`: `str`
        The call string.

    ## Returns

    A list of `Tile`s.
    '''
    tiles = []
    # Only keep numeric characters
    call_str = ''.join(filter(str.isdigit, call_str))
    # Two digits is a tile, separate the string
    call_str_pairs = [call_str[i:i+2] for i in range(0, len(call_str), 2)]
    # Transform the string pairs into tiles
    for pair in call_str_pairs:
        tiles.append(Tile(int(pair)))
    return tiles

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

    def set_player(self, player_idx: int, player: Player):
        '''
        Method: set_player()

        ## Description

        Sets the player at the given index.

        ## Parameters

        - `player_idx`: `int`
            The index of the player.
        - `player`: `Player`
            The player to set.
        '''
        self.players[player_idx] = player
        
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
            "credits": [
                # self.ruleset.get_rule("starting_credits") for _ in range(len(self.players))
                25000 for _ in range(len(self.players))
            ],
            "wind": "E",
            "round": 1,
            "repeat": 0,
            "wind_e": random.randint(0, 3),
            "calls": [
                [] for _ in range(len(self.players))
            ],
            "reach": [
                False for _ in range(len(self.players))
            ],
            "ippatsu": [
                0 for _ in range(len(self.players))
            ],
            "end_game": False,
            "no_draw": False
        }
        self.history = {
            "actions": [],
        }
        # Initialize players
        for i in range(len(self.players)):
            self.players[i].initialize()
        # Initialize player hands
        self.hands = [self.wall.get_starting_hand(i) for i in range(len(self.players))]

    def record(self, obs, action):
        '''
        Method: record()

        ## Description

        Records the action.
        '''
        self.history["actions"].append((obs, action))
        with open("game-log.log", "w") as f:
            f.write(str(self.history))

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
        if self.state["no_draw"]:
            tile = None
            self.state["no_draw"] = False
        else:
            if len(self.wall.mountain) == 0:
                # Start ten / no ten query
                # TODO
                # End game
                self.end_game({
                    "reason": "wall_empty",
                    "credits": [0, 0, 0, 0]  
                })
            else:
                tile = self.wall.mountain.pop()
            
        rinshan_continue = True # 嶺上
        # Perform action
        discarded_tile = Tile()
        while rinshan_continue:
            rinshan_continue = False
            # Query player for action: active
            obs = self.get_observation(player_idx, {
                "player_state": "active",
                "incoming_tile": tile
            })
            action = player.act(obs)
            # Record action
            self.record(obs, action)
            # Perform action
            discarded_tile = self.perform_action(action, obs)
            if action.action_type == "kan" or action.action_type == "akan" or action.action_type == "mkan" or action.action_type == "nukidora":
                rinshan_continue = True
                # Rinshan draw
                try:
                    tile = self.wall.get_replacements().pop()
                except IndexError:
                    # Suukaikan but the same player, no more tiles to draw
                    self.end_game({
                        "reason": "suukaikan",
                        "credits": [0, 0, 0, 0]
                    })
            else:
                rinshan_continue = False
        # Query other players for action: passive
        for i in range(len(self.players)):
            if i != player_idx:
                passive_obs = self.get_observation(i, {
                    "player_state": "passive",
                    "incoming_tile": discarded_tile
                })
                passive_action = self.players[i].act(passive_obs)
                # Record action
                self.record(passive_obs, passive_action)
                # Perform action
                self.perform_action(passive_action, passive_obs)

        # Update game state
        self.state["player_idx"] = (player_idx + 1) % len(self.players)

    def end_game(self, end_game_args: dict):
        '''
        Method: end_game()
        
        ## Description

        Ends the game.
        '''
        # End game event
        self.state["end_game"] = end_game_args
        print(end_game_args)
        for player_idx in range(len(self.players)):
            self.state["credits"][player_idx] += end_game_args["credits"][player_idx]
        raise MahjongEndGame(self.state["end_game"])
        
    def calculate_credits(self, player_idx: int, ron_or_tsumo: str or int, ron_from: int = -1) -> list:
        '''
        Method: calculate_credits()

        ## Description

        Calculates the credits for the player.

        ## Parameters

        - `player_idx`: `int`
            The index of the player.
        - `ron_or_tsumo`: `str`
            The type of ron or tsumo. Can be "ron" or "tsumo".

        ## Returns

        A list of credits for each player.
        '''
        credits = [0, 0, 0, 0]
        if ron_or_tsumo == "ron":
            # Calculate ron credits
            # TODO
            credits[player_idx] = 1
            credits[ron_from] -= 1
        elif ron_or_tsumo == "tsumo":
            # Calculate tsumo credits
            # TODO
            credits[0] = credits[1] = credits[2] = credits[3] = -0.333
            credits[player_idx] = 1
        return credits
            
    def perform_action(self, action: Action, obs: dict = None):
        '''
        Method: perform_action()

        ## Description
        
        Performs an action. An action will change the state of the game,
        which means this function is the core of the gameplay.

        ## Returns

        A `Tile` if the action is a discard or replace, otherwise `None`.
        '''
        assert isinstance(action, Action)
        # Get player
        player = self.state["player_idx"]
        # Get player
        player = self.players[player]
        # Perform action
        print(action)
        if action.action_type == "kan":
            # 加槓
            player_idx = obs["player_idx"]
            if get_tiles_from_call(action.action_string)[0] != obs["incoming_tile"]:
                raise MahjongRuleError("Kakan must be called with the incoming tile {}, but got {} from action string".format(obs["incoming_tile"], get_tiles_from_call(action.action_string)[0]), self)
            # Get the tile to kan
            tile = obs["incoming_tile"]
            kanned = False
            # Check wheter the player previously has called pon
            for call_idx in range(len(self.state["calls"][player_idx])):
                call = self.state["calls"][player_idx][call_idx]
                if call.find("p") != -1 and get_tiles_from_call(call)[0] == tile:
                    # Kakan OK, replace the pon with the kan
                    self.state["calls"][player_idx][call_idx] = action.action_string
                    kanned = True
                    break
            # If kan failed, raise an error
            if not kanned:
                raise MahjongRuleError("Kakan failed: player {} does not have pon for tile {}".format(player_idx, tile), self)
            # Whether the rest players can call ron due to chankan
            for i in range(len(self.players)):
                if i != player_idx:
                    chankan_obs = self.get_observation(i, {
                        "player_state": "chankan",
                        "incoming_tile": tile
                    })
                    action = self.players[i].act(chankan_obs)

                    self.record(chankan_obs, action)
            # Check for Suukaikan
            kans = []
            for i in range(len(self.players)):
                for call in self.state["calls"][i]:
                    if call.find("k") != -1:
                        kans.append(i)
            if len(kans) >= 5 or len(kans) == 4 and len(set(kans)) != 1:
                self.end_game({
                    "reason": "suukaikan",
                    "credits": [0, 0, 0, 0]
                })
            # Return the tile
        elif action.action_type == "mkan":
            pass
        elif action.action_type == "akan":
            pass
        elif action.action_type == "chii":
            player_idx = obs["player_idx"]
            action_string = action.action_string
            # Append the chi to the player's calls
            self.state["calls"][player_idx].append(action_string)
            # Append the incoming tile to the player's hand
            self.hands[player_idx].append(obs["incoming_tile"])
            # Remove the tiles used in the chii
            for tile in get_tiles_from_call(action_string):
                try:
                    self.hands[player_idx].remove(tile)
                except ValueError:
                    raise MahjongRuleError("Chii failed: player {} does not have tile {}".format(player_idx, tile), self)
            # Set the active player to be the previous player, so as to step to the chi caller
            self.state["player_idx"] = (player_idx - 1) % len(self.players)
            # Disallow the next draw tile
            self.state["no_draw"] = True
            return None
        elif action.action_type == "pon":
            player_idx = obs["player_idx"]
            action_string = action.action_string
            # Append the pon to the player's calls
            self.state["calls"][player_idx].append(action_string)
            # Append the incoming tile to the player's hand
            self.hands[player_idx].append(obs["incoming_tile"])
            # Remove the tiles used in the pon
            for tile in get_tiles_from_call(action_string):
                try:
                    self.hands[player_idx].remove(tile)
                except ValueError:
                    raise MahjongRuleError("Pon failed: player {} does not have tile {}".format(player_idx, tile), self)
            # Set the active player to be the previous player, so as to step to the pon caller
            self.state["player_idx"] = (player_idx - 1) % len(self.players)
            return None
        elif action.action_type == "tsumo":
            # Win the game
            player_idx = obs["player_idx"]
            if obs["active_player"] != player_idx:
                raise MahjongRuleError("Tsumo must be called by the active player {}, but got {}".format(player_idx, obs["active_player"]), self)
            credits = self.calculate_credits(player_idx, "tsumo")
            self.end_game({
                "reason": "tsumo",
                "credits": credits
            })
        elif action.action_type == "reach":
            # Get the tile to cut
            tile_id = action.action_string[-2:]
            player_idx = obs["player_idx"]
            if int(tile_id) == 60:
                # Discard the incoming tile
                tile = obs["incoming_tile"]
                # Add the discarded tile to the player's discarded tiles
                self.state["discarded_tiles"][player].append(tile)
                # Reach state
                self.state["reach"][player_idx] = True
                self.state["ippatsu"][player_idx] = True
                # Return the discarded tile
                return tile
            else:
                # Replace and reach
                tile = Tile(int(tile_id))
                # Remove one tile from the player's hand
                try:
                    self.hands[player_idx].remove_tile(tile)
                except ValueError:
                    raise ValueError("Player {} does not have the tile {}.".format(player_idx, tile))
                # Add the drawn tile to the player's hand
                self.hands[player_idx].add_tile(obs["incoming_tile"])
                # Add the drawn tile to the player's discarded tiles
                self.state["discarded_tiles"][player_idx].append(obs["incoming_tile"])
                # Reach state
                self.state["reach"][player_idx] = True
                self.state["ippatsu"][player_idx] = True
                # Return the tile
                return tile
        elif action.action_type == "ron":
            # Win the game
            player_idx = obs["player_idx"]
            ron_from = obs["active_player"]
            credits = self.calculate_credits(player_idx, "ron", ron_from)
            self.end_game({
                "reason": "ron",
                "credits": credits
            })
        elif action.action_type == "discard":
            # Discard the incoming tile
            player_idx = obs["player_idx"]
            tile = obs["incoming_tile"]
            # Add the discarded tile to the player's discarded tiles
            self.state["discarded_tiles"][player_idx].append(tile)
            # Return the discarded tile
            return tile
        elif action.action_type == "replace":
            # Get the tile to cut
            tile_id = action.action_string
            # Turn into a tile
            tile = Tile(int(tile_id))
            # Remove one tile from the player's hand
            try:
                self.hands[obs["player_idx"]].remove_tile(tile)
            except ValueError:
                raise ValueError("Player {} does not have the tile {}.".format(obs["player_idx"], tile))
            # Add the discarded tile to the player's discarded tiles
            self.state["discarded_tiles"][obs["player_idx"]].append(tile)
            # Add the drawn tile to the player's hand
            if obs["incoming_tile"] is not None:
                self.hands[obs["player_idx"]].add_tile(obs["incoming_tile"])
            # Return the tile
            return tile
        elif action.action_type == "ten":
            pass
        elif action.action_type == "noten":
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
        obs["credits"] = self.state["credits"]
        # A player can see whether a player is reach, and whether ippatsu is available
        obs["reach"] = self.state["reach"]
        obs["ippatsu"] = self.state["ippatsu"]
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
