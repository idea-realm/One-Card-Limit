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
from typing import Dict, List, Tuple
from collections import defaultdict
# Local Imports
from ..core.state import Action, HandState, GameConfig
from ..core.game_logic import get_valid_actions
from .game_tree import build_game_tree
from .info_set import InfoState, get_info_state

class Policy:
    """
    Represents a policy mapping information states to action probabilities.
    Provides methods for displaying, accessing, and manipulating the policy.
    """
    def __init__(self, policy_dict: Dict[InfoState, Dict[Action, float]] = None):
        self._policy: Dict[InfoState, Dict[Action, float]] = policy_dict or {}
    
    def __getitem__(self, info_state: InfoState) -> Dict[Action, float]:
        """Get action probabilities for a given information state."""
        return self._policy[info_state]
    
    def __setitem__(self, info_state: InfoState, action_probs: Dict[Action, float]) -> None:
        """Set action probabilities for a given information state."""
        self._policy[info_state] = action_probs
    
    def __contains__(self, info_state: InfoState) -> bool:
        """Check if information state exists in policy."""
        return info_state in self._policy
    
    def __iter__(self):
        """Iterate over information states."""
        return iter(self._policy)
    
    def items(self):
        """Return items (info_state, action_probs) pairs."""
        return self._policy.items()
    
    def keys(self):
        """Return information states."""
        return self._policy.keys()
    
    def values(self):
        """Return action probability dictionaries."""
        return self._policy.values()
    
    def get(self, info_state: InfoState, default=None):
        """Get action probabilities with default fallback."""
        return self._policy.get(info_state, default)
    
    def to_dict(self) -> Dict[InfoState, Dict[Action, float]]:
        """Convert policy to dictionary format."""
        return self._policy.copy()
    
    @classmethod
    def from_dict(cls, policy_dict: Dict[InfoState, Dict[Action, float]]) -> 'Policy':
        """Create policy from dictionary."""
        return cls(policy_dict)
    
    def show(self, max_entries: int = None, sort_by_card: bool = True) -> None:
        """
        Display the policy in a readable format.
        
        Args:
            max_entries: Maximum number of entries to show (None for all)
            sort_by_card: Whether to sort by card value
        """
        print("=== Policy ===")
        
        # Sort info states for better readability
        sorted_items = sorted(
            self._policy.items(),
            key=lambda x: (str(x[0].card), x[0].actions) if sort_by_card else str(x[0])
        )
        
        if max_entries:
            sorted_items = sorted_items[:max_entries]
        
        for info_state, action_probs in sorted_items:
            action_str = ", ".join([
                f"{action.name}: {prob:.1%}" 
                for action, prob in action_probs.items()
            ])
            print(f"{info_state} -> {{{action_str}}}")
        
        if max_entries and len(self._policy) > max_entries:
            print(f"... and {len(self._policy) - max_entries} more entries")
    
    def show_by_card(self, card_filter: str = None) -> None:
        """
        Display policy grouped by card.
        
        Args:
            card_filter: Show only entries for this card (e.g., 'A', 'K')
        """
        print("=== Policy by Card ===")
        
        # Group by card
        by_card = defaultdict(list)
        for info_state, action_probs in self._policy.items():
            card_str = str(info_state.card)
            if card_filter is None or card_str == card_filter:
                by_card[card_str].append((info_state, action_probs))
        
        # Sort cards by value (high to low)
        card_ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        sorted_cards = sorted(by_card.keys(), key=lambda x: card_ranks.index(x) if x in card_ranks else 99)
        
        for card in sorted_cards:
            print(f"\n{card}:")
            # Sort by action sequence
            sorted_entries = sorted(by_card[card], key=lambda x: x[0].actions)
            for info_state, action_probs in sorted_entries:
                action_str = ", ".join([
                    f"{action.name}: {prob:.1%}" 
                    for action, prob in action_probs.items()
                ])
                actions_part = f"-{info_state.actions}" if info_state.actions else ""
                print(f"  {card}{actions_part} -> {{{action_str}}}")
    
    def get_action_summary(self) -> Dict[str, int]:
        """Get summary statistics about the policy."""
        total_states = len(self._policy)
        action_counts = defaultdict(int)
        
        for action_probs in self._policy.values():
            # Count the most likely action for each state
            best_action = max(action_probs.items(), key=lambda x: x[1])[0]
            action_counts[best_action.name] += 1
        
        return {
            'total_states': total_states,
            'action_distribution': dict(action_counts)
        }
    
    def __len__(self) -> int:
        """Return number of information states in policy."""
        return len(self._policy)
    
    def __str__(self) -> str:
        """String representation of policy."""
        return f"Policy({len(self._policy)} states)"
    
    def __repr__(self) -> str:
        return self.__str__()

class Strategy:
    def __init__(self, config: GameConfig, policy: Policy = None):
        self.config = config
        self.policy = policy or self._generate_random_policy()

    def get_action(self, state: HandState) -> Action:
        # Get the info state for the acting player
        info_state = get_info_state(state, state.acting_pos)
        
        # Get the action probabilities for this info state
        action_probs = self.policy[info_state]
        
        # Choose an action based on the probabilities
        return self.weighted_random_choice(action_probs)
    
    def _generate_random_policy(self) -> Policy:
        """Generate random policy (made private since it's internal)."""
        policy_dict = {}
        root = build_game_tree(self.config)
        for node in root:
            # For each node in the game tree check if it is a leaf node
            if node.is_leaf:
                continue
            for info_state in node.info_state:
                if info_state not in policy_dict:
                    # Initialize policy for this info state with equal probabilities for all valid actions
                    actions = get_valid_actions(node.state)
                    policy_dict[info_state] = {action: 1.0 / len(actions) for action in actions}
        
        return Policy(policy_dict)

    def get_strategy(self, info_state: InfoState) -> Dict[Action, float]:
        """Get strategy for specific info state."""
        return self.policy[info_state]
        
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
        """
        data = {
            'config': self.config,
            'policy': self.policy.to_dict()
        }
        
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filepath: str) -> 'Strategy':
        """
        Load strategy from a file.
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        policy = Policy.from_dict(data['policy'])
        return cls(config=data['config'], policy=policy)

    @classmethod
    def create_or_load(cls, config: GameConfig, strategy_type: str = "cfr", train_iterations: int = 10000) -> 'Strategy':
        """
        Factory method to create or load appropriate strategy.
        
        Args:
            config: Game configuration
            strategy_type: Type of strategy ("cfr" or "random")
            train_iterations: Number of iterations to train if creating new CFR strategy
        
        Returns:
            Strategy instance
        """
        if strategy_type == "cfr":
            try:
                from .cfr_strategy import CFRStrategy
                strategy_path = get_strategy_path(config)
                
                if strategy_path.exists():
                    print(f"Loading existing CFR strategy from {strategy_path}")
                    return CFRStrategy.load(strategy_path)
                else:
                    print(f"No trained CFR strategy found for {config}")
                    print(f"Training new CFR strategy with {train_iterations} iterations...")
                    
                    # Create and train new CFR strategy
                    cfr_strategy = CFRStrategy(config)
                    cfr_strategy.train(train_iterations)
                    
                    # Save the trained strategy
                    cfr_strategy.save(str(strategy_path))
                    print(f"Trained strategy saved to {strategy_path}")
                    
                    return cfr_strategy
                    
            except (ImportError, ModuleNotFoundError, pickle.UnpicklingError) as e:
                print(f"Error with CFR strategy: {e}")
                print("Using random strategy instead")
                return cls(config)
        else:
            return cls(config)

def get_strategy_path(config: GameConfig) -> Path:
    """
    Get path for trained strategies.
    """
    return Path(f"trained_strategies/cfr_strategy_d{config.deck_size}_r{config.max_raises}.pkl")

