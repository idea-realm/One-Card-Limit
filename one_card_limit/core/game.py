# core/game.py
from typing import Optional, Tuple
from .card import Deck
from .state import HandState, GameRules, PlayerState
from .action import Action

class OneCardLimitGame:
    def __init__(self, deck_size: int, num_raises_allowed: int, ante: int = 1):
        game_rules = GameRules(deck_size, num_raises_allowed, ante)
        players = [
            PlayerState(0),
            PlayerState(1)
        ]
        self.state = HandState(game_rules, players)
        self.history : list[HandState] = []
        self.message : list[str] = []
        
    @property
    def game_rules(self) -> GameRules:
        """
        Returns the game rules.
        This property allows access to the game rules of the current game state.
        """
        return self.state.game_rules
    
    @property
    def players(self) -> list[PlayerState]:
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
    def acting_player(self):
        """
        Returns the player who is currently acting.
        This property retrieves the player based on the acting position in the hand state.
        """
        return self.players[self.state.acting_pos]
    
    def start_hand(self):
        self.deal_cards()
        self.message.append(f"Both players ante {self.game_rules.ante}.")
        self.history.append(self.state.clone())
    
    def deal_cards(self):
        deck = Deck(self.game_rules.deck_size)
        deck.shuffle()
        for player in self.players:
            player.card = deck.deal_card()
            player.stack -= self.game_rules.ante
            self.state.pot += self.game_rules.ante
    
    def next_action(self, action: Action): 
        """
        Process the next action taken by the player.
        This method updates the game state based on the action taken by the player.
        """
        if self.state.is_over:
            raise ValueError("Game is over")
        self.process_action(action)
        self.history.append(self.state.clone())

    def process_action(self, action: Action) -> None:
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
        self.message.append(f"{self.acting_player.name} checks.")
        if len(self.state.actions_taken) >= 2 and self.state.actions_taken[-2] == Action.CHECK:
            self.state.is_over = True
            return self.showdown()
        self.toggle_player()
        return None

    def handle_bet(self) -> Optional[str]:
        self.state.current_bet = self.game_rules.ante
        self.state.pot += self.state.current_bet
        self.acting_player.stack -= self.state.current_bet
        self.message.append(f"{self.acting_player.name} bets {self.state.current_bet}.")
        self.toggle_player()
        return None

    def handle_call(self) -> Optional[str]:
        self.state.pot += self.state.current_bet
        self.acting_player.stack -= self.state.current_bet
        self.message.append(f"{self.acting_player.name} calls {self.state.current_bet}.")
        self.state.is_over = True
        return self.showdown()

    def handle_raise(self) -> None:
        if self.state.raises_made < self.game_rules.num_raises_allowed:
            new_bet = self.state.current_bet * 2
            self.state.current_bet = new_bet
            self.state.pot += new_bet
            self.acting_player.stack -= new_bet
            self.state.raises_made += 1
            self.message.append(f"{self.acting_player.name} raises to {new_bet}.")
            self.toggle_player()
            return None
        else:
            raise ValueError("No raises left, can't raise")

    def handle_fold(self) -> None:
        self.state.is_over = True
        self.message.append(f"{self.acting_player.name} folds.")
        self.state.winner = (self.state.acting_pos + 1) % 2
        return self.end_hand()

    def showdown(self) -> Tuple[str, int]:
        self.state.is_over = True
        self.message.append(
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
        self.message.append(f"Player {self.players[self.state.winner].name} wins the pot of {self.state.pot}.")
            
    def toggle_player(self) -> None:
        """
        This method switches the acting position between the two players.
        """
        self.state.acting_pos = (self.state.acting_pos + 1) % 2
        
    def dealer_message(self) -> str:
        """
        Returns the dealer message.
        This message is used to display the action in the game.
        """
        message = '\n'.join(self.message)
        self.message = []  # Clear the message after displaying
        return message