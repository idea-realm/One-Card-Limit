# core/strategy.py
import random
from .action import Action
from .state import HandState

class Strategy:
    def __init__(self, policy: dict[HandState, dict[Action, float]] = {}):
        self.policy_dict = policy

    def get_action(self, state: HandState) -> Action:
        valid_actions = state.valid_actions

        if (state) not in self.policy_dict:
            return random.choice(valid_actions)

        action_probs = self.policy_dict[(state)]
        return self.weighted_random_choice(action_probs)
    
    @staticmethod
    def weighted_random_choice(action_probs: dict[Action, float]) -> Action:
        rnd = random.random()
        cumulative = 0.0
        for action, prob in action_probs.items():
            cumulative += prob
            if rnd < cumulative:
                return action
        return list(action_probs.keys())[-1]

