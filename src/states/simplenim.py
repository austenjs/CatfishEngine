import math
import random
from typing import List

from src.states.state import Action, State

class SimpleNim(State):
    def __init__(self, num_objects: int = 10):
        self.num_objects = num_objects

    def _is_valid_state(self) -> bool:
        return self.num_objects >= 0

    def generate_actions(self) -> List[Action]:
        actions = []
        for num_to_remove in range(1, 3):
            action = Action(num_to_remove)
            if not self.get_next_state(action):
                break
            actions.append(action)
        return actions

    def get_next_state(self, action: Action) -> State:
        new_state = SimpleNim(self.num_objects - action.get_encoded_action())
        if not new_state._is_valid_state():
            return None
        return new_state

    def get_value(self) -> float:
        if self.num_objects == 0:
            return 1
        elif self.num_objects == 1:
            return -1
        
        return 0
    
    def is_terminal(self) -> bool:
        return self.num_objects == 0
    
    def generate_random_move(self) -> Action:
        if self.num_objects <= 1:
            return Action(self.num_objects)
        
        return Action(random.randint(1, 2))

    def __str__(self):
        return f'[Simple NIM] {self.num_objects} remaining.'
