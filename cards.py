# cards.py
import random

class Card:
    def __init__(self, rank, suit = None):
        card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        card_suits = ["d","h","c","s"]
        if rank in card_ranks: 
            self.rank : str = rank
            self.val : int = card_ranks.index(rank)
        if suit is None or suit in card_suits:
            self.suit : str = suit
        else:
            return ValueError  

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
            cards = [Card(rank, suit) for rank in enumerate(card_ranks) for suit in card_suits]
        else:
            cards = [Card(rank) for rank in card_ranks]
            
        self.cards = cards[-size:]
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        self.shuffle()
        return self.cards.pop()
    
    def deal_hand(self, num_cards: int, num_players: int):
        cards = [tuple([self.deal() for _ in range(num_cards)]) for _ in range(num_players)]
        return tuple(cards)
    
    def __str__(self) -> str:
        return "Deck(" + f"{[str(card) for card in self.cards]})" 

    def __iter__(self) -> None:
        return iter(self.cards)