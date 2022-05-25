'''
File: action.py
Author: Kunologist
Description:
    Action for the game of mahjong. This class is just for
    representation, and does not contain any logic.
'''

class Action:

    def __init__(self, action_type: str, action_string: str = ""):
        '''
        Constructor: __init__
        
        ## Description
        
        The constructor of the Action class.
        
        ## Parameters
        
        - `action_type`: `str`
            The type of the action.
        - `action_string`: `str`
            The string representation of the action.
        
        ## Details

        Here is the list of possible action types:

        - `noop` (no operation)
        - `akan`
        - `mkan`
        - `kan`
        - `chii`
        - `pon`
        - `discard`
        - `replace`
        - `reach`
        - `ron`
        - `tsumo`
        - `ten`
        - `noten`

        The action string notation is as follows:

        ### `akan`

        Concealed quad (ankan, 暗槓).

        E.g. `"121212a12"` (ankan of 2m)

        The `"a"` is always placed before the 4-th tile.

        ### `mkan`

        Exposed quad (minkan, 明槓).

        E.g. `"121212m12"` (minkan of 2m)

        The `"m"` is put where the tile is called. Placing
        before the 3-rd tile means calling from the next player.

        ### `kan`

        Late kan (kakan, 加槓).

        E.g. `"47k474747"` (kakan of 7z)

        The `"k"` is placed where the tile is previously called
        pon. Placing before the 2-nd tile means that the tile
        is previously pon-ed from the opposing player.

        ### `chii`

        Call for sequence (chii, 吃).

        E.g. `"c275226"` (chii of dora 7p with 5p and 6p in hand)

        The `"c"` is always placed before the first tile since
        we only chii from the previous player.

        ### `pon`

        Call for pon (pon, 碰).

        E.g. `"41p4141"` (pon of 1z)

        The `"p"` is put before the called tile. Placing before
        the 2-nd tile means that the tile is pon-ed from the
        opposing player.

        ### `discard`

        Discard (discard, 捨てる). Discards the incoming tile.

        (no action string)

        ### `replace`

        Cut (切る).

        The action string should be the tile that is discarded.

        E.g. `"41"` (cut 1z from hand)

        ### `reach`

        Call reach (riichi, 立直).

        The action string should be the tile that is discarded.
        This action also calls reach.

        E.g. `"r51"` (riichi with 0m)
        `"r60"` (richii with discard)

        ### `ron`

        Call ron (ron, ロン).

        (no action string)

        ### `tsumo`

        Call tsumo (tsumo, ツモ).

        (no action string)

        ### `ten`

        Call ten (tenpai, 聴牌), i.e. the player has a waiting
        hand by the end of a game.

        (no action string)

        ### `noten`

        Call noten (noten, 不聴), i.e. the player does NOT
        have a waiting hand by the end of a game.

        (no action string) 
        '''
        self.action_type = action_type
        self.action_string = action_string
    
    def CHII(chii_string: str):
        '''
        Method: CHII
        
        ## Description
        
        This function returns a `CHII` action from the given
        tile id and chii string.
        
        ## Parameters
        
        - `chii_string`: `str`
            The string representation of the action.

        ## Returns

        A `chii` action.
        '''
        return Action("chii", chii_string)
    
    def PON(pon_string: str):
        '''
        Method: PON

        ## Description

        This function returns a `PON` action from the given
        pon string.

        ## Parameters

        - `pon_string`: `str`
            The string representation of the action.

        ## Returns

        A `pon` action.
        '''
        return Action("pon", pon_string)

    def KAN(pon_or_kan_string: str):
        '''
        Method: KAN
        
        ## Description
        
        This function returns a `KAN` action from the given
        pon string.
        
        ## Parameters
        
        - `pon_or_kan_string`: `str`
            The string representation of the pon / the string
            representation of the kan.

        ## Returns

        A `kan` action.
        '''
        if pon_or_kan_string.find("p") != -1:
            pon_or_kan_string.replace("p", "k")
            kan_string = pon_or_kan_string + pon_or_kan_string[-2:]
        elif pon_or_kan_string.find("k") != -1:
            kan_string = pon_or_kan_string
        else:
            raise ValueError("Invalid kan string: {}".format(pon_or_kan_string))
        return Action("kan", kan_string)

    def AKAN(tile_id: int or str):
        '''
        Method: AKAN
        
        ## Description
        
        This function returns an `AKAN` action from the given
        akan string.
        
        ## Parameters
        
        - `tile_id`: `int` / `str`
            The id of the tile. Not `"4s"` string!

        ## Returns

        An `akan` action.
        '''
        if tile_id % 10 == 5 and tile_id != 45:
            # The tile is a 5, and a dora will be involved
            if tile_id == 15:
                akan_string = "a15151551"
            elif tile_id == 25:
                akan_string = "a25252552"
            elif tile_id == 35:
                akan_string = "a35353553"
        else:
            akan_string = str(tile_id) * 3 + "a" + str(tile_id)
        return Action("akan", akan_string)

    def DISCARD():
        '''
        Method: DISCARD
        
        ## Description
        
        This function returns a `DISCARD` action.
        
        ## Returns

        A `discard` action.
        '''
        return Action("discard", "")
    
    def REPLACE(tile_id: int):
        '''
        Method: REPLACE
        
        ## Description
        
        This function returns a `REPLACE` action from the given
        tile id.
        
        ## Parameters
        
        - `tile_id`: `int`
            The id of the tile.

        ## Returns

        A `replace` action.
        '''
        return Action("replace", str(tile_id))

    def REACH(tile_id: int):
        '''
        Method: REACH
        
        ## Description
        
        This function returns a `REACH` action from the given
        tile id.
        
        ## Parameters
        
        - `tile_id`: `int`
            The id of the tile. If `tile_id` is `0` or `60`,
            the action means that the player calls reach upon
            discard

        ## Returns

        A `reach` action.
        '''
        if tile_id == 0:
            tile_id = 60
        return Action("reach", "r"+str(tile_id))

    def TSUMO():
        '''
        Method: TSUMO
        
        ## Description
        
        This function returns a `TSUMO` action.
        
        ## Returns

        A `tsumo` action.
        '''
        return Action("tsumo", "")

    def RON():
        '''
        Method: RON

        ## Description

        This function returns a `RON` action.

        ## Returns

        A `ron` action.
        '''
        return Action("ron", "")

    def NOOP():
        '''
        Method: NOOP
        
        ## Description
        
        This function returns a `NOOP` action.
        
        ## Returns

        A `noop` action.
        '''
        return Action("noop", "")
    
    def TEN():
        '''
        Method: TEN
        
        ## Description
        
        This function returns a `TEN` action.
        
        ## Returns

        A `ten` action.
        '''
        return Action("ten", "")
    
    def NOTEN():
        '''
        Method: NOTEN
        
        ## Description
        
        This function returns a `NOTEN` action.
        
        ## Returns

        A `noten` action.
        '''
        return Action("noten", "")
    
    def get_unicode_str(self):
        '''
        Method: get_unicode_str

        ## Description

        This function returns the unicode string representation
        of the action string.

        ## Returns

        A `str` representing the unicode string.
        '''
        from env.tiles import Tile
        # Extract digits from action string
        action_string = self.action_string
        digits = [int(ch) for ch in action_string if ch.isdigit()]
        for digit_idx in range(0, len(digits), 2):
            id = digits[digit_idx] * 10 + digits[digit_idx+1]
            if id == 0:
                break
            elif id == 60:
                id = 0
                break
            else:
                tile = Tile(id)
                action_string = action_string.replace(str(id), tile.get_unicode_tile())
        if self.action_type == "replace":
            return action_string
        else:
            return str(self.action_type) + " " + action_string

    def get_tiles(self):
        '''
        Method: get_tiles

        ## Description

        This function returns the tiles from the action string.

        ## Returns

        A `list` of `Tile` objects.
        '''
        from env.tiles import Tile
        # Extract digits from action string
        action_string = self.action_string
        digits = [int(ch) for ch in action_string if ch.isdigit()]
        tiles = []
        for digit_idx in range(0, len(digits), 2):
            id = digits[digit_idx] * 10 + digits[digit_idx+1]
            if id == 0:
                break
            elif id == 60:
                id = 0
                break
            else:
                tiles.append(Tile(id))
        return tiles

    def __str__(self):
        return str(self.action_type) + " " + str(self.action_string)
    
    def __repr__(self):
        return "Action('{}', '{}')".format(self.action_type, self.action_string)

    def to_json(self):
        return {
            "action_type": self.action_type,
            "action_string": self.action_string
        }

    def __eq__(self, other):
        return self.action_type == other.action_type and self.action_string == other.action_string
    
    def __hash__(self):
        return hash(self.action_type) * hash(self.action_string)
    
    def __neq__(self, other):
        return not self.__eq__(other)
