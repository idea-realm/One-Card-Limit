from typing import Optional
from ..core.state import GameConfig, HandState
from ..core.card import Deck
from ..core.game_logic import process_action
from ..strategy.base_strategy import Strategy
from ..utils.logger import GameLogger

class GameManager:
    """Manages the game flow between human and computer players"""
    
    def __init__(self, 
                 initial_stack: int = 100,
                 config: Optional[GameConfig] = None,
                 computer_strategy: Optional[Strategy] = None,
                 log_enabled: bool = True):
        """Initialize the game manager with the given configuration and strategy"""
        self.config = config or GameConfig(deck_size=3, max_raises=2, ante=1)
        self.human_stack = initial_stack
        self.computer_stack = initial_stack
        self.human_pos = 1  # Start human as IP
        self.computer = computer_strategy if computer_strategy else Strategy(self.config)
        self.logger = GameLogger(initial_stack) if log_enabled else None
        
    def play_hand(self) -> None:
        """Play a single hand of the game"""
        # Initialize hand
        state = HandState(self.config)
        self._deal_cards(state)
        
        self.logger.log_hand_start()
        
        # Play until hand is complete
        while not state.is_over:
            self.logger.log_state(state)
            action = self._get_action(state)
            process_action(state, action)
            self.logger.log_action_message(state)
            
        # Update stacks and log results
        self._update_stacks(state)
        self.logger.log_hand_end(state, self.human_stack, self.computer_stack)
        
        # Switch positions for next hand
        self.human_pos = (self.human_pos + 1) % 2
    
    def play_session(self, num_hands: int) -> None:
        """Play multiple hands in a session"""
        self.logger.log_session_start(self.human_stack, self.computer_stack)
        
        for i in range(num_hands):
            self.logger.log_hand_header(i + 1, num_hands, self.human_pos)
            self.play_hand()
            
        self.logger.log_session_end(self.human_stack, self.computer_stack)
    
    def _deal_cards(self, state: HandState) -> None:
        """Deal cards to both players"""
        deck = Deck(self.config.deck_size)
        deck.shuffle()
        state.players[0].card = deck.deal_card()
        state.players[1].card = deck.deal_card()
    
    def _get_action(self, state: HandState):
        """Get action from current player (human or computer)"""
        if state.acting_pos == self.human_pos:
            from .cli import get_human_action
            return get_human_action(state)
        else:
            action = self.computer.get_action(state)
            return action
    
    def _update_stacks(self, state: HandState) -> None:
        """Update player stacks based on hand result"""
        self.human_stack += state.players[self.human_pos].stack
        self.computer_stack += state.players[(1 - self.human_pos) % 2].stack