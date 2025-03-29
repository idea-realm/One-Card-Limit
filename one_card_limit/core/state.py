# core/state.py
from .action import Action
from .card import Card
from typing import List
from enum import Enum
from copy import deepcopy

class GameRules:
    """
    Represents the type of One Card Limit game based on number of cards, raises allowed, and ante size.
    
    Attributes:
    deck_size: int - The size of the deck. [3, 13]
    max_raises: int - The number of raises allowed in the hand 
    ante: int - The ante for the hand. The default is 1.
    """
    def __init__(self, deck_size: int, num_raises_allowed: int, ante: int = 1):
        if deck_size not in range(3, 14):
            raise ValueError("Deck size must be between 3 and 13")
        
        self.deck_size = deck_size
        self.num_raises_allowed = num_raises_allowed
        self.ante = ante
        
    def __repr__(self):
        return f"GameRules({self.deck_size}, {self.num_raises_allowed}, {self.ante})"
    
    def __str__(self):
        if self.ante == 1:
            return f"1CL({self.deck_size}, {self.num_raises_allowed})"
        return f"1CL({self.deck_size}, {self.num_raises_allowed}, {self.ante})"
    
    def __eq__(self, other):
        return self.deck_size == other.deck_size and self.num_raises_allowed == other.num_raises_allowed and self.ante == other.ante
    
    def __hash__(self):
        return hash((self.deck_size, self.num_raises_allowed, self.ante))

class PlayerState:
    """
    Represents the state of a player in the hand.
    
    Attributes:
    card: Card - The player's card
    stack: int - The player's stack size in this hand
    pos: int - The player's position in the hand (0 or 1)
    name: str - The player's name (OP or IP)
    
    Methods:
    __str__ - Returns a string representation of the player
    __repr__ - Returns a string representation of the player
    
    """
    
    def __init__(self, pos : int, card: Card = None):
        if pos in [0, 1]:
            self.pos = pos
            self.name = ["OP", "IP"][pos]
        else:
            raise ValueError("Invalid position")

        self.stack = 0
        self.card = card
        
    def __str__(self):
        """
        Returns a string representation of the player.
        This method provides a summary of the player's state, including their card and stack size.
        """
        return f"{self.name}: {self.card} ({self.stack})"
    
    def __repr__(self):
        return f"PlayerState({self.card}, {self.stack}, {self.pos})"

    def __eq__(self, other):
        return self.card == other.card and self.stack == other.stack and self.pos == other.pos
    
    def __hash__(self):
        return hash((self.card, self.stack, self.pos))
    
class HandState:
    """
    Represents the state of the hand.
    """
    def __init__(self, game_rules: GameRules, players: List[PlayerState]):
        self.game_rules = game_rules
        self.players =  players
        self.acting_pos: int = 0  # OP acts first
        self.actions_taken: list[Action] = []
        self.is_over: bool = False
        self.winner: int = None  # Will be set to the winning player's position (0 or 1) when the hand is over
        self.current_bet = 0
        self.pot = 0
        self.raises_made = 0

    @property
    def valid_actions(self):
        if self.is_over:
            raise ValueError("Game is over")
        if self.current_bet == 0:
            return [Action.CHECK, Action.BET]
        if self.raises_made < self.game_rules.num_raises_allowed:
            return [Action.CALL, Action.RAISE, Action.FOLD]
        else:
            return [Action.CALL, Action.FOLD]

    @property
    def stacks(self):
        """
        Returns the current stacks of the players in the hand.
        This property returns a list of integers representing the stacks of each player.
        """
        return [player.stack for player in self.players]
    
    @property
    def cards(self):
        """
        Returns the current cards of the players in the hand.
        This property returns a list of Card objects representing the cards of each player.
        """
        return [player.card for player in self.players]
    
    def __str__(self):
        """
        Returns a string representation of the hand state.
        This method provides a summary of the hand state, including player cards and stacks.
        """
        return f"""
        Players:
            {self.players[0].name}: {self.players[0].card} ({self.players[0].stack})
            {self.players[1].name}: {self.players[1].card} ({self.players[1].stack})
        Pot: {self.pot}
        Current Bet: {self.current_bet}
        Actions Taken: {self.actions_taken}
        """

    def __repr__(self):
        return f"HandState({self.players}, {self.acting_pos}, {self.actions_taken}, {self.is_over})"
    
    def __eq__(self, other):
        return self.players == other.players and self.acting_pos == other.acting_pos and self.actions_taken == other.actions_taken and self.is_over == other.is_over
    
    def __hash__(self):
        return hash((tuple(self.players), self.acting_pos, tuple(self.actions_taken), self.is_over))

    def clone(self):
        return deepcopy(self)