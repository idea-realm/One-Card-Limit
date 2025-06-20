# strategy/info_set.py
"""
This module defines the `InfoState` class and the `get_info_state` function, 
which are used to represent and extract a player's knowledge of the game state 
in a one-card limit poker game.
"""

# Standard Imports
from dataclasses import dataclass, field
from typing import Optional, List
# Local Imports
from ..core.state import Card, Action, HandState

@dataclass
class InfoState:
    """
    An information set represents a player's knowledge of the game state.
    It is a tuple of the game rules, the player's position, their card, and the actions taken so far. 
    """
    pos: int                    # which player's turn it is (0 or 1)
    card: Card
    actions_taken: List[tuple[int, "Action"]] = field(default_factory=list)
    result: Optional[int] = None
    
    @property
    def actions(self) -> str:  # Changed return type to match implementation
        return "".join([str(action) for _, action in self.actions_taken])
    
    def __str__(self) -> str:
        encoded = f"{self.card}"
        if self.actions != "":
            encoded += f"-{self.actions}"        
        if self.result is not None:            
            encoded += f"-({str(self.result)})"       
        return encoded
    
    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.__str__())

def get_info_state(state: HandState, pos: int) -> InfoState:
    """
    Returns an observed state for the given player position.
    """
    result = None
    if state.is_over:
        # If the hand is over, return the final stack for the player
        result = state.players[pos].stack
    
    return InfoState(
        pos=pos, 
        card=state.players[pos].card, 
        actions_taken=state.actions_taken,
        result=result
    )