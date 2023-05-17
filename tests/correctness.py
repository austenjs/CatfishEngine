import os
from pathlib import Path
import sys
import unittest

sys.path.append(os.path.join(Path(os.path.dirname(__file__)).parents[0]))

from src.states import Action, SimpleNim
from src.agent import RandomAgent, MinimaxAgent, NegamaxAgent

class TestAgentsOnSimpleGame(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.guarantee_lose_state = SimpleNim(10)
        self.guarantee_win_state = SimpleNim(9)

        self.players = [MinimaxAgent(15, use_alpha_beta=False),
                        MinimaxAgent(15, use_alpha_beta=True),
                        NegamaxAgent(15, use_alpha_beta=False),
                        NegamaxAgent(15, use_alpha_beta=True),
                        RandomAgent()]

    def test_deterministic(self):
        expectedActions1 = [Action(2), Action(2), Action(2)]
        expectedActions2 = [Action(1), Action(1), Action(1)]

        for i in range(len(self.players)):
            if type(self.players[i]) == RandomAgent:
                continue
            for j in range(len(self.players)):
                if type(self.players[j]) == RandomAgent:
                    continue

                players = [self.players[i], self.players[j]]
                for _ in range(100):
                    move = 0
                    state = self.guarantee_win_state
                    actions1 = []
                    actions2 = []
                    while not state.is_terminal():
                        player = players[move % 2]
                        action = player.get_move(state)
                        
                        # Player did not give a valid move
                        if action is None:
                            action = state.generate_random_move()
                        
                        if move == 0:
                            actions1.append(action)
                        else:
                            actions2.append(action)

                        state = state.get_next_state(action)
                        move = (move + 1) % 2
            self.assertTrue(all([actions1[i] == expectedActions1[i] for i in range(3)]), f"Agent {players[0]} is not detereministic despite exploring the entire state space!")
            self.assertTrue(all([actions2[i] == expectedActions2[i] for i in range(3)]), f"Agent {players[0]} is not detereministic despite exploring the entire state space!")

    def test_guarantee_win(self):
        for i in range(len(self.players)):
            if type(self.players[i]) == RandomAgent:
                continue
            for j in range(len(self.players)):
                players = [self.players[i], self.players[j]]
                move = 0
                state = self.guarantee_win_state
                while not state.is_terminal():
                    player = players[move % 2]
                    action = player.get_move(state)
                    
                    # Player did not give a valid move
                    if action is None:
                        action = state.generate_random_move()

                    state = state.get_next_state(action)
                    move = (move + 1) % 2
                self.assertEqual(move, 0, f"Agent {players[0]} does not play perfect moves!")

    def test_guarantee_lose(self):
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                if type(self.players[j]) == RandomAgent:
                    continue
                players = [self.players[i], self.players[j]]
                move = 0
                state = self.guarantee_lose_state
                while not state.is_terminal():
                    player = players[move % 2]
                    action = player.get_move(state)
                    
                    # Player did not give a valid move
                    if action is None:
                        action = state.generate_random_move()

                    state = state.get_next_state(action)
                    move = (move + 1) % 2
                self.assertEqual(move, 1, f"Agent {players[1]} does not play perfect moves!")

if __name__ == '__main__':
    unittest.main()
