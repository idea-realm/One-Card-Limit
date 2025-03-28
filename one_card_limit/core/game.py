# core/game.py
from typing import Optional, Tuple
from .card import Deck
from .state import HandState, GameRules, PlayerState
from .action import Action

class OneCardLimitGame:
    def __init__(self, deck_size: int, num_raises_allowed: int, ante: int = 1):
        self.game_rules = GameRules(deck_size, num_raises_allowed, ante)
        self.state = HandState(self.game_rules)  # Initialize the hand state with game rules 
        self.message_log = list[str]()
        self.history = list[HandState]()
        self.state.players = [
            PlayerState(pos=0),  # OP
            PlayerState(pos=1)   # IP
        ]
    
    @property
    def players(self):
        """
        Returns the list of players in the game.
        This property allows access to the players in the game state.
        """
        return self.state.players
    
    @property
    def is_complete(self) -> bool:
        """
        Returns True if the game is complete (i.e., the hand is over).
        This property checks the is_over flag in the hand state.
        """
        return self.state.is_over
    
    @property
    def acting_pos(self):
        return self.state.acting_pos
    
    @property
    def acting_player_name(self):
        return self.players[self.state.acting_pos].name
    
    def start_hand(self):
        self.deal_cards()
        self.message_log.append(f"Both players ante {self.game_rules.ante}.")
        self.history.append(self.state.clone())

    def next_action(self, action: Action):
        if self.is_complete:
            raise ValueError("Game is over")
        self.process_action(action)
        self.history.append(self.state.clone())

    def deal_cards(self):
        deck = Deck(self.game_rules.deck_size)
        deck.shuffle()
        for i, player in enumerate(self.players):
            self.players[i].card = deck.deal_card()
            self.players[i].stack -= self.game_rules.ante
            self.state.pot += self.game_rules.ante

    def process_action(self, action: Action) -> Optional[str]:
        self.state.actions_taken.append(action)
        match action:
            case Action.CHECK:
                self.handle_check()
            case Action.BET:
                self.handle_bet()
            case Action.CALL:
                self.handle_call()
            case Action.RAISE:
                self.handle_raise()
            case Action.FOLD:
                self.handle_fold()
        
    def handle_check(self) -> Optional[str]:
        self.message_log.append(f"{self.acting_player_name} checks.")
        if len(self.state.actions_taken) >= 2 and self.state.actions_taken[-2] == Action.CHECK:
            self.state.is_over = True
            return self.showdown()
        self.toggle_player()
        return None

    def handle_bet(self) -> Optional[str]:
        self.state.current_bet = self.game_rules.ante
        self.message_log.append(f"{self.acting_player_name} bets {self.state.current_bet}.")
        self.state.pot += self.state.current_bet
        self.players[self.acting_pos].stack -= self.state.current_bet
        self.toggle_player()
        return None

    def handle_call(self) -> Optional[str]:
        self.message_log.append(f"{self.acting_player_name} calls {self.state.current_bet}.")
        self.state.pot += self.state.current_bet
        self.players[self.state.acting_pos].stack -= self.state.current_bet
        self.state.is_over = True
        return self.showdown()

    def handle_raise(self) -> Optional[str]:
        if self.state.raises_made < self.game_rules.num_raises_allowed:
            new_bet = self.state.current_bet * 2
            self.state.current_bet = new_bet
            self.message_log.append(f"{self.acting_player_name} raises to {new_bet}.")
            self.state.pot += new_bet
            self.players[self.state.acting_pos].stack -= new_bet
            self.state.raises_made += 1
            self.toggle_player()
            return None
        else:
            raise ValueError("No raises left, can't raise")

    def handle_fold(self) -> Optional[str]:
        self.state.is_over = True
        self.message_log.append(f"{self.acting_player_name} folds.")
        self.state.winner = (self.state.acting_pos + 1) % 2
        return self.end_hand()

    def showdown(self) -> Tuple[str, int]:
        self.state.is_over = True
        print("Entering showdown...")  # For debugging purposes
        self.message_log.append(
            f"Showdown:\n"
            f"{self.players[0].name} shows {self.players[0].card}\n"
            f"{self.players[1].name} shows {self.players[1].card}."
        )
        if self.players[0].card > self.players[1].card:
            self.state.winner = 0
        else:
            self.state.winner = 1    
        return self.end_hand()
    
    def end_hand(self) -> None:
        """
        Ends the current hand and determines the winner.
        This method sets the is_over flag to True and determines the winner based on the players' cards.
        """
        
        self.players[self.state.winner].stack += self.state.pot  # Add the pot to the winning player's stack
        self.message_log.append(f"Player {self.state.winner} wins the pot of {self.state.pot}.")
            
    def toggle_player(self):
        self.state.acting_pos = (self.acting_pos + 1) % 2