from one_card_limit.interface.game_manager import GameManager
from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.base_strategy import Strategy

def main():
    # Create game with custom configuration
    config = GameConfig(
        deck_size=4,    # Number of cards in deck (3-13)
        max_raises=2    # Maximum number of raises allowed (0-2)
    )
    
    # Use factory method to create or load strategy
    # This will automatically train a new strategy if one doesn't exist
    try:
        computer_strategy = Strategy.create_or_load(
            config, 
            strategy_type="cfr", 
            train_iterations=5000  # Adjust iterations as needed
        )
    except Exception as e:
        print(f"Error creating strategy: {e}")
        print("Falling back to random strategy")
        computer_strategy = Strategy(config)
    
    # Initialize game manager with the loaded strategy
    game = GameManager(
        initial_stack=100,
        config=config,
        computer_strategy=computer_strategy,
        log_enabled=True
    )
    
    # Play 3 hands
    try:
        game.play_session(3)
    except KeyboardInterrupt:
        print("\nGame session terminated by user")
        print(f"Final stacks - Human: {game.human_stack}, Computer: {game.computer_stack}")

if __name__ == "__main__":
    main()

