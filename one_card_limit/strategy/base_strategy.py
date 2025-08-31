# one_card_limit\strategy\base_strategy.py
"""
This module defines the `Strategy` class, which represents a strategy for the One Card Limit Poker game. 
It includes methods for generating random strategies, retrieving actions based on the strategy, 
saving and loading strategies, and displaying the strategy.
"""

# Standard Imports
import random
import pickle
from pathlib import Path
from typing import Dict, List
# Local Imports
from ..core.game_logic import Action, HandState, GameConfig, InfoState, generate_all_handstates

class Strategy:
    def __init__(self, config: GameConfig, policy: Dict[InfoState, Dict[Action, float]] = None) -> None:
        self.config = config
        if policy is None:
            self.default_policy()
        else: 
            self.policy = policy
        
    def get_action(self, state: HandState) -> Action:
        # Return random choice if no policy
        if not self.policy:
            raise ValueError("No policy defined for strategy.")
        
        # Get the info state for the acting player
        info_state = state.get_info_state(state.acting_pos)
        
        # Get the action probabilities for this info state
        action_probs = self.policy[info_state]
        
        # Choose an action based on the probabilities
        return self.weighted_random_choice(action_probs)
    
    def get_strategy(self, info_state: InfoState) -> Dict[Action, float]:
        return self.policy[info_state]
   
    def show_policy(self) -> None:
        """Display the policy in a readable format"""
        print("=== Policy ===")
        
        # Sort info states for better readability
        sorted_items = sorted(
            self.policy.items(),
            key=lambda x: (str(x[0].card), str(x[0].actions))
        )
        
        
        for info_state, action_probs in sorted_items:
            action_str = ", ".join([
                f"{action.name}: {prob:.1%}" 
                for action, prob in action_probs.items()
            ])
            print(f"{info_state} -> {{{action_str}}}")
    
    def default_policy(self) -> None:
        """Initialize a default uniform random policy."""
        self.policy = {}
        all_handstates: List[HandState] = generate_all_handstates(self.config)
        for handstate in all_handstates:
            if handstate.is_over:
                continue
            info_state = handstate.get_info_state(handstate.acting_pos)
            valid_actions = handstate.get_valid_actions()
            prob = 1.0 / len(valid_actions)
            self.policy[info_state] = {action: prob for action in valid_actions}
     
    @staticmethod
    def weighted_random_choice(action_probs: dict[Action, float]) -> Action:
        rnd = random.random()
        cumulative = 0.0
        for action, prob in action_probs.items():
            cumulative += prob
            if rnd < cumulative:
                return action
        return list(action_probs.keys())[-1]
    
    def save(self, filepath: str = None) -> None:
        """Save strategy to a file."""
        data = {
            'config': self.config,
            'policy': self.policy
        }
        if filepath is None:
            filepath = f"trained_strategies/cfr_strategy_d{self.config.deck_size}_r{self.config.max_raises}.pkl"
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    @classmethod
    def load(cls, config: GameConfig) -> 'Strategy':
        """Create or load appropriate strategy."""
        try:
            strategy_path = Path(f"trained_strategies/cfr_strategy_d{config.deck_size}_r{config.max_raises}.pkl")
            if strategy_path.exists():
                print(f"Loading existing CFR strategy from {strategy_path}")
                with open(strategy_path, 'rb') as f:
                    data = pickle.load(f)
                    policy = data['policy']
                    return cls(config=data['config'], policy=policy)
            else:
                print(f"No trained strategy found for {config}")
                
        except (ImportError, ModuleNotFoundError, pickle.UnpicklingError) as e:
            print(f"Error with CFR strategy: {e}")
            print("Using random strategy instead")
            return cls(config)

