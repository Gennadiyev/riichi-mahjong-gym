import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.utils import get_value
from env.deck import Deck
from env.tiles import Tile

# def shanten_test():
#     deck = Deck("114477m225588s15z")
#     assert shanten_count(deck) == 0
#     deck_2 = Deck("147m258p369s1234z")
#     assert shanten_count(deck_2) == 6
#     deck_3 = Deck("19m19p019s123444z")
#     assert shanten_count(deck_3) == 2
#     deck_4 = Deck("11223344556s")
#     assert shanten_count(deck_4) == 0

# print(Deck("123s354s678p99m406p").get_short_string())
# input()
# agari_output = get_value(Deck("123s304s678p99m406p"), Tile("4p"), is_tsumo=True)
# agari_output = get_value(Deck("55z111z222z333z444z"), Tile("5z"), melds=["a41414141", "a42424242", "a43434343", "a44444444"], is_tsumo=True, is_tenhou=True, )
agari_output = get_value(Deck("234m234s456p567m66p"), Tile("5m"), melds=["c121314"], is_tsumo=True)
# agari_output = get_value(Deck("123m123p123123s99m"), Tile("1s"))
# agari_output = get_value(Deck("111m222m333m444m55m"), Tile("5m"))
# agari_output = get_value(Deck("123m123m123p123p99s"), Tile("1m"))
print(agari_output)
print("{} 番 {} 符，{} 点".format(agari_output.han, agari_output.fu, agari_output.cost['main']))
print("役：{}".format(", ".join([str(yaku) for yaku in agari_output.yaku])))

# from mahjong.tile import TilesConverter

# tiles_converter = TilesConverter()
# print(tiles_converter.one_line_string_to_136_array(Deck("12355m123p011224s").get_short_string(), has_aka_dora=True))
