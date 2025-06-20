# core/state.py
"""
This module defines the core components and state management for a hand of one-card limit poker game, including hand initialization, player actions, and state transitions.
"""

# Standard Imports
from enum import Enum
from typing import List, Literal
from dataclasses import dataclass, field
from copy import deepcopy
from random import shuffle

class Action(Enum):
    CHECK = "check"
    BET = "bet"
    CALL = "call"
    RAISE = "raise"
    FOLD = "fold"
    
    def __str__(self) -> Literal['x', 'b', 'c', 'r', 'f']:
        if self.value == "check":
            return "x"
        return self.value[0].lower()
    
    def __repr__(self)  -> Literal['check', 'bet', 'call', 'raise', 'fold']:
        return self.value

class Card:
    """
    Represents a playing card
    """
    def __init__(self, rank: str | int) -> None:
        card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        
        if isinstance(rank, int):
            rank = card_ranks[rank]
        
        if rank not in card_ranks:
            raise ValueError("Invalid card rank")
        else:
            self.rank = rank
            self.val = card_ranks.index(rank)    
        
    def __str__(self) -> str:
        return f"{self.rank}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank})"

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self) -> int:
        return hash(self.val)

class Deck:
    """
    Represents a deck of cards.
    """
    def __init__(self, size: int) -> None:
        card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        if size not in range(3, 14):
            raise ValueError("Deck size must be between 3 and 13")
        
        self.cards = [Card(rank) for rank in card_ranks[::-1][:size]] 
    
    def shuffle(self) -> None:
        shuffle(self.cards)
    
    def deal_card(self) -> Card:
        return self.cards.pop()
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        return "Deck(" + f"{[str(card) for card in self.cards]})"
    
    def __repr__(self) -> str:
        return f"Deck({len(self.cards)})"

@dataclass
class GameConfig:
    """
    Configuration for the game rules.
    """
    deck_size: int = 4
    max_raises: int = 2
    ante: int = 1
    
    def __post_init__(self) -> None:
        if not (3 <= self.deck_size <= 13):
            raise ValueError("Deck size must be between 3 and 13")
        
        if not (0 <= self.max_raises < 3):
            raise ValueError("Max raises must be between 0 and 2")

    def __str__(self) -> str:
        return f"{self.deck_size}-{self.max_raises}"
    
    def __repr__(self) -> str:
        return self.__str__()

@dataclass
class PlayerState:
    """
    Represents a single player's state in the hand.
    """
    pos: int          # 0 = OP, 1 = IP
    stack: int        # player's stack result for the hand
    card: Card        # the player's card 
    
    def __str__(self) -> str:
        return f"{self.name}, {self.stack}, {self.card}"
        
    @property
    def name(self) -> str:
        return ["OP", "IP"][self.pos]

@dataclass
class HandState:
    """
    Represents the mutable state of a single hand of one card limit poker.
    """
    config: GameConfig
    players: List[PlayerState] = field(default_factory=list)
    acting_pos: int = 0
    current_bet: int = 0
    pot: int = 0
    raises_made: int = 0
    is_over: bool = False
    showdown: bool = False
    actions_taken: List[tuple[int, "Action"]] = field(default_factory=list)
    winner_pos: int = None
    
    def __post_init__(self) -> None:
        # Only initialize if players list is empty
        if not self.players:
            # Initialize players with ante
            self.players = [
                PlayerState(pos=i, card=None, stack=-self.config.ante)
                for i in [0, 1]
            ]
            
            # Initialize the pot
            self.pot = 2 * self.config.ante
    
    @classmethod
    def create_new_hand(cls, config: GameConfig) -> "HandState":
        """Factory method to create a new hand with proper initialization."""
        return cls(config=config)
    
    @property
    def cards_dealt(self) -> bool:
        return all(player.card is not None for player in self.players)
    
    @property
    def acting_player(self) -> PlayerState:
        return self.players[self.acting_pos]
    
    def __str__(self) -> str:        
        encoded = "".join([str(player.card) for player in self.players])
        if self.actions_taken != []:
            actions = "".join([str(action) for _, action in self.actions_taken])
            encoded += f"-({actions})"        
        if self.is_over and self.winner_pos is not None:
            stacks = "".join([str(player.stack) for player in self.players])            
            encoded += f"-({stacks})"       
        return encoded

    def __hash__(self) -> int:
        return hash(self.__str__())

    def clone(self) -> "HandState":
        return deepcopy(self)
