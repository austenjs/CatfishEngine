import math

from src.agent import Agent
from src.states import Action, State

class NegamaxAgent(Agent):
    def __init__(self, max_depth: int = 0, use_alpha_beta: bool = False):
        super().__init__(max_depth)
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, state: State) -> Action:
        if self.use_alpha_beta:
            best_action, _ = self._alpha_beta(state, self.max_depth)
        else:
            best_action, _ = self._negamax(state, self.max_depth)
        return best_action
    
    def _alpha_beta(self, state: State, depth: int, alpha: float = -math.inf, beta: float = math.inf, color: int = 1) -> tuple[Action, float]:
        if depth == 0 or state.is_terminal():
            return None, state.get_value()
        
        best_action = None
        value = -math.inf
        for action in state.generate_actions():
            child = state.get_next_state(action)
            _, child_value = self._alpha_beta(child, depth - 1, -beta, -alpha, -color)
            child_value = -child_value
            if child_value <= value:
                continue

            best_action, value = action, child_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        return best_action, value

    def _negamax(self, state: State, depth: int, color: int = 1) -> tuple[Action, float]:
        if depth == 0 or state.is_terminal():
            return None, state.get_value()
        
        best_action = None
        value = -math.inf
        for action in state.generate_actions():
            child = state.get_next_state(action)
            _, child_value = self._negamax(child, depth - 1, -color)
            child_value = -child_value
            if child_value <= value:
                continue
            best_action, value = action, child_value
        return best_action, value
    
    def __str__(self):
        return "Negamax" + (' with alpha-beta pruning' if self.use_alpha_beta else '')
