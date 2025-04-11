from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.game_tree import build_game_tree
from one_card_limit.strategy.base_strategy import Strategy


# Create initial game state with specific cards
config = GameConfig(deck_size=3, max_raises=2)

# Build game tree
game_tree = build_game_tree(config)

for node in game_tree:
    print(node.state)
    print("\n".join([str(info_state) for info_state in node.info_state]))
    print("-----------")

# Print the game tree
print(game_tree)

strategy = Strategy(config)
for key, value in strategy.policy.items():
    print(key, value)
