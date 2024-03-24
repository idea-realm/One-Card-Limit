from player import Player
import time, random

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

    def deal(self) -> Card:
        self.shuffle()
        return self.cards.pop()

class Hand:
    def __init__(self, IP : Player, OP : Player, bet_size : int = 1, ante : int = 1, print_output = True) -> None:
        self.pot : int = 0
        self.ante = ante
        self.bet_size = bet_size
        self.players = {"IP" : IP, "OP" : OP}
        
        self.print_output = print_output
        self.output_msg : list[str] = []
        
        self.state : str = None
        self.is_over = False
        
        self.states = {
            "Open" : {
                "acting_player" : self.players["OP"],
                "actions" : {
                    "Check" : "OP_Check",
                    "Bet" : "OP_Bet"
                }
            },
            "OP_Check" : {
                "acting_player" : self.players["IP"],
                "actions" : {
                    "Check" : "Showdown",
                    "Bet" : "IP_Bet"
                }
            },
            "OP_Bet" : {
                "acting_player" : self.players["IP"],
                "actions" : {
                    "Call" : "Showdown",
                    "Fold" : "OP_Win"
                }
            },
            "IP_Bet" : {
                "acting_player" : self.players["OP"],
                "actions" : {
                    "Call" : "Showdown",
                    "Fold" : "IP_Win"
                }
            }
        }
        
        self.play_hand()
    
    def acting_player(self) -> Player:
        return self.states[self.state]["acting_player"]
    
    def avail_actions(self) -> list[str]:
        return list(self.states[self.state]["actions"].keys())
    
    def disp_output(self):
        if len(self.output_msg) > 0:
            for msg in self.output_msg:
                print(msg)
            print(f"Pot is {self.pot}")
            print("------------------")
            time.sleep(1)
            self.output_msg = []
    
    def play_hand(self):
        deck = Deck()
        for pos, player in self.players.items():
            player.card = deck.deal() 
            player.stack_size += -self.ante
            self.pot += self.ante
            self.output_msg.append(f"{player.name} is {pos}")
        
        self.state = "Open"
        
        while not self.is_over:
            
            if self.print_output:
                self.disp_output()
            
            actions = self.avail_actions()
            curr_player = self.acting_player()
            action = curr_player.decide_action(self.state, actions)
            self.handle_action(action)
         
            if self.state == "Showdown":
                self.is_over = True
                self.showdown()
            
            elif self.state in ["IP_Win","OP_Win"]:
                self.is_over = True
                winner = self.players[self.state[:2]]
                self.end_hand(winner)

            if self.print_output:
                self.disp_output()
            
            
    def handle_action(self, action):
        acting_player = self.acting_player()
        match action:
            case "Check":
                msg = f"{acting_player.name} checks"
            case "Bet":
                msg = f"{acting_player.name} bets {self.bet_size}"
                self.pot += self.bet_size
                acting_player.stack_size -= self.bet_size
            case "Call":
                msg = f"{acting_player.name} calls"
                self.pot += self.bet_size
                acting_player.stack_size -= self.bet_size
            case "Fold":
                msg = f"{acting_player.name} folds"
        
        self.output_msg.append(msg)
        self.state = self.states[self.state]["actions"][action]
        
    def showdown(self):
        for player in self.players.values():
            self.output_msg.append(f"{player.name} shows {player.card.rank}")
        if self.players["IP"].card.val > self.players["OP"].card.val:
            self.end_hand(self.players["IP"])
        else:
            self.end_hand(self.players["OP"])
            
    def end_hand(self, winner):
        self.output_msg.append(f"{winner.name} wins pot of {self.pot}")
        winner.stack_size += self.pot    
        