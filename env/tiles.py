'''
File: tiles.py
Author: Kunologist
Description:
    This file contains the Tile class, which is used to represent a single
    tile in the mahjong game.
'''

import random

class Tile:
    '''
    Class: tile

    ## Description
    
    This class is used to represent a single tile in the mahjong game.

    ## Details

    The ID of the card is used to represent the card object. The mapping
    between the ID and the card object is as follows:

    - `11` ~ `19`: 1~9 man
    - `21` ~ `29`: 1~9 pin
    - `31` ~ `39`: 1~9 sou
    - `41` ~ `47`: ton, nan, shaa, pei, haku, hatsu, chun
    - `51` ~ `53`: Red dora 5 man, 5 pin, 5 sou 
    '''

    id = None
    hidden_id = None
    valid_id = [0, 
                11, 12, 13, 14, 15, 16, 17, 18, 19,
                21, 22, 23, 24 ,25, 26, 27, 28, 29,
                31, 32, 33, 34, 35, 36, 37, 38, 39,
                41, 42, 43, 44, 45, 46, 47, 48, 49,
                51, 52, 53]

    def __init__(self, constructor = None):
        '''
        Constructor: __init__

        ## Description

        Creates a tile object from a tile object, a string, or an integer.

        ## Parameters

        - `constructor`: `tile` or `str` or `int`

        ## Details

        If the constructor is a tile object, the tile object is copied.

        If the constructor is a string, the tile object is created from the
        string. Specify the rank, then the suit, without spaces.

        - `"1m"` ~ `"9m"`: 1~9 man
        - `"1p"` ~ `"9p"`: 1~9 pin
        - `"1s"` ~ `"9s"`: 1~9 sou
        - `"1z"` ~ `"7z"`: ton, nan, shaa, pei, haku, hatsu, chun
        - `"0m", "0p", "0s": Red dora 5 man, 5 pin, 5 sou

        If the constructor is an integer, the tile object is created from the
        number.

        - `11` ~ `19`: 1~9 man
        - `21` ~ `29`: 1~9 pin
        - `31` ~ `39`: 1~9 sou
        - `41` ~ `47`: ton, nan, shaa, pei, haku, hatsu, chun
        - `51` ~ `53`: Red dora 5 man, 5 pin, 5 sou

        ## Examples

        ```python
        >>> tile_1m = tile('1m')
        >>> tile_3p = tile(23)
        >>> tile_r5s = tile('0s')
        ```
        '''
        self.hidden_id = random.random()
        if isinstance(constructor, Tile):
            self.id = constructor.id
        elif isinstance(constructor, str):
            self.id = self.__str_to_id(constructor)
        elif isinstance(constructor, int):
            self.__set_id_with_check(constructor)
        elif constructor is None:
            self.id = 0
        else:
            raise TypeError("Invalid constructor type {}, expected tile, str, or int".format(type(constructor)))

    def __str_to_id(self, str_id: str) -> int:
        '''
        Method: __str_to_id

        ## Description

        Converts a string to an integer ID.

        ## Parameters

        - `str_id`: ID of the tile as string

        ## Details

        The string is converted to an integer ID.

        - `"1m"` ~ `"9m"`: 1~9
        - `"1p"` ~ `"9p"`: 1~9
        - `"1s"` ~ `"9s"`: 1~9
        - `"1z"` ~ `"7z"`: ton, nan, shaa, pei, haku, hatsu, chun
        - `"0m", "0p", "0s": Red dora 5
        '''

        assert isinstance(str_id, str), "str_id must be a string"
        assert len(str_id) == 2 and str_id[0] in "0123456789" and str_id[1] in "mpsz", "Invalid string ID"
        
        if str_id[0] == "0":
            if str_id[1] == "m":
                return 51
            elif str_id[1] == "p":
                return 52
            elif str_id[1] == "s":
                return 53

        if str_id[1] == 'm':
            return int(str_id[0]) + 10
        elif str_id[1] == 'p':
            return int(str_id[0]) + 20
        elif str_id[1] == 's':
            return int(str_id[0]) + 30
        elif str_id[1] == 'z':
            return int(str_id[0]) + 40
    
    def __id_to_str(self) -> str:
        '''
        Method: __id_to_str

        ## Description

        Returns the string ID of the tile.

        ## Returns

        - `str`: string ID of the tile
        '''
        if self.id == 0:
            return ""
        if self.id < 10:
            return str(self.id) + "m"
        elif self.id < 20:
            return str(self.id - 10) + "p"
        elif self.id < 30:
            return str(self.id - 20) + "s"
        elif self.id < 40:
            return str(self.id - 30) + "z"
        elif self.id == 51:
            return "0m"
        elif self.id == 52:
            return "0p"
        elif self.id == 53:
            return "0s"
        else:
            return "(invalid)"

    def __set_id_with_check(self, id: int) -> None:
        '''
        Method: __set_id

        ## Description

        Sets the ID of the tile.

        ## Parameters

        - `id`: ID of the tile
        '''
        assert isinstance(id, int), "id must be an integer"
        if id in self.valid_id:
            self.id = id
        else:
            raise ValueError("Invalid ID")

    def get_id(self) -> int:
        '''
        Method: get_id

        ## Description

        Returns the ID of the tile.

        ## Returns

        - `int`: ID of the tile
        '''
        return self.id
    
    def get_rank(self) -> int:
        '''
        Method: get_rank

        ## Description

        Returns the rank of the tile.

        ## Returns

        - `int`: rank of the tile
        '''
        if self.id > 50:
            return 5
        return self.id % 10
    
    def get_suit(self) -> str:
        '''
        Method: get_suit

        ## Description

        Returns the suit of the tile.

        ## Returns

        - `str`: suit of the tile
        '''
        if self.id == 0:
            return ""
        if self.id < 10 or self.id == 51:
            return "m"
        elif self.id < 20 or self.id == 52:
            return "p"
        elif self.id < 30 or self.id == 53:
            return "s"
        elif self.id < 40:
            return "z"

    def get_name(self) -> str:
        '''
        Method: get_name

        ## Description

        Returns the name of the tile.

        ## Returns

        - `str`: name of the tile
        '''
        return self.__id_to_str()
    
    def copy(self):
        '''
        Method: copy

        ## Description

        Returns a copy of the tile.

        ## Returns

        - `tile`: copy of the tile
        '''
        return Tile(self)

    def __eq__(self, other):
        '''
        Method: __eq__

        ## Description

        Returns whether the tile is equal to another tile.
        Compares only the ID. Comparing against non-tile objects
        will always return `False`.

        ## Parameters

        - `other`: tile to compare

        ## Returns

        - `bool`: whether the tile is equal to the other tile
        '''
        return isinstance(other, Tile) and self.id == other.id
    
    def __ne__(self, other):
        '''
        Method: __ne__

        ## Description

        Negates the result of `__eq__`.

        ## Parameters

        - `other`: tile to compare

        ## Returns

        - `bool`: whether the tile is not equal to the other tile
        '''
        return not self.__eq__(other)
    
    def __lt__(self, other):
        '''
        Method: __lt__

        ## Description

        Returns whether the tile ID is smaller than another tile.
        Compares only the ID. Comparing against non-tile objects
        will raise TypeError.

        ## Parameters

        - `other`: tile to compare

        ## Returns

        - `bool`: whether the tile is less than the other tile
        '''
        if not isinstance(other, Tile):
            raise TypeError("Cannot compare tile with non-tile object")
        return self.id < other.id
    
    def __gt__(self, other):
        '''
        Method: __gt__

        ## Description

        Negates the result of `__lt__`.

        ## Parameters

        - `other`: tile to compare

        ## Returns

        - `bool`: whether the tile is greater than the other tile
        '''
        return not self.__lt__(other)

    def __le__(self, other):
        '''
        Method: __le__

        ## Description

        Returns whether the tile ID is smaller or equal to another tile.
        Compares only the ID. Comparing against non-tile objects will
        raise TypeError.

        ## Parameters

        - `other`: tile to compare

        ## Returns

        - `bool`: whether the tile is less than or equal to the other tile
        '''
        return self.__lt__(other) or self.__eq__(other)
    
    def __ge__(self, other):
        '''
        Method: __ge__

        ## Description

        Returns whether the tile ID is smaller or equal to another tile.
        Compares only the ID. Comparing against non-tile objects will
        raise TypeError.

        ## Parameters

        - `other`: tile to compare

        ## Returns

        - `bool`: whether the tile is greater than or equal to the other tile
        '''
        return self.__gt__(other) or self.__eq__(other)
    
    def __str__(self):
        '''
        Method: __str__

        ## Description

        Returns the string representation of the tile.

        ## Returns

        - `str`: string representation of the tile
        '''
        return self.__id_to_str()
    
    def __repr__(self):
        '''
        Method: __repr__

        ## Description

        Returns the string representation of the tile. This method
        follows the rule of `eval(repr(tile)) == tile`.

        ## Returns

        - `str`: string representation of the tile
        '''
        return "tile(" + str(self.id) + ")"

    def __hash__(self):
        '''
        Method: __hash__

        ## Description

        Returns the hash of the tile.

        ## Returns

        - `int`: hash of the tile
        '''
        return hash(self.id + self.hidden_id)
    

