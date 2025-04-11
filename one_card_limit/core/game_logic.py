# game_logic.py
from typing import List
from .state import HandState
from .card import Deck
from .action import Action

def deal_cards(state: HandState) -> None:
    deck = Deck(state.game_rules.deck_size)
    deck.shuffle()
    for player in state.players:
        player.card = deck.deal_card()
    return None

def get_valid_actions(state: HandState) -> List[Action]:
    if not state.cards_dealt or state.is_over:
        return []
    if state.current_bet == 0:
        return [Action.CHECK, Action.BET]
    else:
        valid = [Action.CALL, Action.FOLD]
        if state.raises_made < state.game_rules.max_raises:
            valid.append(Action.RAISE)
        return valid

def process_action(state: HandState, action: Action) -> None:
    """
    Updates the game state based on the action taken by the current player
    """
    if state.is_over:
        raise ValueError("Hand is already over")
    
    elif not state.cards_dealt:
        raise ValueError("Cards have not been dealt yet")
    
    valid = get_valid_actions(state)
    if action not in valid:
        raise ValueError(f"Invalid action {action}, valid: {valid}")

    # Record the action in the history
    state.actions_taken.append((state.acting_pos, action))

    match action:
        case Action.CHECK:
            handle_check(state)
        case Action.BET:
            handle_bet(state)
        case Action.CALL:
            handle_call(state)
        case Action.RAISE:
            handle_raise(state)
        case Action.FOLD:
            handle_fold(state)
            
    # Switch to next player
    state.acting_pos = (state.acting_pos + 1) % 2
    
    # If the hand is over, finalize outcomes
    if state.is_over:
        return end_hand(state)
        

def handle_check(state: HandState) -> None:
    if state.acting_pos == 1:
        state.is_over = True
        state.showdown = True
        return None
    else:
        return None

def handle_bet(state: HandState) -> None:
    state.current_bet = state.game_rules.ante
    state.pot += state.current_bet
    state.acting_player.stack -= state.current_bet
    return None

def handle_call(state: HandState) -> None:
    state.pot += state.current_bet
    state.acting_player.stack -= state.current_bet
    state.is_over = True
    state.showdown = True

def handle_raise(state: HandState) -> None:
    if state.raises_made < state.game_rules.max_raises:
        new_bet = state.current_bet * 2
        state.current_bet = new_bet
        state.pot += new_bet
        state.acting_player.stack -= new_bet
        state.raises_made += 1
    else:
        raise ValueError("No raises left, can't raise")

def handle_fold(state: HandState) -> None:
    state.winner_pos = (state.acting_pos + 1) % 2
    state.is_over = True
    return None

def end_hand(state: HandState) -> None:
    state.is_over = True
    # Determine winner
    if state.showdown:
        state.winner_pos = max(state.players, key=lambda player: player.card).pos

    # Award pot to winner
    state.players[state.winner_pos].stack += state.pot