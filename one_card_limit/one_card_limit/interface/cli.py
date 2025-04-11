from ..core.state import HandState
from ..core.action import Action
from ..core.game_logic import get_valid_actions

def get_human_action(state: HandState) -> Action:
    """Get action from human player via command line"""
    print(f"\nYour card: {state.players[state.acting_pos].card}")
    valid_actions = get_valid_actions(state)
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