'''
File: deck.py
Author: Kunologist
Description:
    This file contains the Deck class, a class that represents a deck of tiles.
'''

from env.tiles import Tile

class Deck:
    '''
    Class: Deck

    ## Description

    A class that represents a deck of tiles.
    '''
    tiles = []

    def __init__(self, tiles: list or str or None = None):
        '''
        Constructor: __init__

        ## Description

        Initializes a new deck from a list of tiles or string. If no tiles are
        given, an empty deck is created.

        ## Parameters

        - `tiles`: `list` or `str` or `None`
            A list of tiles or a string that represents a list of tiles. If no
            tiles are given, an empty deck is created.

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
        >>> deck = Deck("19m19p19s1234567z")
        ```
        '''
        if tiles is None:
            self.tiles = []
        elif isinstance(tiles, str):
            self.tiles = self.parse_string(tiles)
        elif isinstance(tiles, list):
            self.tiles = self.parse_list(tiles)
        else:
            raise TypeError("Invalid input type for deck creation, expected str or list, got " + str(type(tiles)))
    
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
        tiles.sort()
        return tiles
    
    def sort(self):
        '''
        Method: sort()
    
        ## Description
    
        Sorts the deck in ascending order.
        '''
        self.tiles.sort()

    def __str__(self):
        return "".join([str(tile) for tile in self.tiles])
        # o = ""
        # for tile in self.tiles:
        #     o += str(tile)
        # return o
    
    def __repr__(self):
        return "Deck"

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
