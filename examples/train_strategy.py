from one_card_limit.core.game_logic import GameConfig
from one_card_limit.strategy.cfr_strategy import CFRStrategy

def main():
    # Create game configuration
    config = GameConfig(
        deck_size=5,    # Number of cards in deck (3-13)
        max_raises=1    # Maximum number of raises allowed (0-2)
    )
    
    # Create CFR strategy
    cfr_strategy = CFRStrategy(config)
    
    # Train the strategy
    iterations = 10000  # More iterations for better convergence
    strategy = cfr_strategy.train(iterations)
    
    # Save the trained strategy
    
    strategy.save()
    print(f"Strategy saved")
    
    # Show the strategy
    print("\nSample strategies:")
    strategy.show_policy()


if __name__ == "__main__":
    main()
