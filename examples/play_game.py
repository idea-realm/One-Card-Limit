from one_card_limit.interface import GameManager
from one_card_limit.core import GameConfig
from one_card_limit.strategy import Strategy
from pathlib import Path

def main():
    # Create game with custom configuration
    config = GameConfig(
        deck_size=3,    # Number of cards in deck (3-13)
        max_raises=2    # Maximum number of raises allowed (0-2)
    )
    
    # Load the trained strategy
    strategy_path = Path("trained_strategies\cfr_strategy_3card.pkl")
    if strategy_path.exists():
        computer_strategy = Strategy.load(strategy_path)
    else:
        print("No trained strategy found, using random strategy")
        computer_strategy = Strategy(config)
    
    # Initialize game manager with the loaded strategy
    game = GameManager(
        initial_stack=100,
        config=config,
        computer_strategy=computer_strategy,
        log_enabled=True
    )
    
    # Play 5 hands
    try:
        game.play_session(5)
    except KeyboardInterrupt:
        print("\nGame session terminated by user")
        print(f"Final stacks - Human: {game.human_stack}, Computer: {game.computer_stack}")

if __name__ == "__main__":
    main()
