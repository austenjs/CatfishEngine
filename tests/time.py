import os
from pathlib import Path
import sys
import time

sys.path.append(os.path.join(Path(os.path.dirname(__file__)).parents[0]))

from src.states import SimpleNim
from src.agent import Agent, MinimaxAgent, NegamaxAgent

SMALL_GAMESPACE = SimpleNim(10)
BIG_GAMESPACE = SimpleNim(30)
PLAYERS = [MinimaxAgent(30, use_alpha_beta=False),
           MinimaxAgent(30, use_alpha_beta=True),
           NegamaxAgent(30, use_alpha_beta=False),
           NegamaxAgent(30, use_alpha_beta=True)]

def test_player_time(player: Agent):
    start = time.time()
    _ = player.get_move(SMALL_GAMESPACE)
    print(f'{player} in a small game space makes a move in {time.time() - start}s')

    start = time.time()
    _ = player.get_move(BIG_GAMESPACE)
    print(f'{player} in a big game space makes a move in {time.time() - start}s')

if __name__ == '__main__':
    for player in PLAYERS:
        test_player_time(player)
