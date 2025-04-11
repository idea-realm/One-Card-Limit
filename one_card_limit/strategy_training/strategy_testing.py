from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.cfr_strategy import CFRStrategy
from pathlib import Path

config = GameConfig(deck_size=3, max_raises=2)
cfr = CFRStrategy(config)
num_iterations = 100000

# During training
for i in range(num_iterations):
    if i % 1000 == 0:
        print(f"Training progress: {i}/{num_iterations}")
    cfr._cfr_iteration()

# Get the final average strategy
final_strategy = cfr.get_average_strategy()

# Print strategy for specific info state
for info_state, action_probs in final_strategy.items():
    print(info_state, {action: format(prob, '.2%') for action, prob in action_probs.items()})
    
# Save the trained strategy
strategy_path = Path("trained_strategies/cfr_strategy_3card.pkl")
cfr.save(strategy_path)