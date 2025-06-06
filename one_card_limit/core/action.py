# core/action.py
from enum import Enum

class Action(Enum):
    CHECK = "check"
    BET = "bet"
    CALL = "call"
    RAISE = "raise"
    FOLD = "fold"

    def __str__(self):
        if self.value == "check":
            return "x"
        return self.value[0].lower()
    
    def __repr__(self):
        return self.value
