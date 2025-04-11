# One Card Limit Poker

A Python implementation of One Card Limit Poker, featuring both human and AI players. This project implements a simplified poker variant that's well-suited for studying the game theory of poker and training AI strategies.

## Game Rules

One Card Limit Poker is a simplified poker variant where:
1. Each player is dealt one card from a deck of N cards (default N=3)
2. Players take turns betting with the following options:
   - Check (when no bet is made)
   - Bet/Raise (up to a maximum number of raises)
   - Call (match the current bet)
   - Fold (give up the hand)
3. After betting is complete, the player with the higher card wins
4. Maximum raises can be configured (default is 2)

### Betting Structure
- Each hand starts with a small ante (default 1 chip)
- Bet size is same as the ante, raise is double the current bet
- Example hand: Both players Ante 1 chip (pot=2) → OP Bets 1 chip (pot=3) → IP Raises 2 chips (pot=5) → OP Calls 2 chips (pot=7) : Winning Player gets pot (7 chips, net win of 6 chips after ante)

## Installation

```bash
# Clone the repository
git clone https://github.com/idea-realm/Simple-Poker-Game.git
cd one_card_limit

# Install in development mode
pip install -e ".[dev]"
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
│   ├── action.py       # Game actions (bet, call, fold, etc.)
│   ├── card.py        # Card and deck implementations
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

## Features
- Configurable deck size (3-13 cards)
- Adjustable maximum raises (0-2)
- Human vs Computer gameplay via CLI
- Built-in strategy framework
- Counterfactual Regret Minimization (CFR) implementation
- Game state logging
- Extensible architecture for new strategies

## Development

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
