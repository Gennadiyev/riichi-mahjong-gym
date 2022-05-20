import os
from re import A
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.tiles import Tile

def test_tiles_basic():
    tile = Tile(15)
    assert tile
    another_tile = Tile("5m")
    assert another_tile
    assert tile == another_tile
    assert tile.__str__() == "5m"

def test_tiles_unicode():
    assert Tile(33).get_unicode_tile() == "🀒"
    assert Tile("5z").get_unicode_tile() == "🀆"
