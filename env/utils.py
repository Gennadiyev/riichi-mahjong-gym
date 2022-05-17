'''
File: utils.py
Author: Kunologist
Description:
    Utilities used for other modules.
'''

from dataclasses import is_dataclass
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.shanten import Shanten

__shanten = Shanten()
__hand_calculator = HandCalculator()
__tiles_converter = TilesConverter()

def get_value(deck, incoming_tile, melds: list = [], game_state = None, ruleset = None, deduce: bool = False, **kwargs) -> int:
    '''
    Function: get_value(deck: `list`) -> `int`

    ## Description

    Returns the value of a given deck. This is a monster
    function.

    ## Parameters

    - `deck`: `Deck`
        The target deck.
    - `incoming_tile`: `Tile`
        The incoming tile.
    - `melds`: `list`
        The meld list.
    - `game_state`: `GameState`
        The game state. In addition to the default game.state, additional
        information (keys) must be provided:
        - `ron_or_tsumo_player_idx`: `int`
            The index of the player who won the ron or tsumo.
        - `ron_from_player_idx`: `int`
            If ron, the index of the player who gave the ron.
        - `is_tsumo`: `bool`
            Whether the game is tsumo.
        - `is_wall_empty`: `bool`
            Whether the wall is empty.
    - `ruleset`: `Ruleset`
        The ruleset.
    - `kwargs`:
        Additional arguments. See below.
        - is_tsumo = False
        - is_riichi = False
        - is_ippatsu = False
        - is_rinshan = False
        - is_chankan = False
        - is_haitei = False
        - is_houtei = False
        - is_daburu_riichi = False
        - is_nagashi_mangan = False
        - is_tenhou = False
        - is_renhou = False
        - is_chiihou = False
        - player_wind = None
        - round_wind = None
        - has_open_tanyao = False,
        - has_aka_dora = True,
        - has_double_yakuman = True,
        - kazoe_limit = `0 (HandConstants.KAZOE_LIMITED)`
            Can be set to `1 (HandConstants.KAZOE_SANBAIMAN)` or `2 (HandConstants.NO_LIMIT)`.
        - kiriage = False,
        - fu_for_open_pinfu = True,
        - fu_for_pinfu_tsumo = False,
        - renhou_as_yakuman = False,
        - has_daisharin = False,
        - has_daisharin_other_suits = False
    - deduce = False
        If `True`, the value of above flags will be deduced
        from the game state and ruleset.


    ## Returns

    Everything you should know about the deck.
    '''
    from env.deck import Deck
    from env.tiles import Tile
    assert isinstance(deck, Deck)
    assert isinstance(incoming_tile, Tile)
    assert isinstance(melds, list)

    tiles_136_array = __tiles_converter.one_line_string_to_136_array(deck.get_short_string(), has_aka_dora=True)
    win_tile = incoming_tile.get_136_id()

    # Create melds from call strings
    meld_objects = []
    for meld in melds:
        meld_deck = Deck()
        digits = [int(ch) for ch in meld if ch.isdigit()]
        for digit_idx in range(0, len(digits), 2):
            id = digits[digit_idx] * 10 + digits[digit_idx+1]
            tile = Tile(id)
            meld_deck.add_tile(tile)
        # meld is a call string
        if meld.find("c") != -1:
            # CHII
            c_index = meld.find("c")
            # The next two digits are the called tile
            called_tile_id = Tile(int(meld[c_index+1:c_index+3])).get_136_id()
            meld_object = Meld(
                meld_type=Meld.CHI,
                tiles=meld_deck.get_136_array(),
                opened=True,
                called_tile=called_tile_id
            )
            meld_objects.append(meld_object)
        elif meld.find("p") != -1:
            # PON
            p_index = meld.find("p")
            # The next two digits are the called tile
            called_tile_id = Tile(int(meld[p_index+1:p_index+3])).get_136_id()
            meld_object = Meld(
                meld_type=Meld.PON,
                tiles=meld_deck.get_136_array(),
                opened=True,
                called_tile=called_tile_id
            )
            meld_objects.append(meld_object)
        elif meld.find("k") != -1:
            # KAN (KAKAN)
            k_index = meld.find("k")
            # The next two digits are the called tile
            called_tile_id = Tile(int(meld[k_index+1:k_index+3])).get_136_id()
            meld_object = Meld(
                meld_type=Meld.KAN,
                tiles=meld_deck.get_136_array(),
                opened=True,
                called_tile=called_tile_id
            )
            meld_objects.append(meld_object)
        elif meld.find("a") != -1:
            # ANKAN
            a_index = meld.find("a")
            # The next two digits are the called tile
            called_tile_id = Tile(int(meld[a_index+1:a_index+3])).get_136_id()
            meld_object = Meld(
                meld_type=Meld.KAN,
                tiles=meld_deck.get_136_array(),
                opened=False
            )
            meld_objects.append(meld_object)
        elif meld.find("m") != -1:
            # MINKAN
            m_index = meld.find("m")
            # The next two digits are the called tile
            called_tile_id = Tile(int(meld[m_index+1:m_index+3])).get_136_id()
            meld_object = Meld(
                meld_type=Meld.KAN,
                tiles=meld_deck.get_136_array(),
                opened=True,
                called_tile=called_tile_id
            )
            meld_objects.append(meld_object)

    # Create config
    if deduce:
        # Deduce the results from the game_state and ruleset
        from env.mahjong import MahjongGame
        from env.ruleset import Ruleset
        assert isinstance(game_state, MahjongGame)
        assert isinstance(ruleset, Ruleset)
        # All the current options in ruleset does not affect options
        options = OptionalRules (
            has_open_tanyao=kwargs.get("has_open_tanyao", True),
            has_aka_dora=kwargs.get("has_aka_dora", True),
            has_double_yakuman=kwargs.get("has_double_yakuman", True),
            kazoe_limit=kwargs.get("kazoe_limit", 0),
            kiriage=kwargs.get("kiriage", False),
            fu_for_open_pinfu=kwargs.get("fu_for_open_pinfu", True),
            fu_for_pinfu_tsumo=kwargs.get("fu_for_pinfu_tsumo", False),
            renhou_as_yakuman=kwargs.get("renhou_as_yakuman", False),
            has_daisharin=kwargs.get("has_daisharin", False),
            has_daisharin_other_suits=kwargs.get("has_daisharin_other_suits", False),
        )
        # is_tsumo
        is_tsumo = game_state["is_tsumo"]
        # is_riichi
        is_riichi = game_state["reach"][game_state["ron_or_tsumo_player_idx"]]
        # is_ippatsu
        is_ippatsu = game_state["ippatsu"][game_state["ron_or_tsumo_player_idx"]]
        # is_rinshan
        is_rinshan = game_state["rinshan"]
        # is_chankan
        is_chankan = game_state["chankan"]
        # is_haitei
        is_haitei = game_state["is_wall_empty"] and game_state["is_tsumo"]
        # is_houtei
        is_houtei = game_state["is_wall_empty"] and not game_state["is_tsumo"]
        # is_daburu_riichi
        is_daburu_riichi = game_state["double_reach"][game_state["ron_or_tsumo_player_idx"]]
        # is_nagashi_mangan
        is_nagashi_mangan = game_state["is_nagashi_mangan"]
        # is_tenhou
        is_tenhou = (
            game_state["wind_e"] == game_state["ron_or_tsumo_player_idx"] and \
            sum(len(discards) for discards in game_state["discarded_tiles"]) == 0
        )
        # is_renhou
        is_renhou = False
        # is_chiihou
        is_chiihou = (
            sum(len(discards) for discards in game_state["discarded_tiles"]) == 0
        )
        # player_wind
        wind_e = game_state["wind_e"]
        player_wind = ["E", "S", "W", "N", "E", "S", "W", "N"][game_state["ron_or_tsumo_player_idx"] - wind_e + 4]
        # round_wind
        round_wind = game_state["wind"]
        config = HandConfig (
            is_tsumo         = is_tsumo,
            is_riichi        = is_riichi,
            is_ippatsu       = is_ippatsu,
            is_rinshan       = is_rinshan,
            is_chankan       = is_chankan,
            is_haitei        = is_haitei,
            is_houtei        = is_houtei,
            is_daburu_riichi = is_daburu_riichi,
            is_nagashi_mangan= is_nagashi_mangan,
            is_tenhou        = is_tenhou,
            is_renhou        = is_renhou,
            is_chiihou       = is_chiihou,
            player_wind      = player_wind,
            round_wind       = round_wind,
            options          = options
        )
    else:
        # Defaults or user-defined by kwargs
        options = OptionalRules (
            has_open_tanyao=kwargs.get("has_open_tanyao", True),
            has_aka_dora=kwargs.get("has_aka_dora", True),
            has_double_yakuman=kwargs.get("has_double_yakuman", True),
            kazoe_limit=kwargs.get("kazoe_limit", 0),
            kiriage=kwargs.get("kiriage", False),
            fu_for_open_pinfu=kwargs.get("fu_for_open_pinfu", True),
            fu_for_pinfu_tsumo=kwargs.get("fu_for_pinfu_tsumo", False),
            renhou_as_yakuman=kwargs.get("renhou_as_yakuman", False),
            has_daisharin=kwargs.get("has_daisharin", False),
            has_daisharin_other_suits=kwargs.get("has_daisharin_other_suits", False),
        )
        config = HandConfig (
            is_tsumo=kwargs.get('is_tsumo', False),
            is_riichi=kwargs.get('is_riichi', False),
            is_ippatsu=kwargs.get('is_ippatsu', False),
            is_rinshan=kwargs.get('is_rinshan', False),
            is_chankan=kwargs.get('is_chankan', False),
            is_haitei=kwargs.get('is_haitei', False),
            is_houtei=kwargs.get('is_houtei', False),
            is_daburu_riichi=kwargs.get('is_daburu_riichi', False),
            is_nagashi_mangan=kwargs.get('is_nagashi_mangan', False),
            is_tenhou=kwargs.get('is_tenhou', False),
            is_renhou=kwargs.get('is_renhou', False),
            is_chiihou=kwargs.get('is_chiihou', False),
            player_wind=kwargs.get('player_wind', None),
            round_wind=kwargs.get('round_wind', None),
            options=options
        )

    result = __hand_calculator.estimate_hand_value(tiles_136_array, win_tile, melds=meld_objects, config=config)
    return result

def shanten_count(deck) -> int:
    '''
    Function: shanten_count(deck: `list`) -> `int`

    ## Description

    Calculates the shanten count of a given deck.

    ## Parameters

    - `deck`: `Deck`
        The target deck.

    ## Returns

    `int`
        The shanten count of the hand
    '''
    raise NotImplementedError("Shanten counter has been deprecated.")
    from env.deck import Deck
    from env.tiles import Tile

    assert isinstance(deck, Deck)

    deck_short_string = deck.get_short_string()
    tiles_34_array = __tiles_converter.one_line_string_to_34_array(deck_short_string, has_aka_dora=True)

    result = __shanten.calculate_shanten(tiles_34=tiles_34_array)

    return result

def fu_count(deck, calls: list = []) -> int:
    '''
    Function: fu_count(deck: `list`) -> `int`

    ## Description

    Calculates the number of fu of a given deck.

    ## Parameters

    - `deck`: `Deck`
        The target deck.
    - `call`: `list`
        The call list.

    ## Returns

    `int`
        The number of fu of the given deck.
    '''
    return 20

def check_reach(deck, calls: list = []) -> bool or list:
    '''
    Function: check_reach(deck: `list`) -> `bool`
 
    ## Description

    Checks whether a given deck is tenpai on discard.
 
    ## Parameters
    
    - `deck`: `Deck`
        The target deck.
    - `call`: `list`
        The call list. If this list is not empty, no
        reach check will be performed (Ankan is an
        exception).
 
    ## Returns
    
    `bool` or `list`
        `False` if no such discarding hand exists, a
        `list` of `Tile` if such a hand exists.
    '''

    from env.deck import Deck
    from env.tiles import Tile
    
    assert isinstance(calls, list)
    
    if isinstance(deck, Deck):
        deck_list = deck.get_tiles()
    else:
        assert isinstance(deck, list)
        assert all(isinstance(tile, Tile) for tile in deck)
        deck_list = deck
    
    # Consider red dora as non-red ones
    deck_list = [Tile((tile.get_id() - 50) * 10 + 5) if tile.is_red_dora() else tile for tile in deck_list]
    
    if len(calls) != 0 and not all(call.find("a") != -1 for call in calls):
        return False
    else:
        reach_discard = []
        all_valid_tile_id = [11, 12, 13, 14, 15, 16, 17, 18, 19,
            21, 22, 23, 24 ,25, 26, 27, 28, 29,
            31, 32, 33, 34, 35, 36, 37, 38, 39,
            41, 42, 43, 44, 45, 46, 47, 48, 49
        ]
        all_tiles = [Tile(i) for i in all_valid_tile_id]
        for tile in deck_list:
            deck_remaining = Deck(deck_list.copy()) - tile
            for additional_tile in all_tiles:
                deck_tenpai = deck_remaining + additional_tile
                if check_agari(deck_tenpai, []):
                    reach_discard.append(tile)
                    break
        if len(reach_discard) == 0:
            return False
        else:
            return reach_discard

def check_tenpai(deck, calls: list = []) -> bool:
    '''
    Function: check_tenpai(deck: `list`) -> `bool`
 
    ## Description

    Checks whether a given deck is in tenpai state.
 
    ## Parameters
    
    - `deck`: `Deck`
        The target deck.
    - `call`: `list`
        The call list.
 
    ## Returns
    
    `bool`
        `True` if the deck is tenpai, `False` otherwise.
    '''
    from env.deck import Deck
    from env.tiles import Tile
    
    assert isinstance(calls, list)
    
    if isinstance(deck, Deck):
        deck_list = deck.get_tiles()
    else:
        assert isinstance(deck, list)
        assert all(isinstance(tile, Tile) for tile in deck)
        deck_list = deck

    all_valid_tile_id = [11, 12, 13, 14, 15, 16, 17, 18, 19,
        21, 22, 23, 24 ,25, 26, 27, 28, 29,
        31, 32, 33, 34, 35, 36, 37, 38, 39,
        41, 42, 43, 44, 45, 46, 47, 48, 49
    ]
    all_tiles = [Tile(i) for i in all_valid_tile_id]
    for tile in deck_list:
        deck_addition = Deck(deck_list.copy()) + tile
        if check_agari(deck_addition.get_tiles(), calls):
            return True
    return False


def check_agari(deck, calls: list = []) -> bool:
    '''
    Function: check_agari(deck: `list`) -> `bool`
 
    ## Description

    Checks whether a given deck is agari.
 
    ## Parameters
    
    - `deck`: `Deck` or `list` of `Tiles`
        The target deck.
 
    ## Returns
    
    `bool`
        Whether the given deck is in agari state.
    '''
    from env.deck import Deck
    from env.tiles import Tile
    
    assert isinstance(calls, list)
    
    # Get tile list
    if isinstance(deck, Deck):
        deck_list = deck.get_tiles()
    else:
        assert isinstance(deck, list)
        assert all(isinstance(tile, Tile) for tile in deck)
        deck_list = deck

    # Sort tile list
    deck_list.sort()
    # Consider red dora as non-red ones
    deck_list = [Tile((tile.get_id() - 50) * 10 + 5) if tile.is_red_dora() else tile for tile in deck_list]

    deck = Deck(deck_list)

    # Ordinary hand
    toitsu = []
    for tile in deck_list:
        if deck_list.count(tile) >= 2 and tile not in toitsu:
            toitsu.append(tile)

    def is_3_complete(deck_list_):
        deck_list = deck_list_.copy()
        if len(deck_list) == 0:
            return True
        else:
            tile = deck_list[0]
            if tile.get_suit() == "z":
                if deck_list.count(tile) != 3:
                    return False
                deck_list.remove(tile)
                deck_list.remove(tile)
                deck_list.remove(tile)
                return is_3_complete(deck_list)
            else:
                res = []
                if deck_list.count(tile) >= 3:
                    deck_list.remove(tile)
                    deck_list.remove(tile)
                    deck_list.remove(tile)
                    res.append(is_3_complete(deck_list))
                elif tile.get_rank() <= 7:
                    if deck_list.count(Tile(tile.get_id() + 1)) >= 1 and deck_list.count(Tile(tile.get_id() + 2)) >= 1:
                        deck_list.remove(tile)
                        deck_list.remove(Tile(tile.get_id() + 1))
                        deck_list.remove(Tile(tile.get_id() + 2))
                        res.append(is_3_complete(deck_list))
                return any(res)

    for toitsu_ in toitsu:
        check_deck_without_toitsu = Deck(deck_list) - Deck([toitsu_, toitsu_])
        if is_3_complete(check_deck_without_toitsu.get_tiles()):
            return True, "ordinary"

    # Kokushi mosou
    kokushi_mosou_tiles = Deck("1m9m1p9p1s9s1234567z").get_tiles()
    kokushi_mosou_flag = True
    tile_1_9_z = 0
    for tile in kokushi_mosou_tiles:
        if not tile in deck:
            kokushi_mosou_flag = False
            break
        else:
            tile_1_9_z += deck.get_tiles().count(tile)
    if kokushi_mosou_flag and tile_1_9_z == 14:
        return True, "kokushi_mosou"

    # Chiitoitsu
    chiitoitsu = True
    if len(deck_list) == 14:
        for tile in deck_list:
            if deck_list.count(tile) != 2:
                # Chiitoitsu shall not have 4 of a kind
                chiitoitsu = False
                break
        if chiitoitsu:
            return True, "chiitoitsu"
    
    return False
