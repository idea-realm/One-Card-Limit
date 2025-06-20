from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.cfr_strategy import CFRStrategy
from one_card_limit.strategy.base_strategy import get_strategy_path

# Configure the game
config = GameConfig(deck_size=4, max_raises=1)
cfr = CFRStrategy(config)
num_iterations = 10000

# Train using the train method (cleaner approach)
cfr.train(num_iterations)

# The policy is now automatically updated with the average strategy
# Print strategy for each specific info state/card
cfr.policy.show_by_card()

# Save the trained strategy with config-specific name
strategy_path = get_strategy_path(config)
cfr.save(str(strategy_path))
