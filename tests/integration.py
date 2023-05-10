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

        self.minimax = MinimaxAgent(15)
        self.negamax = NegamaxAgent(15)
        self.random = RandomAgent()

    def test_deterministic(self):
        expectedActions1 = [Action(2), Action(2), Action(2)]
        expectedActions2 = [Action(1), Action(1), Action(1)]
        players = [self.minimax, self.negamax]
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
        # Testcase 1
        move = 0
        players = [self.minimax, self.negamax]
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

        # Testcase 2
        move = 0
        players = [self.minimax, self.random]
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

        # Testcase 3
        move = 0
        players = [self.negamax, self.minimax]
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

        # Testcase 4
        move = 0
        players = [self.negamax, self.random]
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
        # Testcase 1
        move = 0
        players = [self.minimax, self.negamax]
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

        # Testcase 2
        move = 0
        players = [self.negamax, self.minimax]
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

unittest.main()
