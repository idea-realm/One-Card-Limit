import random

class Player:
    def __init__(self, name, stack_size):
        self.name = name
        self.stack_size = stack_size
        self.card = None

class HumanPlayer(Player):
    def __init__(self, name, stack_size):
        super().__init__(name, stack_size)
        
    def decide_action(self, hand_state, actions):
        print(f"You have {self.card.rank}")
        while True:
            for i, action in enumerate(actions, start=1):
                print(f"{i}. {action}")
            try:
                selection = int(input("Select an action: "))
                if 1 <= selection <= len(actions):
                    print("---------------------")
                    return actions[selection - 1]
                else:
                    print("Please select a valid action.")
            except ValueError:
                print("Please enter a number.")

class ComputerPlayer(Player):
    def __init__(self, name, stack_size, strategy):
        super().__init__(name, stack_size)
        self.strategy = strategy

    def decide_action(self, hand_state, actions):
        strategy_key = (self.card.rank, hand_state)
        probabilities = self.strategy.get(strategy_key, None)
        if probabilities:
            action = random.choices(actions, weights=probabilities)[0]
        else:
            action = random.choice(actions)
        return action
