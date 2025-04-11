"""
One Card Limit Poker - A Python implementation of One Card Limit Poker with AI

This package provides a complete implementation of One Card Limit Poker,
including game mechanics, AI strategies, and user interface components.

Main Components:
- core: Basic game mechanics and state management
- strategy: AI strategy implementation and game tree analysis
- interface: User interface and game flow management
- utils: Utility functions and logging

Example usage:
    from one_card_limit.interface import GameManager
    from one_card_limit.core import GameConfig
    
    # Create game with custom configuration
    config = GameConfig(deck_size=3, max_raises=2, ante=1)
    game = GameManager(initial_stack=100, config=config)
    
    # Play 10 hands
    game.play_session(10)
"""

__version__ = "0.1.0"

# Core game components
from .core.action import Action
from .core.card import Card, Deck
from .core.state import GameConfig, HandState
from .core.game_logic import process_action, get_valid_actions

# Strategy components
from .strategy.base_strategy import Strategy
from .strategy.cfr_strategy import CFRStrategy
from .strategy.info_set import InfoState
from .strategy.game_tree import GameNode, build_game_tree

# Interface components
from .interface.game_manager import GameManager
from .interface.cli import get_human_action

# Utility components
from .utils.logger import GameLogger

__all__ = [
    # Core
    'Action',
    'Card',
    'Deck',
    'GameConfig',
    'HandState',
    'process_action',
    'get_valid_actions',
    
    # Strategy
    'Strategy',
    'CFRStrategy',
    'InfoState',
    'GameNode',
    'build_game_tree',
    
    # Interface
    'GameManager',
    'get_human_action',
    
    # Utils
    'GameLogger',
]
