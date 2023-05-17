import math

from src.agent import Agent
from src.states import Action, State

class MinimaxAgent(Agent):
    def __init__(self, max_depth: int = 0, use_alpha_beta: bool = False):
        super().__init__(max_depth)
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, state: State) -> Action:
        if self.use_alpha_beta:
            best_action, _ = self._alpha_beta(state, self.max_depth)
        else:
            best_action, _ = self._minimax(state, self.max_depth)
        return best_action

    def _alpha_beta(self, state: State, depth: int, alpha: float = -math.inf, beta: float = math.inf, is_max_player: bool = True) -> tuple[Action, float]:
        if depth == 0 or state.is_terminal():
            return None, (state.get_value() if is_max_player else -state.get_value())
        
        best_action = value = None
        if is_max_player:
            value = -math.inf
            for action in state.generate_actions():
                child = state.get_next_state(action)
                _, child_value = self._alpha_beta(child, depth - 1, alpha, beta, not is_max_player)
                if child_value > value:
                    best_action, value = action, child_value
                
                if value >= beta:
                    break
                alpha = max(alpha, value)
        else:
            value = math.inf
            for action in state.generate_actions():
                child = state.get_next_state(action)
                _, child_value = self._alpha_beta(child, depth - 1, alpha, beta, not is_max_player)
                if child_value < value:
                    best_action, value = action, child_value
                
                if value <= alpha:
                    break
                beta = min(beta, value)
        return best_action, value

    def _minimax(self, state: State, depth: int, is_max_player: bool = True) -> tuple[Action, float]:
        if depth == 0 or state.is_terminal():
            return None, (state.get_value() if is_max_player else -state.get_value())
        
        best_action = value = None
        if is_max_player:
            value = -math.inf
            for action in state.generate_actions():
                child = state.get_next_state(action)
                _, child_value = self._minimax(child, depth - 1, not is_max_player)
                if child_value <= value:
                    continue
                best_action, value = action, child_value
        else:
            value = math.inf
            for action in state.generate_actions():
                child = state.get_next_state(action)
                _, child_value = self._minimax(child, depth - 1, not is_max_player)
                if child_value >= value:
                    continue
                best_action, value = action, child_value
        return best_action, value

    def __str__(self):
        return "Minimax" + (' with alpha-beta pruning' if self.use_alpha_beta else '')
