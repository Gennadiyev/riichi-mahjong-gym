'''
File: action.py
Author: Kunologist
Description:
    Action for the game of mahjong. This class is just for
    representation, and does not contain any logic.
'''

class Action:

    from env.mahjong import MahjongGame

    def __init__(self, action_type: str, action_string: str):
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

        Call ron (ron, 和了).

        (no action string)

        ### `tsumo`

        Call tsumo (tsumo, 自摸).

        (no action string)

        ### `ten`

        Call ten (tenpai, 聴牌), i.e. the player has a waiting
        hand by the end of a game.

        (no action string)

        ### `noten`

        Call noten (noten, ノーテン), i.e. the player does NOT
        have a waiting hand by the end of a game.

        (no action string) 
        '''
        self.action_type = action_type
        self.action_string = action_string
    
    def KAN(self, pon_string: str):
        '''
        Method: KAN
        
        ## Description
        
        This function returns a `KAN` action from the given
        pon string.
        
        ## Parameters
        
        - `pon_string`: `str`
            The string representation of the pon.

        ## Returns

        A `kan` action.
        '''
        pon_string.replace("p", "k")
        kan_string = pon_string + pon_string[-2:]
        return Action("kan", kan_string)

    def AKAN(self, tile_id: int):
        '''
        Method: AKAN
        
        ## Description
        
        This function returns an `AKAN` action from the given
        akan string.
        
        ## Parameters
        
        - `tile_id`: `int`
            The id of the tile.

        ## Returns

        An `akan` action.
        '''
        akan_string = str(id) * 3 + "a" + str(id)
        return Action("akan", akan_string)

    def DISCARD(self):
        '''
        Method: DISCARD
        
        ## Description
        
        This function returns a `DISCARD` action.
        
        ## Returns

        A `discard` action.
        '''
        return Action("discard", "")
    
    def REPLACE(self, tile_id: int):
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

    def REACH(self, tile_id: int):
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

    def TSUMO(self):
        '''
        Method: TSUMO
        
        ## Description
        
        This function returns a `TSUMO` action.
        
        ## Returns

        A `tsumo` action.
        '''
        return Action("tsumo", "")

    def __str__(self):
        return self.action_string
    
    def __repr__(self):
        return "Action({}, {})".format(self.action_type, self.action_string)