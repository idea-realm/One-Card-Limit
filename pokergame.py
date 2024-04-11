from enum import Enum
from cards import Card, Deck
import random

class Action(Enum):
    CHECK = 1
    RAISE = 2
    CALL = 3
    FOLD = 4

    def __str__(self) -> str:
        return self.name.lower()
    
class Player:
    def __init__(self, name: str = None, card: Card = None):
        self.name = name
        self.card = card
        self.stack_size = 0
        
    def decide_action(self, options: list[Action]):
        return random.choice(options)
    
    def __repr__(self):
        string = f"Player({self.name}, {self.card}, {self.stack_size})"
        return string
    
    def __str__(self) -> str:
        return f"{self.name}: {self.stack_size}, Card: {self.card}"
        
class HumanPlayer(Player):
    def __init__(self, name: str = None, card: Card = None):
        super().__init__(name, card)
        
    def decide_action(self, options: list[Action]) -> Action:
        print(f"You have {self.card}")
        while True:
            for i, action in enumerate(options, start=1):
                print(f"{i}. {action.name}")
            try:
                selection = int(input("Select an action: "))
                if 1 <= selection <= len(options):
                    print("---------------------")
                    return options[selection - 1]
                else:
                    print("Please select a valid action.")
            except ValueError:
                print("Please enter a number.")          
     
class Hand():
    def __init__(self, players: list[Player], deck_size: int = 5, max_raises: int = 1) -> None:    
        self.players = players
        self.max_raises = max_raises
        self.raise_size = 1
        self.pot = 0
        self.curr_bet = 0
        self.raises = 0
        self.acting_pos = 0
        self.is_over = False
        self.winner : int
        self.actions : list[Action] = []

        # deal cards if player cards not provided
        self.deck = Deck(size=deck_size)

        for player in self.players:
            player.card = self.deck.deal()
            player.stack_size += -1
            self.pot += 1
        
    def get_options(self) -> list[Action]:
        """Returns valid Actions given hand state"""
        options = [Action.CHECK, Action.RAISE]
        if self.actions:                            
            if self.actions[-1] == Action.RAISE:
                options = [Action.CALL, Action.FOLD]
                if self.raises < self.max_raises:
                    options.append(Action.RAISE)
        return options
        
    def handle_action(self, action: Action):
        """Updates Hand state based on action"""
        if action == Action.RAISE: 
            self.pot += self.raise_size + self.curr_bet
            self.players[self.acting_pos].stack_size += -(self.raise_size + self.curr_bet)
            self.curr_bet = self.raise_size
            self.raises += 1
            self.raise_size *= 2
        elif action == Action.CALL:
            self.pot += self.curr_bet
            self.players[self.acting_pos].stack_size += -self.curr_bet
            self.get_payouts()
        elif action == Action.CHECK and self.acting_pos == 1:
            self.get_payouts()
        elif action == Action.FOLD:
            self.get_payouts()
        
        self.actions.append(action)
        self.acting_pos = len(self.actions) % 2
        
    def get_payouts(self):
        """Gets winner, updates player stack sizes"""
        #if folded then winner is other player, else winner is higher card
        if self.actions[-1] == Action.FOLD:
            self.winner = (self.acting_pos + 1) % 2
        else:
            self.winner = max([0,1], key = lambda pos: self.players[pos].card.val)
        #award pot to winning p
        self.players[self.winner].stack_size += self.pot
        self.is_over = True
    
    def play_hand(self):
        """Plays hand"""
        while not self.is_over:
            options = self.get_options()
            action = self.players[self.acting_pos].decide_action(options)
            self.handle_action(action)
            self.dealer_message()

    def __str__(self) -> str:
        state =  f"{self.players[0].card}, {self.players[1].card}, {[action.name.lower() for action in self.actions]}"
        if self.is_over:
            state += str(self.players[0].stack_size)
        return state
    
    def dealer_message(self):
        if self.actions:
            last_action = self.actions[-1]
            last_player = self.players[(self.acting_pos + 1) % 2]
            match last_action:
                case Action.CHECK:
                    print(f"{last_player.name} checks")
                case Action.CALL:
                    print(f"{last_player.name} calls {self.curr_bet}")
                case Action.RAISE:
                    print(f"{last_player.name} raises to {self.raise_size}, {self.curr_bet} to call")
                case Action.FOLD:
                    print(f"{last_player.name} folds")
            
        if self.is_over:    
            if last_action != Action.FOLD:
                print(f"{self.players[0].name} shows {self.players[0].card}. {self.players[1].name} shows {self.players[1].card}")
            print(f"{self.players[self.winner].name} wins pot of {self.pot}")