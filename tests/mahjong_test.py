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

def game_test():
    seed = 24
    game = MahjongGame(ruleset, wall="wall.json")
    random_agent_1 = Agent("random_1")
    random_player_1 = Player("random_1", agent=random_agent_1)
    random_agent_2 = Agent("random_2")
    random_player_2 = Player("random_2", agent=random_agent_2)
    random_agent_3 = Agent("random_3")
    random_player_3 = Player("random_3", agent=random_agent_3)
    random_agent_4 = Agent("random_4")
    random_player_4 = Player("random_4", agent=random_agent_4)
    game.set_player(0, random_player_1)
    game.set_player(1, random_player_2)
    game.set_player(2, random_player_3)
    # game.set_player(3, random_player_4)
    game.initialize_game()
    try:
        game.play()
    except:
        pass

game_test()
