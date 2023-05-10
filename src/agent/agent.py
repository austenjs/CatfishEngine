from src.states import Action, State

class Agent:
    def __init__(self, max_depth: int = 0):
        self.max_depth = max_depth

    def get_move(self, state: State) -> Action:
        pass
