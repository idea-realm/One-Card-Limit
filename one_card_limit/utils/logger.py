# utils/logger.py
"""
This module provides the `GameLogger` class, which is responsible for logging events
in a simple poker game. It includes methods to log the start and end of a game session,
details of each hand, player actions, and the final results.
"""

# Standard Imports
from time import sleep
# Local Imports
from ..core.state import Action, HandState

class GameLogger:
    """
    Handles logging of game events
    """
    def __init__(self, initial_stack: int):
        self.initial_stack = initial_stack
        self.human_starting_stack = initial_stack
        self.computer_starting_stack = initial_stack

    def log_session_start(self, human_stack: int, computer_stack: int) -> None:
        print("\n=== New Game Session ===")
        print(f"Initial stacks - Human: {human_stack}, Computer: {computer_stack}")
    
    def log_session_end(self, human_stack: int, computer_stack: int) -> None:
        print("\n=== Session Complete ===")
        print(f"Final stacks - Human: {human_stack}, Computer: {computer_stack}")
        print(f"Net profit - Human: {human_stack - self.human_starting_stack}, Computer: {computer_stack - self.computer_starting_stack}")

    def log_hand_header(self, hand_num: int, total_hands: int, human_pos: int) -> None:
        print(f"\n--- Hand {hand_num}/{total_hands} ---")
        print(f"You are {'IP' if human_pos == 1 else 'OP'}")
    
    def log_hand_start(self) -> None:
        print(f"Cards dealt, Antes Posted")
        sleep(2)
    
    def log_state(self, state: HandState) -> None:
        print(f"Pot is: {state.pot}, Current bet: {state.current_bet}")

    def log_hand_end(self, state: HandState, human_stack: int, computer_stack: int) -> None:
        if state.is_over:
                if state.showdown:
                    print("Showdown:")
                    for player in state.players:
                        sleep(2)
                        print(f"{player.name} shows: {player.card}")
                if state.winner_pos is not None:
                    sleep(1)
                    print(f"{state.players[state.winner_pos].name} wins {state.pot}")
        sleep(1)
        print(f"Hand over")
        print(f"Stacks - Human: {human_stack}, Computer: {computer_stack}")
        print("----------------")

    def log_action_message(self, state: HandState) -> None:
        sleep(1)
        if state.actions_taken != []:    
            # Get message for current action
            last_action = state.actions_taken[-1][1]
            last_action = last_action.value.capitalize()
            last_player = state.players[(state.acting_pos + 1) % 2].name
            msg = f"{last_player} {last_action}s"
            if last_action in [Action.RAISE, Action.BET]:
                msg += (f" to {state.current_bet}")
            elif last_action == Action.CALL:
               msg += (f" {state.current_bet}")
            print(msg)