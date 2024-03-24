from enum import Enum
import random


class Card:
    def __init__(self, rank, val):
        self.rank = rank
        self.val = val

class Deck:
    def __init__(self):
        card_ranks = ["10", "J", "Q", "K", "A"]
        self.cards = [Card(rank, val) for val, rank in enumerate(card_ranks, start=2)]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        self.shuffle()
        return self.cards.pop()

class Player:
    def __init__(self, name, stack_size):
        self.name = name
        self.stack_size = stack_size
        self.card = None

    def get_actions(self, hand_state):
        actions = {
            "Open": ["Check", "Bet"],
            "OP_Check": ["Check", "Bet"],
            "OP_Bet": ["Call", "Fold"],
            "IP_Bet": ["Call", "Fold"]
        }
        return actions[hand_state]

class HumanPlayer(Player):
    def __init__(self, name, stack_size):
        super().__init__(name, stack_size)
        
    def decide_action(self, hand_state):
        print(f"You have {self.card.rank}")
        actions = self.get_actions(hand_state)
        while True:
            for i, action in enumerate(actions, start=1):
                print(f"{i}. {action}")
            try:
                selection = int(input("Select an action: "))
                if 1 <= selection <= len(actions):
                    return actions[selection - 1]
                else:
                    print("Please select a valid action.")
            except ValueError:
                print("Please enter a number.")

class ComputerPlayer(Player):
    def __init__(self, name, stack_size, strategy):
        super().__init__(name, stack_size)
        self.strategy = strategy

    def decide_action(self, hand_state):
        actions = self.get_actions(hand_state)
        strategy_key = (self.card.rank, hand_state)
        probabilities = self.strategy.get(strategy_key, None)
        if probabilities:
            action = random.choices(actions, weights=probabilities)[0]
        else:
            action = random.choice(actions)
        return action

class Hand:
    def __init__(self, ante, bet_size):
        self.deck = Deck()
        self.ante = ante
        self.bet_size = bet_size
        self.pot = 0
        self.state = None
       
    def play_hand(self, IP, OP):
        self.state = "Open"
        for player in [OP,IP]:
            player.card = self.deck.deal()   
            player.stack_size -= self.ante
        self.pot += 2 * self.ante
        print(f"Pot is {self.pot}, blinds posted")
        
        self.execute_rounds(IP, OP)
        
    def execute_rounds(self, IP, OP):
        if self.state == "Open":
            self.handle_action(OP, IP, if_check = "OP_Check", if_bet = "OP_Bet")
            
        if self.state == "OP_Check":
            self.handle_action(IP, OP, if_check = "Showdown", if_bet = "IP_Bet")
            
        if self.state == "OP_Bet":
            self.handle_action(IP, OP, if_call = "Showdown", if_fold = "Fold")  
            
        if self.state == "IP_Bet":
            self.handle_action(OP, IP, if_call = "Showdown", if_fold = "Fold")
            
        if self.state == "Showdown":
            self.showdown(IP, OP)
        
    def handle_action(self, acting_player, other_player, if_check = None, if_fold = None, if_bet=None, if_call=None):
        
        action = acting_player.decide_action(self.state)
        
        if action == "Check":
            print(f"{acting_player.name} checks")
            self.state = if_check
            
        elif action == "Bet":
            print(f"{acting_player.name} bets {self.bet_size}")
            self.pot += self.bet_size
            acting_player.stack_size -= self.bet_size
            self.state = if_bet
            
        elif action == "Call":
            print(f"{acting_player.name} calls")
            self.pot += self.bet_size
            acting_player.stack_size -= self.bet_size
            self.state = if_call
            
        elif action == "Fold":
            print(f"{acting_player.name} folds")
            self.decide_winner(other_player)
            self.state = if_fold

    def showdown(self, IP, OP):
        print(f"{IP.name} shows {IP.card.rank}, {OP.name} shows {OP.card.rank}")
        if IP.card.val > OP.card.val:
            self.decide_winner(IP)
        else:
            self.decide_winner(OP)
            
    def decide_winner(self, winner):
        print(f"{winner.name} wins pot of {self.pot}")
        winner.stack_size += self.pot

    
        