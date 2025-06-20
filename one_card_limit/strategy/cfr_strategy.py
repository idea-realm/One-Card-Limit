# strategy/cfr_strategy.py
"""
This module implements the Counterfactual Regret Minimization (CFR) algorithm for One Card Limit Poker. 
CFR is a game-theoretic approach used to compute optimal strategies in imperfect information games.
The `CFRStrategy` class can be instantiated with a `GameConfig` object and used to train and evaluate strategies.
"""

# Standard Imports 
import pickle
from typing import Dict
from pathlib import Path
# Local Imports
from .base_strategy import Strategy, Policy
from .info_set import InfoState, get_info_state
from ..core.state import Action, Card, Deck, GameConfig, HandState
from ..core.game_logic import process_action, deal_cards

class CFRStrategy(Strategy):
    """
    Implementation of Counterfactual Regret Minimization (CFR) for One Card Limit Poker.
    """
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.regret_sum: Dict[InfoState, Dict[Action, float]] = {}
        self.strategy_sum: Dict[InfoState, Dict[Action, float]] = {}
        self.iterations = 0
    
    def train(self, iterations: int = 10000) -> None:
        """
        Train the CFR strategy for the specified number of iterations.
        Updates the policy with the average strategy after training.
        
        Args:
            iterations: Number of CFR iterations to run (default: 10000)
        """
        print(f"Training CFR strategy for {iterations} iterations...")
        
        for i in range(iterations):
            self._cfr_iteration()
            self.iterations += 1
            
            # Progress reporting
            if (i + 1) % 1000 == 0:
                print(f"Completed {i + 1}/{iterations} iterations")
        
        # Update policy with the average strategy after training
        self._update_policy_with_average_strategy()
        print(f"Training complete! Trained for {self.iterations} total iterations.")
        
    def _cfr_iteration(self) -> None:
        """
        Run one iteration of CFR training.
        """
        # Initialize reach probabilities for both players
        op_reach_prob = 1.0
        ip_reach_prob = 1.0
        
        # Create initial game state using factory method
        initial_state = HandState.create_new_hand(self.config)
        deal_cards(initial_state)
        
        # Run CFR recursion
        self._cfr_recursive(initial_state, op_reach_prob, ip_reach_prob)

    def _cfr_recursive(self, state: HandState, op_reach: float, ip_reach: float) -> Dict[int, float]:
        """
        Recursive CFR implementation.
        Returns expected values for each player.
        """
        if state.is_over:
            # Terminal state, return utility values
            utilities = {
                i : state.players[i].stack 
                for i in [0, 1]
            }
            return utilities

        player = state.acting_pos
        info_state = get_info_state(state, state.acting_pos)
        
        # Get current strategy through regret matching
        strategy = self.get_strategy(info_state)
        
        # Initialize action values and node value
        action_values: Dict[Action, float] = {}
        node_value = {0: 0.0, 1: 0.0}  # Expected value for each player
        
        # Recursively evaluate each action
        for action in self.policy[info_state].keys():
            # Create new state after taking action
            new_state = state.clone()
            process_action(new_state, action)
            
            # Update reach probabilities
            if player == 0:  # OP
                action_reach = op_reach * strategy[action]
                child_values = self._cfr_recursive(new_state, action_reach, ip_reach)
            else:  # IP
                action_reach = ip_reach * strategy[action]
                child_values = self._cfr_recursive(new_state, op_reach, action_reach)
            
            action_values[action] = child_values[player]
            for p in [0, 1]:
                node_value[p] += strategy[action] * child_values[p]

        # Compute counterfactual regrets and update
        if player == 0:
            reach_prob = ip_reach
        else:
            reach_prob = op_reach
            
        for action in action_values:
            regret = reach_prob * (action_values[action] - node_value[player])
            self.update_regrets(info_state, action, regret)
            
        return node_value

    def calculate_ev(self, card: Card, position: int) -> float:
        """
        Calculate expected value for a specific card and position.
        """
        ev = 0.0
        iterations = 1000  # Number of iterations for Monte Carlo simulation
        
        for _ in range(iterations):
            # Create new game state using factory method
            state = HandState.create_new_hand(self.config)
            
            # Deal card to player
            deck = Deck(self.config.deck_size)
            deck.shuffle()
            state.players[position].card = card
            deck.cards.remove(card)
            
            # Deal random card for opponent
            state.players[1 - position].card = deck.deal_card()
            
            # Get values using current strategy
            values = self._cfr_recursive(state, 1.0, 1.0)
            ev += values[position]
            
        return ev / iterations

    def calculate_ev_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate EV matrix for all possible starting hands and positions.
        """
        ev_matrix = {
            'OP': {},
            'IP': {}
        }
        
        deck = Deck(self.config.deck_size)
        for card in deck.cards:
            ev_matrix['OP'][str(card)] = self.calculate_ev(card, 0)
            ev_matrix['IP'][str(card)] = self.calculate_ev(card, 1)
            
        return ev_matrix
    
    def update_regrets(self, info_state: InfoState, action: Action, regret: float) -> None:
        """
        Update regret sums and strategy sums for the given info state and action.
        
        Args:
            info_state: The information state
            action: The action taken
            regret: The counterfactual regret value
        """
        # Initialize regret sum dictionary for new info states
        if info_state not in self.regret_sum:
            self.regret_sum[info_state] = {
                action: 0.0 for action in self.policy[info_state].keys()
            }
        
        # Initialize strategy sum dictionary for new info states
        if info_state not in self.strategy_sum:
            self.strategy_sum[info_state] = {
                action: 0.0 for action in self.policy[info_state].keys()
            }
        
        # Update regret sum
        self.regret_sum[info_state][action] += regret
        
        # Get current strategy for this info state
        strategy = self.get_strategy(info_state)
        
        # Update strategy sum - accumulate the current strategy
        for a, prob in strategy.items():
            self.strategy_sum[info_state][a] += prob

    def get_strategy(self, info_state: InfoState) -> Dict[Action, float]:       
        """
        Get current strategy for the given info state using regret matching.
        This is used during training and returns the current regret-matched strategy.
        """
        # If this is a new info state, return the policy's uniform strategy
        if info_state not in self.regret_sum:
            return self.policy[info_state]
        
        strategy = {}
        regret_sum = self.regret_sum[info_state]
        
        # Sum positive regrets
        normalizing_sum = 0
        for action in self.policy[info_state].keys():
            strategy[action] = max(0, regret_sum[action])
            normalizing_sum += strategy[action]
        
        # Normalize probabilities
        if normalizing_sum > 0:
            for action in strategy:
                strategy[action] /= normalizing_sum
        else:
            # If all regrets are negative or zero, use uniform strategy
            action_count = len(self.policy[info_state])
            for action in self.policy[info_state].keys():
                strategy[action] = 1.0 / action_count
        
        return strategy

    def _update_policy_with_average_strategy(self) -> None:
        """Update the policy with the average strategy computed from strategy_sum."""
        for info_state in self.policy.keys():
            if info_state in self.strategy_sum:
                strategy_sum = self.strategy_sum[info_state]
                normalizing_sum = sum(strategy_sum.values())
                
                if normalizing_sum > 0:
                    # Update policy with normalized average strategy
                    avg_strategy = {
                        action: sum_prob / normalizing_sum 
                        for action, sum_prob in strategy_sum.items()
                    }
                    self.policy[info_state] = avg_strategy
                # If normalizing_sum is 0, keep the existing uniform policy

    def get_average_strategy(self) -> Dict[InfoState, Dict[Action, float]]:
        """
        Get the average strategy across all iterations.
        This is mainly for compatibility and debugging purposes.
        """
        avg_strategy = {}
        
        for info_state in self.policy.keys():
            if info_state in self.strategy_sum:
                strategy_sum = self.strategy_sum[info_state]
                normalizing_sum = sum(strategy_sum.values())
                
                if normalizing_sum > 0:
                    avg_strategy[info_state] = {
                        action: sum_prob / normalizing_sum 
                        for action, sum_prob in strategy_sum.items()
                    }
                else:
                    # Use current policy if no accumulated strategy
                    avg_strategy[info_state] = self.policy[info_state].copy()
            else:
                # Use current policy if no strategy sum
                avg_strategy[info_state] = self.policy[info_state].copy()
        
        return avg_strategy

    def save(self, filepath: str) -> None:
        """
        Save CFR strategy to a file.
        """
        data = {
            'config': self.config,
            'policy': self.policy.to_dict(),
            'regret_sum': self.regret_sum,
            'strategy_sum': self.strategy_sum,
            'iterations': self.iterations
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filepath: str) -> 'CFRStrategy':
        """
        Load CFR strategy from a file.
        
        Args:
            filepath: Path to the saved strategy file
            
        Returns:
            CFRStrategy object with loaded state
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        strategy = cls(config=data['config'])
        strategy.policy = Policy.from_dict(data['policy'])
        strategy.regret_sum = data['regret_sum']
        strategy.strategy_sum = data['strategy_sum']
        strategy.iterations = data.get('iterations', 0)
        
        return strategy
