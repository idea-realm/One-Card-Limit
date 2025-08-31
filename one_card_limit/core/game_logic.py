# core/game_logic.py
"""
This module defines the core components and state management for a hand of one-card limit poker game, including hand initialization, player actions, and state transitions.
"""

# Standard Imports
from enum import Enum
from typing import List, Literal, Tuple, Optional
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

@dataclass
class Card:
    """Represents a playing card"""
    def __init__(self, rank: str | int) -> None:
        card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        if isinstance(rank, int):
            rank = card_ranks[rank]
        if rank not in card_ranks:
            raise ValueError("Invalid card rank")
        else:
            self.rank: str = rank
            self.val: int = card_ranks.index(rank)    
        
    def __str__(self) -> str:
        return f"{self.rank}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.val == other.val
    
    def __hash__(self) -> int:
        return hash(self.rank)
    
    def __lt__(self, other):
        return self.val < other.val
    
    def __gt__(self, other):
        return self.val > other.val

@dataclass
class GameConfig:
    """Configuration for the game rules."""
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
        return f"GameConfig(deck_size={self.deck_size}, max_raises={self.max_raises}, ante={self.ante})"
    
    def get_deck(self) -> List[Card]:
        """Generates a deck of cards based on the configuration."""
        card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        return [Card(rank) for rank in card_ranks[::-1][:self.deck_size]]
    
    def get_all_card_combos(self) -> List[Tuple[Card, Card]]:
        """Generates all possible card combinations for the game."""
        deck = self.get_deck()
        combos = []
        for i in range(len(deck)):
            for j in range(i + 1, len(deck)):
                combos.append((deck[i], deck[j]))
                combos.append((deck[j], deck[i]))
        return combos

    
@dataclass
class InfoState:
    """
    An information set represents a player's knowledge of the game state.
    It is a tuple of the game rules, the player's position, their card, and the actions taken so far. 
    """
    pos: int
    card: Card
    actions: List[Action]
    valid_actions: List[Action]
    result: Optional[int] = None
    
    def __str__(self) -> str:
        encoded = f"{self.card}"
        if len(self.actions) > 0:
            action_str = "".join([str(action) for action in self.actions])
            encoded += f"-{action_str}"        
        if self.result is not None:            
            encoded += f"-({str(self.result)})"       
        return encoded
    
    def __repr__(self) -> str:
        return f"InfoState(pos={self.pos}, card={self.card}, actions={self.actions})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InfoState):
            return False
        return (self.card == other.card and 
                self.actions == other.actions)
            
    def __hash__(self) -> int:
        return hash((self.pos, self.card, tuple(self.actions)))
    
class HandState:
    """
    Represents the mutable state of a single hand of one card limit poker.
    """
    def __init__(self, config: GameConfig, deal_cards: bool = False) -> None:
        """Initializes hand state with given game configuration."""
        self.config: GameConfig = config
        self.cards: List[Card] = []
        self.actions: List[Action] = []
        self.stacks: List[int] = [-config.ante,-config.ante]
        self.acting_pos: int = 0
        self.current_bet: int = 0
        self.pot: int = 2 * config.ante
        self.raises_made: int = 0
        self.is_over: bool = False
        self.showdown: bool = False
        self.winner_pos: int = None
        self.cards_dealt: bool = False

        if deal_cards:
            self.deal_cards()
    
    def deal_cards(self) -> None:
        """Assigns cards to players if none dealt"""
        if self.cards_dealt:
            raise ValueError("Cards already dealt.")
        deck = self.config.get_deck()
        shuffle(deck)
        self.cards = [deck.pop(), deck.pop()]
        self.cards_dealt = True
    
    def get_valid_actions(self) -> List[Action]:
        """
        Returns a list of valid actions for the acting player of the hand
        """
        if not self.cards_dealt:
            raise ValueError("Cards not dealt")
        if self.is_over:
            raise ValueError("Hand is over")
        else: 
            if self.current_bet == 0:
                return [Action.CHECK, Action.BET]
            else:
                valid = [Action.CALL, Action.FOLD]
                if self.raises_made < self.config.max_raises:
                    valid.append(Action.RAISE)
                return valid

    def get_info_state(self, player_pos: int) -> InfoState:
        if player_pos not in [0,1]:
            raise ValueError("Player position must be 0 or 1")
        else:
            return InfoState(
                pos = player_pos,
                card = self.cards[player_pos],
                actions = self.actions,
                valid_actions = self.get_valid_actions() if not self.is_over else [],
                result = self.stacks[player_pos] if self.is_over else None
            )
    
    def process_action(self, action: Action | str) -> None:
        """Updates the hand state based on the action taken by the current player"""
        action = self.convert_action(action)
        if self.is_over:
            raise ValueError("Hand is already over")
        elif not self.cards_dealt:
            raise ValueError("Cards have not been dealt yet")
        valid = self.get_valid_actions()
        if action not in valid:
            raise ValueError(f"Invalid action {action}, valid: {valid}")

        # Record the action in the history
        self.actions.append(action)

        match action:
            case Action.CHECK:
                self._handle_check()
            case Action.BET:
                self._handle_bet()
            case Action.CALL:
                self._handle_call()
            case Action.RAISE:
                self._handle_raise()
            case Action.FOLD:
                self._handle_fold()
                
        # Switch to next player
        self.acting_pos = (self.acting_pos + 1) % 2
        
        # If the hand is over, finalize outcomes
        if self.is_over:
            return self._end_hand()

    def _handle_check(self) -> None:
        if self.acting_pos == 1:
            self.is_over = True
            self.showdown = True
            return None
        else:
            return None

    def _handle_bet(self) -> None:
        self.current_bet = self.config.ante
        self.pot += self.current_bet
        self.stacks[self.acting_pos] -= self.current_bet

    def _handle_call(self) -> None:
        self.pot += self.current_bet
        self.stacks[self.acting_pos] -= self.current_bet
        self.is_over = True
        self.showdown = True

    def _handle_raise(self) -> None:
        if self.raises_made < self.config.max_raises:
            new_bet = self.current_bet * 2
            self.current_bet = new_bet - self.current_bet
            self.pot += new_bet
            self.stacks[self.acting_pos] -= new_bet
            self.raises_made += 1
        else:
            raise ValueError("No raises left, can't raise")

    def _handle_fold(self) -> None:
        self.winner_pos = (self.acting_pos + 1) % 2
        self.is_over = True
        return None

    def _end_hand(self) -> None:
        if not self.is_over:
            raise ValueError("Hand is not over yet")
        # Determine winner
        if self.showdown:
            self.winner_pos = 0 if self.cards[0] > self.cards[1] else 1

        # Award pot to winner
        self.stacks[self.winner_pos] += self.pot
    
    def __str__(self) -> str:        
        encoded = "".join([str(card) for card in self.cards])
        if self.actions != []:
            action_str = "".join([str(action) for action in self.actions])
            encoded += f"-({action_str})"        
        if self.is_over and self.winner_pos is not None:
            stacks = "".join([str(stack) for stack in self.stacks])            
            encoded += f"-({stacks})"       
        return encoded

    def __hash__(self) -> int:
        return hash(self.config, tuple(self.cards), tuple(self.actions))

    def __repr__(self) -> str:
        return f"HandState(config={self.config}, cards={self.cards}, actions={self.actions})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HandState):
            return False
        return (self.config == other.config and 
                self.cards == other.cards and 
                self.actions == other.actions)
        
    # Helper methods for handling actions as strings
    @staticmethod
    def convert_action(action: Action | str) -> Action:
        if isinstance(action, str):
            if action in ["x", "b", "c", "r", "f", "x"]:
                action_map = {
                    "x": Action.CHECK,
                    "b": Action.BET,
                    "c": Action.CALL,
                    "r": Action.RAISE,
                    "f": Action.FOLD
                }
                action = action_map[action]
            try:
                action = Action(action)
            except ValueError:
                raise ValueError(f"Invalid action string: {action}")
        elif not isinstance(action, Action):
            raise ValueError(f"Action must be of type Action or str, got {type(action)}")
        return action

    def clone(self) -> "HandState":
            return deepcopy(self)
    
    @classmethod
    def from_cards(cls, config: GameConfig, cards: List[Card|None]) -> "HandState":
        """
        Creates a HandState from given cards. Cards argument must have length 2 and be unique. 
        If one card is None, it will be randomly drawn from the deck.
        """
        
        if len(cards) != 2:
            raise ValueError("Must provide exactly 2 cards")
        
        # Both cards provided
        if isinstance(cards[0], Card) and isinstance(cards[1],Card):
            if cards[0] == cards[1]:
                raise ValueError("Cards must be unique")
            elif cards[0] not in config.get_deck() or cards[1] not in config.get_deck():
                raise ValueError("Cards must be in the deck")
        
        # One card provided
        else:
            deck = config.get_deck()
            while None in cards:
                for pos, card in enumerate(cards):
                    if isinstance(card,Card):
                        deck.remove(card)
                        shuffle(deck)
                        cards[1 - pos] = deck.pop()

        state = cls(config, deal_cards=False)
        state.cards = cards
        state.cards_dealt = True
        return state
    
    @classmethod 
    def from_cards_actions(cls, config: GameConfig, cards: List[Card|None], actions: List[Action|str]) -> "HandState":
        """Creates a HandState from given cards and action history. Actions must be valid for the given cards and game configuration. Can be a mix of Action enums or strings."""
        state = cls.from_cards(config, cards)
        for action in actions:
            action = cls.convert_action(action)
            state.process_action(action)
        return state

def generate_all_handstates(config: GameConfig) -> List[HandState]:
    """Generate all possible HandState objects for a given GameConfig."""
    all_handstates = []
    card_combos = config.get_all_card_combos()  # Generate all possible card combinations
    
    for cards in card_combos:
        # Create the initial HandState with the given card combination
        initial_state = HandState(config, deal_cards=False)
        initial_state.cards = list(cards)
        initial_state.cards_dealt = True
        
        # Recursively generate all possible states from the initial state
        generate_states_recursive(initial_state, all_handstates)
    
    return all_handstates

def generate_states_recursive(state: HandState, all_handstates: List[HandState]) -> None:
    """Recursively generate all possible HandState objects from a given state."""
    
    if state.is_over:
        # If the hand is over, add the state to the list and stop recursion
        all_handstates.append(state.clone())
        return
    
    # Add the current state to the list
    all_handstates.append(state.clone())
    
    # Generate new states for each valid action
    for action in state.get_valid_actions():
        new_state = state.clone()
        new_state.process_action(action)
        generate_states_recursive(new_state, all_handstates)

def generate_handstate_infostates(config: GameConfig) -> List[Tuple[HandState, List[InfoState]]]:
    """Generate all HandState objects and their corresponding InfoStates."""
    handstates_with_infostates = []
    all_handstates = generate_all_handstates(config)
    
    for handstate in all_handstates:
        if handstate.is_over:
            # If the hand is over, generate InfoStates for both players
            infostates = [
                handstate.get_info_state(0),  # InfoState for player 0
                handstate.get_info_state(1)   # InfoState for player 1
            ]
        else:
            # If the hand is not over, generate InfoState for the acting player
            infostates = [handstate.get_info_state(handstate.acting_pos)]
        
        handstates_with_infostates.append((handstate, infostates))
    
    return handstates_with_infostates