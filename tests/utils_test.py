import os
import sys


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.deck import Deck
from env.tiles import Tile
from env.utils import check_agari, check_reach, check_tenpai

# Agari test

def test_kokushi_mosou():
    kokushi_mosou_deck = Deck("1m9m1p9p11s9s1234567z")
    assert check_agari(kokushi_mosou_deck, [])

def test_chiitoitsu():
    chiitoitsu_deck = Deck("44m77m11p88p99p55z66z")
    assert check_agari(chiitoitsu_deck, [])

def test_no_agari():
    no_agari_deck = Deck("147m258p369s3456z")
    assert not check_agari(no_agari_deck, [])
    no_agari_deck_winds = Deck("11223399s123p345z")
    assert not check_agari(no_agari_deck_winds, [])
    no_agari_deck_not_full = Deck("123s455p56m")
    assert not check_agari(no_agari_deck_not_full, ["4242p42"])
    no_agari_deck_not_full_again = Deck("3s1p")
    assert not check_agari(no_agari_deck_not_full_again, ["4242p42", "c151617", "c171819", "c373839"])

def test_agari():
    agari_deck = Deck("123m456p789s11z")
    assert check_agari(agari_deck, [])
    agari_deck_1 = Deck("11123456789999m")
    assert check_agari(agari_deck_1, [])
    agari_deck_2 = Deck("223344m667788p66z")
    assert check_agari(agari_deck_2, [])
    agari_deck_3 = Deck("11112345678999p")
    assert check_agari(agari_deck_3, [])
    agari_deck_4 = Deck("11122233344455m")
    assert check_agari(agari_deck_4, [])
    agari_deck_5 = Deck("233444556p11122z")
    assert check_agari(agari_deck_5, [])
    agari_deck_6 = Deck("789p2267s0s")
    assert check_agari(agari_deck_6, ["c262524", "c373638"])
    agari_deck_7 = Deck("55z")
    assert check_agari(agari_deck_7, ["ak111z", "ak222z", "ak333z", "ak444z"])

test_agari()
# Riichi test

def test_riichi():
    riichi_deck = Deck("5056p06777s456m4s7m")
    assert check_reach(riichi_deck)
    riichi_deck_2 = Deck("19m19p19s1234567z4m")
    assert check_reach(riichi_deck_2)
    riichi_deck_3 = Deck("19m19p19s12345667z")
    assert len(check_reach(riichi_deck_3)) == 14
    riichi_deck_4 = Deck("4455m1166p205669s")
    assert Tile("9s") in Deck(check_reach(riichi_deck_4))

def test_no_riichi():
    no_riichi_deck = Deck("123s456p788m11223z")
    assert not check_reach(no_riichi_deck)
    no_riichi_deck_2 = Deck("123s456p788m11z")
    assert not check_reach(no_riichi_deck_2, ["33p3333"])
    no_riichi_deck_3 = Deck("19m19p19s12345667z")

def test_riichi_with_ankan():
    riichi_deck = Deck("123s456p788m11z")
    assert Tile("7m") in check_reach(riichi_deck, ["333333a33"])
    riichi_deck_1 = Deck("123s456p259m11z")
    assert not check_reach(riichi_deck_1, ["333333a33"])

# Tenpai

def test_tenpai():
    no_tenpai_deck = Deck("123s456p777m1123z")
    assert not check_tenpai(no_tenpai_deck)
    tenpai_deck = Deck("1112345678999m")
    assert check_tenpai(tenpai_deck)
    tenpai_deck_2 = Deck("223344m667788p6z")
    assert check_tenpai(tenpai_deck_2)
    tenpai_deck_3 = Deck("88m23344556s111z")
    assert check_tenpai(tenpai_deck_3)

test_riichi_with_ankan()
