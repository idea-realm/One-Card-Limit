# core/card.py
import random

card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
card_suits = ["d","h","c","s"]

class Card:
    """
    Represents a playing card.
    
    Attributes
    ----------
    rank : str | int
        string or int representing the card rank (e.g., "A" = Ace, 2 = Two, etc.)
    suit : str
        string representing the card suit (e.g., "d" = Diamonds, "h" = Hearts, etc.)
    val : int
        integer value of the card (e.g., 0 = Two, 1 = Three, 12 = Ace, etc.)
    
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
        return f"Card({self.val},{self.rank},{self.suit})"

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
    
    Attributes
    ----------
    cards : List[Card]
        The cards in the deck
    
    Methods
    ----------
    shuffle - Shuffles the deck
    deal_card - Deals a card from the deck
    __len__ - Returns the number of cards in the deck
    __str__ - Returns a string representation of the deck
    __repr__ - Returns a string representation of the deck
    
    """
    def __init__(self, size: int):
        if size not in range(3, 14):
            raise ValueError("Deck size must be between 3 and 13")
        
        self.cards = [Card(rank) for rank in card_ranks[::-1][:size]] 
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)
    
    def __str__(self) -> str:
        return "Deck(" + f"{[str(card) for card in self.cards]})"
    
    def __repr__(self) -> str:
        return f"Deck({len(self.cards)})"