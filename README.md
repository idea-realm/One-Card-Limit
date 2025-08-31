# One Card Limit Poker

A Python implementation of One Card Limit Poker, featuring both human and AI players. This project implements a simplified poker variant that's well-suited for studying the game theory of poker and training AI strategies.

## Features
- Human vs Computer gameplay via CLI
- Built-in strategy framework
- Counterfactual Regret Minimization (CFR) implementation
- Game state logging

## Game Rules

One Card Limit Poker is a simplified poker variant where:
1. 2 players are each dealt a card from a deck of size N, ranging from N = 3 {A, K, Q} to N = 13 {A, K, Q, ..., 2}
2. Both players ante a small amount (default is 1)
3. The player to act first is designated as OP (out of position), the player second to act is IP (in position)
4. Players take turns betting with the following options:
   - Check, if no bet was made
   - Bet, if no bet was made (bet size is same value as the ante)
   - Raise, facing a bet (raise size is 2 times the current bet)
   - Call, match the currnt bet
   - Fold, give up the hand
5. After betting is complete, the player with the higher card wins
6. Maximum raises can be configured (default is 2)

### Example hand:
- OP is dealt A, IP is dealt Q, both players Ante 1 chip (pot=2)
- OP Bets 1 chip (pot=3) → IP Raises 2 chips (pot=5) → OP Calls 2 chips (pot=7)
- OP wins (A > Q) pot of 7 chips (net win of 6 chips after ante)
  
## Installation

```bash
# Clone the repository
git clone https://github.com/idea-realm/One-Card-Limit.git
cd one_card_limit

# Install
pip install -e .
```

## Quick Start

### Training an AI Strategy

First, train a strategy using Counterfactual Regret Minimization (CFR):

```python
from one_card_limit.core import GameConfig
from one_card_limit.strategy import CFRStrategy
from pathlib import Path

# Configure the game
config = GameConfig(deck_size=3, max_raises=2)

# Create and train the CFR strategy
cfr = CFRStrategy(config)
num_iterations = 100000

# Train the strategy
for i in range(num_iterations):
    if i % 1000 == 0:
        print(f"Training progress: {i}/{num_iterations}")
    cfr._cfr_iteration()

# Save the trained strategy
strategy_path = Path("trained_strategies/cfr_strategy_3card.pkl")
strategy_path.parent.mkdir(exist_ok=True)
cfr.save(strategy_path)
```

### Playing Against the AI

After training, you can play against the AI using the command-line interface:

```python
from one_card_limit.interface import GameManager
from one_card_limit.core import GameConfig
from one_card_limit.strategy import Strategy
from pathlib import Path

# Load configuration and strategy
config = GameConfig(deck_size=3, max_raises=2)
strategy_path = Path("trained_strategies/cfr_strategy_3card.pkl")
computer_strategy = Strategy.load(strategy_path) if strategy_path.exists() else Strategy(config)

# Initialize game
game = GameManager(
    initial_stack=100,
    config=config,
    computer_strategy=computer_strategy,
    log_enabled=True
)

# Play 5 hands
game.play_session(5)
```

## Project Structure
```
one_card_limit/
├── core/         # Core game mechanics
│   ├── game_logic.py  # Core game rules and logic
│   └── state.py       # Game state management
├── strategy/     # AI strategy implementation
│   ├── base_strategy.py  # Base strategy class
│   ├── cfr_strategy.py  # CFR implementation
│   ├── game_tree.py     # Game tree builder
│   └── info_set.py      # Information set representation
├── interface/    # User interface components
│   ├── cli.py          # Command line interface
│   └── game_manager.py # Game flow management
└── utils/        # Utility functions and logging
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
