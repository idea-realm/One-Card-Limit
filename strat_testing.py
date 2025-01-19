from onecardlimit import Game, Strategy

def generate_strategy_for_game(game: Game) -> Strategy:
    all_states = game.all_states
    action_probabilities = {}

    for state in all_states:
        valid_actions = state.get_valid_actions()
        if valid_actions is not None:    # Check if state is terminal
            num_actions = len(valid_actions)
            probabilities = {action: 1.0 / num_actions for action in valid_actions}
            action_probabilities[state] = probabilities

    return Strategy(action_probabilities)

# Example usage
deck_size = 5
max_raises = 1
game = Game(deck_size, max_raises)
strategy = generate_strategy_for_game(game)
print(strategy)