from dataclasses import dataclass
from typing import Dict
from itertools import permutations
from ..core.state import HandState, GameConfig
from ..core.card import Deck
from ..core.action import Action
from ..core.game_logic import get_valid_actions, process_action
from .info_set import InfoState, get_info_state

@dataclass
class GameNode:
    """
    Represents a node in the game tree.
    Each node contains a hand state and its children nodes for each possible action.
    """
    state: HandState
    children: Dict[Action, 'GameNode'] = None
    
    @property
    def info_state(self) -> list[InfoState]:
        """Returns the information set for the acting player or both players if the node is a leaf."""
        info_states = [get_info_state(self.state, self.state.acting_pos)]
        if self.is_leaf:
            info_states.append(get_info_state(self.state, (self.state.acting_pos + 1) % 2))
        return info_states

    @property
    def is_leaf(self) -> bool:
        """Returns True if node has no children."""
        return self.children is None or len(self.children) == 0

    def build_children(self) -> None:
        """
        Builds the children nodes for all valid actions from this state.
        """
        
        # If the game is over, there are no children
        if self.state.is_over:
            return None
        
        self.children = {}
        
        # If cards are not dealt, build children for all possible card combinations
        if not self.state.cards_dealt:
            deck = Deck(self.state.game_rules.deck_size)
            for cards in permutations(deck.cards, 2):
                new_state = self.state.clone()
                new_state.players[0].card = cards[0]
                new_state.players[1].card = cards[1]
                self.children[cards] = GameNode(new_state)
            return None
        
        # Otherwise, build children for all valid actions
        valid_actions = get_valid_actions(self.state)
        
        for action in valid_actions:
            new_state = self.state.clone()
            process_action(new_state, action)
            self.children[action] = GameNode(new_state)
    
    def __iter__(self):
        """
        Enables iteration through all nodes in the tree using depth-first traversal.
        Yields each GameNode object in the tree, starting with self.
        """
        yield self
        if self.children:
            for child in self.children.values():
                yield from child
    
    def __str__(self, depth=0) -> str:
        result = ["  " * depth + str(self.state)]
        if not self.is_leaf:
            for action, child in self.children.items():
                result.append("  " * depth + f"-> {action}")
                result.append(child.__str__(depth + 1))
        return "\n".join(result)


def build_game_tree(config: GameConfig) -> GameNode:
    """
    Builds a game tree for the given game configuration.
    Returns the root node of the tree.
    """
    state = HandState(game_rules=config)
    root = GameNode(state)
    
    def build_recursive(node: GameNode) -> None:
        if node.state.is_over:
            return
            
        node.build_children()
        
        for child_node in node.children.values():
            build_recursive(child_node)
    
    build_recursive(root)
    return root







