import math

from src.agent import Agent
from src.states import Action, State

class MinimaxAgent(Agent):
    def get_move(self, state: State) -> Action:
        best_action, _ = self._minimax(state, self.max_depth)
        return best_action

    def _minimax(self, state: State, depth: int, max_player: bool = True) -> tuple[Action, float]:
        if depth == 0 or state.is_terminal():
            return None, (state.get_value() if max_player else -state.get_value())
        
        best_action = value = None
        if max_player:
            value = -math.inf
            for action in state.generate_actions():
                child = state.get_next_state(action)
                _, child_value = self._minimax(child, depth - 1, not max_player)
                if child_value <= value:
                    continue
                best_action, value = action, child_value
        else:
            value = math.inf
            for action in state.generate_actions():
                child = state.get_next_state(action)
                _, child_value = self._minimax(child, depth - 1, not max_player)
                if child_value >= value:
                    continue
                best_action, value = action, child_value
        return best_action, value

    def __str__(self):
        return "Minimax"
