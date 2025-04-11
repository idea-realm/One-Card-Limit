# core/state.py
from dataclasses import dataclass, field
from copy import deepcopy
from typing import List
from .card import Card
from .action import Action

@dataclass
class GameConfig:
    """
    Configuration for the game rules.
    """
    deck_size: int
    max_raises: int
    ante : int = 1
    
    def __post_init__(self):
        if not (3 <= self.deck_size <= 13):
            raise ValueError("Deck size must be between 3 and 13")
        if not (0 <= self.max_raises < 3):
            raise ValueError("Max raises must be between 0 and 2")
    
    def __str__(self) -> str:
        return f"{self.deck_size}-{self.max_raises})"
    
    def __repr__(self) -> str:
        return self.__str__()

@dataclass
class PlayerState:
    """
    Represents a single player's state in the hand.
    """
    pos: int          # 0 = OP, 1 = IP
    stack: int        # player's stack result for the hand
    card: Card      # the player's card 
    
    @property
    def name(self) -> str:
        return ["OP", "IP"][self.pos]

@dataclass
class HandState:
    """
    A mutable hand state that references PlayerState objects. 
    We can update fields like pot, or player states in place, but also provide a .clone() for solver branching.
    """
    game_rules: GameConfig
    players: List[PlayerState] = field(default_factory=list)
    acting_pos: int = 0
    current_bet: int = 0
    pot: int = 0
    raises_made: int = 0
    is_over: bool = False
    showdown: bool = False
    actions_taken: List[tuple[int, "Action"]] = field(default_factory=list)
    winner_pos: int = None
    
    def __post_init__(self):
        # Only initialize if players list is empty
        if not self.players:
            # Initialize players with ante
            self.players = [
                PlayerState(pos=i, card=None, stack=-self.game_rules.ante)
                for i in [0, 1]
            ]
            
            # Initialize the pot
            self.pot = 2 * self.game_rules.ante
    
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

    def __hash__(self):
        return hash(self.__str__())

    def clone(self) -> "HandState":
        return deepcopy(self)
