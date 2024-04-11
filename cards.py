# cards.py
import random

class Card:
    def __init__(self, val, rank, suit = None):
        self.rank : str = rank
        self.val : int = val
        self.suit : str = suit

    def __str__(self) -> str:
        if self.suit:
            return f"{self.rank}{self.suit}"    
        else:
            return f"{self.rank}"
    
    def __repr__(self) -> str:
        return f"Card({self.val},{self.rank},{self.suit})"
    
    def __eq__(self, __value: object) -> bool:
        return self.val == __value
    
    def __hash__(self):
        return hash((self.rank, self.val, self.suit))
    
class Deck:
    def __init__(self, size: int = None, suited = False):
        card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        card_suits = ["d","h","c","s"]
        
        if size is None:
            size = len(card_ranks) * len(card_suits)   
        if suited:
            size *= 4
            cards = [Card(val, rank, suit) for val, rank in enumerate(card_ranks) for suit in card_suits]
        else:
            cards = [Card(val, rank) for val, rank in enumerate(card_ranks)]
            
        self.cards = cards[-size:]
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        self.shuffle()
        return self.cards.pop()

    def __str__(self) -> str:
        return "Deck(" + f"{[str(card) for card in self.cards]})" 

    def __iter__(self) -> None:
        return iter(self.cards)