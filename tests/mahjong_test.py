import os
import sys


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.mahjong import MahjongGame
from env.ruleset import Ruleset

ruleset = Ruleset()

game = MahjongGame(ruleset, random_seed=0x66ccff)

game.initialize_game()
game.play()
