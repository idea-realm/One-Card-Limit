from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.cfr_strategy import CFRStrategy
from one_card_limit.strategy.base_strategy import get_strategy_path

def main():
    # Create game configuration
    config = GameConfig(
        deck_size=4,    # Number of cards in deck (3-13)
        max_raises=2    # Maximum number of raises allowed (0-2)
    )
    
    # Create CFR strategy
    cfr_strategy = CFRStrategy(config)
    
    # Train the strategy
    iterations = 10000  # More iterations for better convergence
    cfr_strategy.train(iterations)
    
    # Save the trained strategy
    strategy_path = get_strategy_path(config)
    cfr_strategy.save(str(strategy_path))
    print(f"Strategy saved to {strategy_path}")
    
    # Show the strategy
    print("\nSample strategies:")
    cfr_strategy.policy.show_by_card()


if __name__ == "__main__":
    main()
