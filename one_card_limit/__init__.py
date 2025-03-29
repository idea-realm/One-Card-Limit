"""
One Card Limit - A poker variant game implementation.

This package provides the One Card Limit game implementation with classes
for game mechanics, player strategies, cards, actions, and game state.
"""

__version__ = '0.1.0'

# Import main components to expose at the package level
from .core.game import OneCardLimitGame
from .core.strategy import Strategy
from .core.human_player import HumanStrategy
from .core.card import Card, Deck
from .core.action import Action
from .core.state import HandState, GameRules, PlayerState

__all__ = [
    'OneCardLimitGame',
    'Strategy',
    'HumanStrategy',  # Added HumanStrategy
    'Card',
    'Deck',  # Added Deck
    'Action',
    'HandState',
    'GameRules',
    'PlayerState'
]