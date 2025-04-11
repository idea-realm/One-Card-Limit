# strategy/base_strategy.py
import random
import pickle
from pathlib import Path
from typing import Dict
from ..core.action import Action
from ..core.state import HandState, GameConfig
from ..core.game_logic import get_valid_actions
from .game_tree import build_game_tree
from .info_set import InfoState, get_info_state

class Strategy:
    def __init__(self, config: GameConfig, policy: Dict[InfoState, Dict[Action, float]] = None):
        self.config = config
        if policy is None:
            self.generate_random_policy()
        else:
            self.policy = policy

    def get_action(self, state: HandState) -> Action:
        # Get the info state for the acting player
        info_state = get_info_state(state, state.acting_pos)
        
        # Get the action probabilities for this info state
        action_probs = self.policy[info_state]
        
        # Choose an action based on the probabilities
        return self.weighted_random_choice(action_probs)
    
    def generate_random_policy(self) -> None:
        self.policy = {}
        root = build_game_tree(self.config)
        for node in root:
            # For each node in the game tree check if it is a leaf node
            if node.is_leaf:
                continue
            for info_state in node.info_state:
                if info_state not in self.policy:
                    # Initialize policy for this info state with equal probabilities for all valid actions
                    actions = get_valid_actions(node.state)
                    self.policy[info_state] = {action: 1.0 / len(actions) for action in actions}     

    def get_strategy(self, info_state: InfoState) -> Dict[Action, float]:
        return self.policy[info_state]
    
    def show_strategy(self) -> str:
        for info_state, action_probs in self.policy.items():
            print(info_state, action_probs)

    @staticmethod
    def weighted_random_choice(action_probs: dict[Action, float]) -> Action:
        rnd = random.random()
        cumulative = 0.0
        for action, prob in action_probs.items():
            cumulative += prob
            if rnd < cumulative:
                return action
        return list(action_probs.keys())[-1]

    def save(self, filepath: str) -> None:
        """
        Save strategy to a file.
        
        Args:
            filepath: Path where to save the strategy
        """
        data = {
            'config': self.config,
            'policy': self.policy
        }
        
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filepath: str) -> 'Strategy':
        """
        Load strategy from a file.
        
        Args:
            filepath: Path to the saved strategy file
            
        Returns:
            Strategy object with loaded policy
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        return cls(config=data['config'], policy=data['policy'])

