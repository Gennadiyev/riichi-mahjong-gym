import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.deck import Deck, Wall

# Deck test

def test_deck_basic():
    deck = Deck("19m19s19p1234567z7p")
    assert deck.__str__() == "1m9m1p7p9p1s9s1z2z3z4z5z6z7z"
    deck_ord = Deck("31m29s1p4m4z1z7m7z2m2m3m2p3z")
    assert deck_ord.__str__() == "1m2m2m3m3m4m7m1p2p2s9s1z3z4z7z"

def test_deck_empty():
    deck_empty = Deck()
    assert deck_empty.__str__() == ""
    assert deck_empty.get_unicode_str() == ""

# Wall test

def test_wall_1():
    from env.ruleset import Ruleset
    ruleset = Ruleset()
    wall = Wall(ruleset, 1)
    assert len(wall.get_mountain()) == 70
    assert len(wall.get_starting_hand(3)) == 13
