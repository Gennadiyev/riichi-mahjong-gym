'''
File: utils.py
Author: Kunologist
Description:
    Utilities used for other modules.
'''

def han_calculator(deck: list) -> int:
    '''
    Function: han_calculator(deck: `list`) -> `int`
 
    ## Description

    Calculates the number of han of a given deck.
 
    ## Parameters
    
    - `deck`: `list`
        A list of tiles.
 
    ## Returns
    `int`
        The number of han of the given deck.
    '''
    han = 0
    for tile in deck:
        if tile.is_honor:
            han += 1
        elif tile.is_red:
            han += 2
        else:
            han += 1
    return han

