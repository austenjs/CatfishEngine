import random

from src.agent import Agent
from src.states import Action, State

class RandomAgent(Agent):
    def get_move(self, state: State) -> Action:
        return random.choice(state.generate_actions())
    
    def __str__(self):
        return "Random"
