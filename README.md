# One Card Limit Poker (Work in Progress)

A Python implementation of One Card Limit Poker, featuring game theory analysis and AI strategy development. This project implements a simplified poker variant that's well-suited for studying poker fundamentals and experimenting with game-theoretic algorithms.

## Current Status
🚧 **This project is a work in progress** 🚧

Currently implemented:
- ✅ Core game mechanics and state management
- ✅ Strategy framework with Policy class
- ✅ Counterfactual Regret Minimization (CFR) implementation
- ✅ Game tree building and information set handling
- ✅ Strategy training and serialization

In development:
- 🔄 Command-line interface for human vs AI gameplay
- 🔄 Game session management
- 🔄 Comprehensive testing and validation

## Game Rules

One Card Limit Poker is a simplified poker variant where:
1. 2 players are each dealt a card from a deck of size N (configurable from 3 to 13 cards)
2. Both players ante a small amount (default is 1 chip)
3. The first player to act is designated as OP (out of position), the second is IP (in position)
4. Players take turns with these betting options:
   - **Check**: Pass if no bet has been made
   - **Bet**: Make the first bet (equal to ante size)
   - **Raise**: Increase the bet (raise size configurable)
   - **Call**: Match the current bet
   - **Fold**: Give up the hand
5. After betting, the player with the higher card wins the pot
6. Maximum number of raises is configurable (0-2)

### Example Hand:
- OP dealt A, IP dealt Q, both ante 1 chip (pot = 2)
- OP bets 1 chip (pot = 3) → IP raises 2 chips (pot = 5) → OP calls 2 chips (pot = 7)
- OP wins with A > Q, taking the 7-chip pot

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd SimplePokerGame

# Install in development mode
pip install -e .
```

## Usage Examples

### Training a CFR Strategy

```python
from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.cfr_strategy import CFRStrategy
from one_card_limit.strategy.base_strategy import get_strategy_path

# Configure the game
config = GameConfig(deck_size=4, max_raises=2)

# Create and train CFR strategy
cfr_strategy = CFRStrategy(config)
cfr_strategy.train(iterations=10000)

# Save the trained strategy
strategy_path = get_strategy_path(config)
cfr_strategy.save(str(strategy_path))
print(f"Strategy saved to {strategy_path}")

# Show the strategy
print("\nSample strategies:")
cfr_strategy.policy.show_by_card()
```

### Playing Against the AI (CLI Interface)

*Note: CLI interface is currently in development*

```python
from one_card_limit.interface.cli import play_game
from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.base_strategy import Strategy

# Configure game and load strategy
config = GameConfig(deck_size=4, max_raises=1)
computer_strategy = Strategy.create_or_load(config, strategy_type="cfr")

# Start interactive game session
play_game(
    config=config,
    computer_strategy=computer_strategy,
    initial_stack=100,
    num_hands=10
)
```

**Example CLI Session:**
```
=== One Card Limit Poker ===
Configuration: 4-card deck, max 1 raise
Starting stacks: You: 100, Computer: 100

Hand #1
Your card: K
Actions: [] (no actions yet)
Pot: 2 (both players ante 1)

Your turn - Available actions:
1. Check
2. Bet (1 chip)
Enter your choice (1-2): 2

You bet 1 chip. Pot: 3
Computer's turn...
Computer raises 2 chips! Pot: 5

Your card: K
Actions: [BET, RAISE] 
Current bet to you: 2 chips

Your turn - Available actions:
1. Call (2 chips)
2. Fold
Enter your choice (1-2): 1

You call 2 chips. Pot: 7
Showdown: Your K vs Computer's A
Computer wins with A > K

Final result: You: 96, Computer: 104
Continue? (y/n): y
```

## Project Structure

```
one_card_limit/
├── core/                    # Core game mechanics
│   ├── game_logic.py       # Game rules and action processing
│   └── state.py            # Game state and configuration
├── strategy/               # Strategy implementation
│   ├── base_strategy.py    # Strategy and Policy classes
│   ├── cfr_strategy.py     # CFR algorithm implementation
│   ├── game_tree.py        # Game tree construction
│   └── info_set.py         # Information set representation
├── interface/              # User interfaces (in development)
└── examples/               # Example scripts and usage
    ├── train_strategy.py   # Strategy training example
    └── show_strategy.py    # Strategy analysis example
```

## Configuration Options

The game can be configured with different parameters:

```python
config = GameConfig(
    deck_size=4,     # Number of cards (3-13)
    max_raises=1     # Maximum raises allowed (0-2)
)
```

Common configurations:
- `GameConfig(deck_size=3, max_raises=2)` - Simple 3-card game
- `GameConfig(deck_size=13, max_raises=1)` - Full deck, limited betting
- `GameConfig(deck_size=4, max_raises=0)` - 4-card game, bet/call only

## Contributing

This is a work-in-progress project. Contributions, suggestions, and feedback are welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)
