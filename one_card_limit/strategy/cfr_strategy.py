# strategy/cfr_strategy.py
"""
This module implements the Counterfactual Regret Minimization (CFR) algorithm for One Card Limit Poker. 
CFR is a game-theoretic approach used to compute optimal strategies in imperfect information games.
The `CFRStrategy` class can be instantiated with a `GameConfig` object and used to train and evaluate strategies.
"""

# Standard Imports 
from typing import Dict
# Local Imports
from .base_strategy import Strategy
from ..core.game_logic import Action, Card, GameConfig, HandState, InfoState

class CFRStrategy:
    """
    Implementation of Counterfactual Regret Minimization (CFR) for One Card Limit Poker.
    """
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.policy: Dict[InfoState, Dict[Action, float]] = {}
        self.regret_sum: Dict[InfoState, Dict[Action, float]] = {}
        self.strategy_sum: Dict[InfoState, Dict[Action, float]] = {}
        self.iterations = 0
        self.trained = False
    
    def train(self, iterations: int = 10000) -> Strategy:
        """
        Train the CFR strategy for the specified number of iterations.
        """
        print(f"Training CFR strategy for {iterations} iterations...")
        
        for i in range(iterations):
            self._cfr_iteration()
            self.iterations += 1
            
            # Progress reporting
            if (i + 1) % 1000 == 0:
                print(f"Completed {i + 1}/{iterations} iterations")
        
        # Update policy with the average strategy after training
        avg_strategy_dict = self.get_average_strategy()
        
        self.policy = avg_strategy_dict
        print(f"Training complete! Trained for {self.iterations} total iterations.")
        return Strategy(config=self.config, policy = self.policy)

    def _cfr_iteration(self) -> None:
        """
        Run one iteration of CFR training.
        """
        # Initialize reach probabilities for both players
        op_reach_prob = 1.0
        ip_reach_prob = 1.0
        
        # Create initial game state using factory method
        initial_state = HandState(self.config, deal_cards=True)
        
        # Run CFR recursion
        self._cfr_recursive(initial_state, op_reach_prob, ip_reach_prob)

    def _cfr_recursive(self, state: HandState, op_reach: float, ip_reach: float) -> Dict[int, float]:
        """ Recursive CFR implementation. Returns expected values for each player."""
        
        if state.is_over:
            # Terminal state, return utility values
            utilities = {
                i : state.stacks[i] 
                for i in [0, 1]
            }
            return utilities

        player = state.acting_pos
        info_state = state.get_info_state(state.acting_pos)
        
        # If this is a new info state, initialize policy
        if info_state not in self.policy:
            valid = info_state.valid_actions
            self.policy[info_state] = {action : 1/len(valid) for action in valid}
            
        if info_state not in self.regret_sum:
            self.regret_sum[info_state] = {
                action: 0.0 for action in self.policy[info_state].keys()
            }
            
        if info_state not in self.strategy_sum:
            self.strategy_sum[info_state] = {
                action: 0.0 for action in self.policy[info_state].keys()
            }
        
        # Get current strategy through regret matching
        strategy = self.get_strategy(info_state)
        
        # Initialize action values and node value
        action_values: Dict[Action, float] = {}
        node_value = {0: 0.0, 1: 0.0}  # Expected value for each player
        
        # Recursively evaluate each action
        for action in self.policy[info_state].keys():
            # Create new state after taking action
            new_state = state.clone()
            new_state.process_action(action)
            
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
        cards = [None, None]
        cards[position] = card
        
        for _ in range(iterations):
            # Create new hand with the specified card and position
            state = HandState.from_cards(self.config, cards)
            
            # Get values using current strategy
            values = self._cfr_recursive(state, 1.0, 1.0)
            ev += values[position]
            
        return ev / iterations

    def calculate_ev_matrix(self) -> Dict[str, Dict[Card, float]]:
        """
        Calculate EV matrix for all possible starting hands and positions.
        """
        ev_matrix = {
            'OP': {},
            'IP': {}
        }
        
        deck = self.config.get_deck()
        # Generate all possible cards in the deck
        for card in deck:
            ev_matrix['OP'][card] = self.calculate_ev(card, 0)
            ev_matrix['IP'][card] = self.calculate_ev(card, 1)
            
        return ev_matrix
    
    def update_regrets(self, info_state: InfoState, action: Action, regret: float) -> None:
        """
        Update regret sums and strategy sums for the given info state and action.
        
        Args:
            info_state: The information state
            action: The action taken
            regret: The counterfactual regret value
        """
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
        """
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

    def get_average_strategy(self) -> Dict[InfoState, Dict[Action, float]]:
        """
        Get the average strategy across all iterations.
        """
        avg_strategy = {}
        
        for info_state, strategy_sum in self.strategy_sum.items():
            avg_strategy[info_state] = {}
            normalizing_sum = sum(strategy_sum.values())
            
            if normalizing_sum > 0:
                for action, sum_prob in strategy_sum.items():
                    avg_strategy[info_state][action] = sum_prob / normalizing_sum
            
            else:
                # If no accumulated strategy (shouldn't happen), use uniform
                action_count = len(self.policy[info_state])
                for action in self.policy[info_state].keys():
                    avg_strategy[info_state][action] = 1.0 / action_count
        
        return avg_strategy