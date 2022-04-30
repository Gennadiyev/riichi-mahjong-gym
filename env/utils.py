'''
File: utils.py
Author: Kunologist
Description:
    Utilities used for other modules.
'''

from numpy import isin


def han_calculator(deck) -> int:
    '''
    Function: han_calculator(deck: `list`) -> `int`
 
    ## Description

    Calculates the number of han of a given deck.
 
    ## Parameters
    
    - `deck`: `Deck`
        The target deck.
 
    ## Returns
    
    `int`
        The number of han of the given deck.
    '''
    pass

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

    if len(calls) != 0 and not all(call.find("a") != -1 for call in calls):
        return False
    else:
        reach_discard = []
        all_valid_tile_id = [11, 12, 13, 14, 15, 16, 17, 18, 19,
            21, 22, 23, 24 ,25, 26, 27, 28, 29,
            31, 32, 33, 34, 35, 36, 37, 38, 39,
            41, 42, 43, 44, 45, 46, 47, 48, 49,
            51, 52, 53
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
            return True

    # Kokushi mosou
    kokushi_mosou_deck = Deck("1m9m1p9p1s9s1234567z")
    if len(deck - kokushi_mosou_deck) == 1 and (deck.get_tiles()[0].get_suit() == "z" or deck.get_tiles()[0].get_rank() == 1 or deck.get_tiles()[0].get_rank() == 9):
        return True
    
    # Chiitoitsu
    chiitoitsu = True
    if len(deck_list) == 14:
        for tile in deck_list:
            if deck_list.count(tile) != 2:
                # Chiitoitsu shall not have 4 of a kind
                chiitoitsu = False
                break
        if chiitoitsu:
            return True
    
    return False
