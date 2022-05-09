import os
import sys


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(0, parent)

from env.mahjong import MahjongGame
from env.ruleset import Ruleset
from env.player import Player
from env.flask_agent import FlaskAgent
from env.agent import Agent

ruleset = Ruleset()
# Random seed is miku's color
seed = 34900
game = MahjongGame(ruleset, random_seed=seed)

# flask_agent = FlaskAgent('Flask Agent')
# flask_player = Player('Flask Player', agent=flask_agent)
# game.set_player(0, flask_player)
random_agent = Agent("random_1")
random_player = Player("random_1", agent=random_agent)
game.set_player(0, random_player)
random_agent = Agent("random_3")
random_player = Player("random_3", agent=random_agent)
game.set_player(1, random_player)
random_agent = Agent("random_4")
random_player = Player("random_4", agent=random_agent)
game.set_player(3, random_player)
game.initialize_game()
game.play()

