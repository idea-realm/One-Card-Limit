from one_card_limit.interface import GameManager
from one_card_limit.core import GameConfig
from one_card_limit.strategy.base_strategy import Strategy, get_strategy_path

def main():
    # Create game with custom configuration
    config = GameConfig(
        deck_size=3,    # Number of cards in deck (3-13)
        max_raises=2    # Maximum number of raises allowed (0-2)
    )
    
    # Load the trained strategy for this specific configuration
    strategy_path = get_strategy_path(config)
    if strategy_path.exists():
        computer_strategy = Strategy.load(strategy_path)
    else:
        print(f"No trained strategy found for deck_size={config.deck_size}, max_raises={config.max_raises}")
        print("Using random strategy instead")
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

