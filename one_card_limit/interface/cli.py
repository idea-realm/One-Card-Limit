# interface/cli.py
"""
This module contains a function, `get_human_action(state: HandState)` that prompts a user to input an action. 
"""
# Local Imports
from ..core.game_logic import Action, HandState

def get_human_action(state: HandState) -> Action:
    """
    Get action from human player via command line
    """
    print(f"\nYour card: {state.cards[state.acting_pos]}")
    valid_actions = state.get_valid_actions()
    print(f"Valid actions: {', '.join(a.name for a in valid_actions)}")
    
    while True:
        try:
            action_str = input("Enter your action: ").strip().upper()
            action = Action[action_str]
            if action in valid_actions:
                return action
            else:
                print("Invalid action. Please choose from the valid actions.")
        except (KeyError, ValueError):
            print("Invalid input. Please enter a valid action name.")