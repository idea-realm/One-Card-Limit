# core/card.py
import random

card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
card_suits = ["d", "h", "c", "s"]

class Card:
    """
    Represents a playing card
    """
    def __init__(self, rank: str | int, suit: str = None):
        if isinstance(rank, int):
            rank = card_ranks[rank]
        
        if rank not in card_ranks:
            raise ValueError("Invalid card rank")
    
        if suit and suit not in card_suits:
            return ValueError("Invalid card suit")
        
        else:
            self.suit = suit
            self.rank = rank
            self.val = card_ranks.index(rank)    
        

    def __str__(self) -> str:
        if self.suit:
            return f"{self.rank}{self.suit}"    
        else:
            return f"{self.rank}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank})"

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash((self.val, self.rank, self.suit))

class Deck:
    """
    Represents a deck of cards.    
    """
    def __init__(self, size: int):
        if size not in range(3, 14):
            raise ValueError("Deck size must be between 3 and 13")
        
        self.cards = [Card(rank) for rank in card_ranks[::-1][:size]] 
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()
    
    def __iter__(self) -> iter:
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)
    
    def __str__(self) -> str:
        return "Deck(" + f"{[str(card) for card in self.cards]})"
    
    def __repr__(self) -> str:
        return f"Deck({len(self.cards)})"