from __future__ import annotations
from typing import Any, List

class Action:
    def __init__(self, encoded_action: Any):
        self.encoded_action = encoded_action
    
    def get_encoded_action(self) -> Any:
        return self.encoded_action
    
    def __str__(self):
        return str(self.encoded_action)
    
    def __eq__(self, __value: Action) -> bool:
        return self.encoded_action == __value.encoded_action

class State:
    def __init__(self):
        pass

    def _is_valid_state(self) -> bool:
        pass

    def generate_actions(self) -> List[Action]:
        pass

    def get_next_state(self, action: Action) -> State:
        pass

    def get_value(self) -> float:
        pass

    def is_terminal(self) -> bool:
        pass

    def generate_random_move(self) -> Action:
        pass
