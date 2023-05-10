import math

from src.agent import Agent
from src.states import Action, State

class NegamaxAgent(Agent):
    def get_move(self, state: State) -> Action:
        best_action, _ = self._negamax(state, self.max_depth)
        return best_action

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
        return "Negamax"
