# core/human_player.py
from .action import Action
from .state import HandState
from .strategy import Strategy

class HumanStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, state: HandState) -> Action:
        self.display_game_info(state)
        while True:
            try:
                action_str = input("Enter your action: ").strip().upper()
                action = Action[action_str]
                return action
            except ValueError:
                print("Invalid action. Please enter a valid action.")

    def display_game_info(self, state : HandState):
        valid_actions = state.valid_actions
        print(f"Your card: {state.players[state.acting_pos].card}")
        print(f"Valid actions: {', '.join([action.name for action in valid_actions])}")