'''
File: deck.py
Author: Kunologist
Description:
    This file contains the Deck class, a class that represents a deck of tiles.
'''

import time
import random
from matplotlib.pyplot import isinteractive
from mahjong.tile import TilesConverter

from env.tiles import Tile
from env.ruleset import Ruleset

class Deck:
    '''
    Class: Deck

    ## Description

    A class that represents a deck of tiles.
    '''
    tiles = []
    sort_always = None

    def __init__(self, tiles: list or str or None = None, sort=False):
        '''
        Constructor: __init__

        ## Description

        Initializes a new deck from a list of tiles or string. If no tiles are
        given, an empty deck is created.

        ## Parameters

        - `tiles`: `list` or `str` or `Deck` or `None`
            A list of tiles or a string that represents a list of tiles. If no
            tiles are given, an empty deck is created.
        - `sort`: `bool`
            Whether to sort the deck. This state is stored so that the deck
            will always be sorted if `sort` is set to `True`.

        ## Details

        A string that represents a list of tiles is parsed to a list of tiles.
        The string must be a valid list of tiles. There are two ways to
        represent a deck:

        - Shorthand naming: `"055m123p78889s113z"`
        - Full naming: `"0m5m5m1p2p3p7p8p8p8p9p1z1z3z"`

        The above notations are both valid and equivalent.        
        
        In fact a string that uses both naming methods is also valid, but not 
        recommended.

        ---

        If a list of tiles is given, the list is checked for validity. The list
        shall contain only `Tile`s, otherwise whatever is in the list will be
        passed to the `Tile` constructor to create a new `Tile` object.

        ## Examples

        Creates a kokushi musou deck:
        
        ```python
        >>> deck = Deck("19m19p19s12345677z")
        ```
        '''
        self.sort_always = sort
        if tiles is None:
            self.tiles = []
        elif isinstance(tiles, str):
            self.tiles = self.parse_string(tiles)
        elif isinstance(tiles, list):
            self.tiles = self.parse_list(tiles)
        elif isinstance(tiles, Deck):
            self.tiles = tiles.tiles
            self.sort_always = tiles.sort_always
        else:
            raise TypeError("Invalid input type for deck creation, expected str or list, got " + str(type(tiles)))
        if sort:
            self.sort()
    
    def parse_string(self, string: str):
        '''
        Method: parse_string(string: `str`)
    
        ## Description
    
        Parses a string that represents a list of tiles to a list of tiles.
    
        ## Parameters
    
        - `string`: `str`
            A string that represents a list of tiles.
        '''
        tiles = []
        # Parse the string in reverse direction
        suit = None
        rank = None
        for i in range(len(string) - 1, -1, -1):
            if string[i].isdigit():
                rank = string[i]
                if suit is None:
                    raise ValueError("Invalid deck string: " + string)
                else:
                    tiles.append(Tile(rank + suit))
            elif string[i] in "mpsz":
                suit = string[i]
        # reverse the list so that the last tile in the string is the last tile in the list
        tiles.reverse()
        return tiles
    
    def __sort_util(self, tile: Tile) -> float:
        '''
        Method: __sort_util(tile: `Tile`)
    
        ## Description
    
        A helper method for sorting the deck.
    
        ## Parameters
    
        - `tile`: `Tile`
            A tile to be compared.

        ## Details

        This method replaces `Tile` ID compare method, which is not
        suitable for sorting. The method overrides red dora comparation
        and returns the value used in `self.sort()`.

        11 < 12 < 13 < 14 < 51 < 15 < 16 < 17 < 18 < 19, etc.
        '''
        if tile.is_red_dora():
            id = tile.get_id()
            return 14.5 if id == 51 else 24.5 if id == 52 else 34.5
        return tile.get_id()

    def sort(self):
        '''
        Method: sort()
    
        ## Description
    
        Sorts the deck in ascending order.
        '''
        self.tiles.sort(key=self.__sort_util)
    
    def get_34_array(self):
        '''
        Method: get_34_array()

        ## Description

        Returns the deck in a 34-array format.

        ## Returns

        A 34-element long array.

        ## Details

        This function will create an array with 34 elements, each means
        the number of tiles of a certain type.

        For example, a deck `12399m123p112233s` will be represented as:
        
         1m 2m 3m                9m 1p 2p 3p                   1s 2s 3s
        [1, 1, 1, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        Note that the array will omit possible dora tiles (0m, 0p, 0s).
        '''
        arr = [0] * 34
        for tile in self.tiles:
            if tile.get_suit() == "m":
                arr[tile.get_rank() - 1] += 1
            elif tile.get_suit() == "p":
                arr[tile.get_rank() + 8] += 1
            elif tile.get_suit() == "s":
                arr[tile.get_rank() + 17] += 1
            elif tile.get_suit() == "z":
                arr[tile.get_rank() + 26] += 1
        return arr

    def get_136_array(self):
        '''
        Method: get_136_array()

        ## Description

        Returns the deck in a 136-array format.

        ## Returns

        An array that has length equal to the length of the deck, with
        each element representing a tile. The tile will be represented
        as a number between 0 and 135.

        ## Details

        This function will create an array with 136 elements, each
        represents a tile. The mapping is as follows:

        - 0~3: 1m
        - 4~7: 2m
        - 8~11: 3m
        ...
        - 32~35: 9m
        - 36~39: 1p
        - 40~43: 2p
        ...
        - 68~71: 9p
        - 72~75: 1s
        ...
        - 104~107: 9s
        - 108~111: 1z
        ...
        - 132~135: 7z

        The DORA will always be the first one in the four tiles:

        - 16: 0m
        - 53: 0p
        - 88: 0s

        ## Examples

        A deck `12355m123p011224s` will be represented as:

        [0, 4, 8, 17, 18, 36, 40, 44, 88, 72, 73, 76, 77, 84]

        mapping:

        0 -> 1m
        4 -> 2m
        8 -> 3m
        17 -> 5m (not dora)
        18 -> 5m (not dora)

        36 -> 1p
        40 -> 2p
        44 -> 3p

        72 -> 1s
        73 -> 1s
        76 -> 2s
        77 -> 2s
        84 -> 4s
        88 -> 0s (dora)
        '''
        return TilesConverter().one_line_string_to_136_array(self.get_short_string())

    def parse_list(self, tile_list: list):
        '''
        Method: parse_list(list: `list`)
    
        ## Description
    
        Parses a list of tiles to a list of tiles.
    
        ## Parameters
    
        - `list`: `list`
            A list of tiles. Each can be `Tile`, or any object that can be
            used to create a `Tile` object.

        ## Returns

        A list of `Tile` objects.
        '''
        tiles = []
        for tile in tile_list:
            if isinstance(tile, Tile):
                tiles.append(tile)
            else:
                tiles.append(Tile(tile))
        return tiles

    def get_unicode_str(self):
        '''
        Method: get_unicode_str()
    
        ## Description
    
        Prints the deck in a pretty manner. Does not print the red dora.
        Does your console support Unicode?

        ## Returns

        A string that represents the deck.

        ## Details

        We use Unicode characters to represent tiles.
        '''
        if len(self.tiles) == 0:
            return ""
        return "".join([tile.get_unicode_tile() for tile in self.tiles])
    
    def get_string(self):
        '''
        Method: get_string()
    
        ## Description
    
        Returns the deck in a string format, e.g.
        `1m2m3m1p2p3p0p5p1s2s3s1z1z1z`.
    
        ## Returns

        A string that represents the deck.
        '''
        return self.__str__()

    def get_short_string(self):
        '''
        Method: get_short_string()

        ## Description

        Returns the deck in a string format, e.g.
        `123m01235p123s111z`.

        ## Returns

        A string that represents the deck.
        '''
        man = []
        pin = []
        sou = []
        char = []
        for tile in self.tiles:
            assert isinstance(tile, Tile)
            if tile.get_suit() == "m":
                man.append(tile.get_name()[0])
            elif tile.get_suit() == "p":
                pin.append(tile.get_name()[0])
            elif tile.get_suit() == "s":
                sou.append(tile.get_name()[0])
            else:
                char.append(tile.get_name()[0])
        # Sort each list
        man.sort()
        pin.sort()
        sou.sort()
        char.sort()
        # Create output string
        output_str = ""
        if len(man) != 0:
            output_str += ("".join(man) + "m")
        if len(pin) != 0:
            output_str += ("".join(pin) + "p")
        if len(sou) != 0:
            output_str += ("".join(sou) + "s")
        if len(char) != 0:
            output_str += ("".join(char) + "z")
        return output_str


        

    def get_tiles(self):
        '''
        Method: get_tiles()
    
        ## Description
    
        Returns the list of tiles in the deck.
    
        ## Returns

        A list of `Tile` objects.
        '''
        return self.tiles
    
    def pop(self):
        '''
        Method: pop()
    
        ## Description
    
        Removes and returns the last tile in the deck.
    
        ## Returns

        A `Tile` object.
        '''
        if self.sort_always:
            tile = self.tiles.pop()
            self.sort()
            return tile
        else:
            return self.tiles.pop()

    def push(self, tile: Tile):
        '''
        Method: push()
    
        ## Description
    
        Adds a tile to the end of the deck.
    
        ## Parameters

        - `tile`: `Tile`
            A tile to be added.
        '''
        self.tiles.append(tile)
        if self.sort_always:
            self.sort()
    
    def add_tile(self, tile: Tile):
        '''
        Method: add_tile()
    
        ## Description
    
        Adds a tile to the end of the deck.
    
        ## Parameters

        - `tile`: `Tile`
            A tile to be added.
        '''
        self.push(tile)
    
    def remove_tile(self, tile: Tile):
        '''
        Method: remove_tile()
    
        ## Description
    
        Removes a tile from the deck.
    
        ## Parameters

        - `tile`: `Tile`
            A tile to be removed.

        ## Raises

        - `ValueError`:
            If the tile is not in the deck.
        '''
        try:
            self.tiles.remove(tile)
        except ValueError:
            raise ValueError("Tile {} not found in deck {}".format(tile, self))
        if self.sort_always:
            self.sort()

    def append(self, tile: Tile):
        '''
        Method: append()

        ## Description

        Adds a tile to the end of the deck.

        ## Parameters

        - `tile`: `Tile`
            A tile to be added.
        '''
        self.push(tile)

    def remove(self, tile: Tile):
        '''
        Method: remove()

        ## Description

        Removes a tile from the deck.

        ## Parameters

        - `tile`: `Tile`
            A tile to be removed.

        ## Raises

        - `ValueError`:
            If the tile is not in the deck.
        '''
        self.remove_tile(tile)

    def __str__(self):
        return "".join([str(tile) for tile in self.tiles])
    
    def __repr__(self):
        return "Deck('{}')".format(self.__str__())

    def __len__(self):
        return len(self.tiles)
    
    def __getitem__(self, key):
        return self.tiles[key]
    
    def __setitem__(self, key, value):
        self.tiles[key] = value
    
    def __delitem__(self, key):
        del self.tiles[key]
    
    def __iter__(self):
        return iter(self.tiles)
    
    def __contains__(self, item):
        return item in self.tiles
    
    def __add__(self, other):
        if isinstance(other, Deck):
            return Deck(self.tiles + other.tiles, sort=self.sort_always)
        elif isinstance(other, Tile):
            return Deck(self.tiles + [other], sort=self.sort_always)
        else:
            raise TypeError("Deck can only be added to Deck or Tile")

    def __sub__(self, other):
        if isinstance(other, Deck):
            tiles = self.tiles.copy()
            for tile in other.tiles:
                try:
                    tiles.remove(tile)
                except:
                    pass
            return Deck(tiles, sort=self.sort_always)
        elif isinstance(other, Tile):
            if other in self.tiles:
                tiles = self.tiles.copy()
                tiles.remove(other)
                return Deck(tiles, sort=self.sort_always)
            else:
                raise ValueError("Tile {} not found in deck {}".format(other, self))
        else:
            raise TypeError("Deck can only be subtracted from Deck or Tile")
    
    def __eq__(self, other):
        assert isinstance(other, Deck)
        if len(self.tiles) != len(other.tiles):
            return False
        this = self.tiles.copy()
        that = other.tiles.copy()
        for tile in this:
            if tile not in that:
                return False
            that.remove(tile)
        return True

class Wall(Deck):
    '''
    Class: Wall

    ## Description

    A class that represents a wall of tiles.
    '''

    tiles = None
    dora_indicators = None
    ura_dora_indicators = None
    starting_hands = None
    replacements = None
    mountain = None

    def __init__(self, ruleset: Ruleset, random_seed: int = None, tiles: list or str or None = None, from_file: str or None = None):
        '''
        Constructor: __init__

        ## Description

        Initializes a new wall from all possible tiles.

        ## Parameters

        - `ruleset`: `Ruleset`
            The ruleset to use. The wall will be initialized accordingly.
        - `random_seed`: `int` or `None` (optional, default: `None`)
            A seed for the random number generator. If no seed is given, the
            current time is used. **Will be ignored if `tiles` is given.**
        - `tiles`: `list` or `str` or `None` (optional, default: `None`)
            A list of tiles or a string that represents a list of tiles. A
            random shuffle of the tiles will only be performed if this
            parameter is not provided.

        ## Details

        In fact, only the `redDora` and `players` property of the ruleset is
        used in wall generation.
        
        ## Examples

        To create a random wall with default ruleset (3-dora):
        
        ```python
        >>> ruleset = Ruleset() # Use a default ruleset
        >>> wall = Wall(ruleset) # Random wall
        >>> wall = Wall(ruleset, random_seed = 114) # Fixed wall
        ```

        To create a wall from a list of tiles,
        call the constructor with a list of tiles.

        ```python
        >>> ruleset = Ruleset() # Use a default ruleset
        >>> wall_114 = Wall(ruleset, 114) # Fixed wall 
        >>> wall_special = Wall(tiles = wall_114.get_tiles()) # Wall from another wall
        ```
        '''
        assert isinstance(ruleset, Ruleset), "Invalid ruleset, expected `Ruleset` object."
        self.ruleset = ruleset
        if tiles is None and from_file is None:
            # Set random seed
            random_seed = random_seed if random_seed is not None else int(time.time())
            random.seed(random_seed)
            self.random_seed = random_seed
            # Parse ruleset to get a valid tile set
            red_dora = int(ruleset.get_rule("redDora"))
            player_count = int(ruleset.get_rule("players"))
            if red_dora == 0 and player_count == 4:
                tiles = [ 
                    11, 12, 13, 14, 15, 16, 17, 18, 19,
                    21, 22, 23, 24, 25, 26, 27, 28, 29,
                    31, 32, 33, 34, 35, 36, 37, 38, 39,
                    41, 42, 43, 44, 45, 46, 47,
                    11, 12, 13, 14, 15, 16, 17, 18, 19,
                    21, 22, 23, 24, 25, 26, 27, 28, 29,
                    31, 32, 33, 34, 35, 36, 37, 38, 39,
                    41, 42, 43, 44, 45, 46, 47,
                    11, 12, 13, 14, 15, 16, 17, 18, 19,
                    21, 22, 23, 24, 25, 26, 27, 28, 29,
                    31, 32, 33, 34, 35, 36, 37, 38, 39,
                    41, 42, 43, 44, 45, 46, 47,
                    11, 12, 13, 14, 15, 16, 17, 18, 19,
                    21, 22, 23, 24, 25, 26, 27, 28, 29,
                    31, 32, 33, 34, 35, 36, 37, 38, 39,
                    41, 42, 43, 44, 45, 46, 47
                ]
            elif red_dora == 3 and player_count == 4:
                tiles = [ 
                    11, 12, 13, 14, (51), 16, 17, 18, 19,
                    21, 22, 23, 24, (52), 26, 27, 28, 29,
                    31, 32, 33, 34, (53), 36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47,
                    11, 12, 13, 14, 15,   16, 17, 18, 19,
                    21, 22, 23, 24, 25,   26, 27, 28, 29,
                    31, 32, 33, 34, 35,   36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47,
                    11, 12, 13, 14, 15,   16, 17, 18, 19,
                    21, 22, 23, 24, 25,   26, 27, 28, 29,
                    31, 32, 33, 34, 35,   36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47,
                    11, 12, 13, 14, 15,   16, 17, 18, 19,
                    21, 22, 23, 24, 25,   26, 27, 28, 29,
                    31, 32, 33, 34, 35,   36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47
                ]
            elif red_dora == 4 and player_count == 4:
                tiles = [ 
                    11, 12, 13, 14, (51), 16, 17, 18, 19,
                    21, 22, 23, 24, (52), 26, 27, 28, 29,
                    31, 32, 33, 34, (53), 36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47,
                    11, 12, 13, 14, 15,   16, 17, 18, 19,
                    21, 22, 23, 24, (52), 26, 27, 28, 29,
                    31, 32, 33, 34, 35,   36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47,
                    11, 12, 13, 14, 15,   16, 17, 18, 19,
                    21, 22, 23, 24, 25,   26, 27, 28, 29,
                    31, 32, 33, 34, 35,   36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47,
                    11, 12, 13, 14, 15,   16, 17, 18, 19,
                    21, 22, 23, 24, 25,   26, 27, 28, 29,
                    31, 32, 33, 34, 35,   36, 37, 38, 39,
                    41, 42, 43, 44, 45,   46, 47
                ]
            elif player_count == 3:
                raise NotImplementedError("3-player wall generation is not implemented yet.")
            else:
                raise Exception("Invalid redDora count: {}".format(ruleset.get_rule("redDora")))
            # Shuffle
            random.shuffle(tiles)
            # Create wall
            self.tiles = self.parse_list(tiles)
            self.game_split()
        else:
            if from_file is not None:
                import json
                with open(from_file, 'r') as f:
                    tiles = json.load(f)
                self.tiles = self.parse_list(tiles)
                self.game_split()
            else:
                self.tiles = self.parse_list(tiles)
                self.game_split()
        
    def game_split(self):
        '''
        Method: game_split(self)

        ## Description

        Split the wall into a separate list of tiles. This method should be
        called before the game starts. This method will take the `tiles` and
        split them into starting hands.

        ## Details

        - Tile 0~13, 14~27, 28~41, (42~55 if 4-player mode) are the starting
        hands for player 1, 2, 3 (and 4 if 4-player mode).

        - Tile -5 ~ 0 are the dora indicators.
        
        - Tile -10 ~ -5 are the ura dora indicators.

        - Tile -14, -13, -12, -11 are replacement tiles.
        '''
        # Get hand
        self.starting_hands = []
        player_count = self.ruleset.get_rule("players")
        for i in range(player_count):
            self.starting_hands.append(
                Deck(self.tiles[i*13:(i+1)*13], sort=True)
            )
        # Get dora
        self.dora_indicators = Deck(self.tiles[-5:])
        # Get ura dora
        self.ura_dora_indicators = Deck(self.tiles[-10:-5])
        # Get replacement tiles
        self.replacements = Deck(self.tiles[-14:-10])
        # Leave the rest of the tiles to the wall
        self.mountain = Deck(self.tiles[(player_count*13):-14])

    def get_starting_hands(self):
        '''
        Method: get_starting_hands(self)

        ## Description

        Returns the list of starting hands. The returned array will be
        `[player1, player2, player3, player4]` if in 4-player mode, or
        `[player1, player2, player3]` if in 3-player mode.
        '''
        return self.starting_hands

    def get_starting_hand(self, player: int):
        '''
        Method: get_starting_hand(self, player)

        ## Description

        Returns the starting hand for the specific player.
        '''
        assert isinstance(player, int)
        assert player in range(0, self.ruleset.get_rule("players")), "Invalid player ID, must be between 0 and {}".format(-1 + self.ruleset.get_rule("players"))
        return self.starting_hands[player]

    def get_dora_indicators(self):
        '''
        Method: get_dora_indicators(self)

        ## Description

        Returns the list of dora indicators.
        '''
        return self.dora_indicators

    def get_ura_dora_indicators(self):
        '''
        Method: get_ura_dora_indicators(self)

        ## Description

        Returns the list of ura dora indicators.
        '''
        return self.ura_dora_indicators

    def get_replacements(self):
        '''
        Method: get_replacements(self)

        ## Description

        Returns the list of replacement tiles.
        '''
        return self.replacements
    
    def get_mountain(self):
        '''
        Method: get_mountain(self)

        ## Description

        Returns the mountain.
        '''
        return self.mountain
    
    def save_tiles(self, filename: str):
        '''
        Method: save_tiles(self, filename)
            
        ## Description

        Saves the tiles to a file so as to allow replication of the game.

        ## Parameters

        - filename: The filename to save the tiles to.

        ## Details

        The file will be saved as a JSON file
        '''
        import json
        with open(filename, "w") as f:
            json.dump([t.get_id() for t in self.tiles], f)
