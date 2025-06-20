from one_card_limit.core.state import GameConfig
from one_card_limit.strategy.cfr_strategy import CFRStrategy
from one_card_limit.strategy.base_strategy import Strategy, get_strategy_path

def main():
    # Create game configuration
    config = GameConfig(
        deck_size=4,    # Number of cards in deck (3-13)
        max_raises=2    # Maximum number of raises allowed (0-2)
    )
    
    print("=== Policy Class Usage Examples ===\n")
    
    # Try to load a trained CFR strategy, or create random if not available
    strategy_path = get_strategy_path(config)
    
    if strategy_path.exists():
        print("Loading trained CFR strategy...")
        strategy = CFRStrategy.load(str(strategy_path))
        print(f"Loaded strategy with {len(strategy.policy)} information states\n")
    else:
        print("No trained strategy found, creating random strategy...")
        strategy = Strategy(config)
        print(f"Created random strategy with {len(strategy.policy)} information states\n")
    
    # Example 1: Basic policy display
    print("1. Basic Policy Display (first 5 entries):")
    strategy.policy.show(max_entries=5)
    print()
    
    # Example 2: Show policy grouped by card
    print("2. Policy Grouped by Card:")
    strategy.policy.show_by_card()
    print()
    
    # Example 3: Show policy for specific card only
    print("3. Policy for Ace only:")
    strategy.policy.show_by_card(card_filter="A")
    print()
    
    # Example 4: Get strategy summary
    print("4. Strategy Summary:")
    summary = strategy.policy.get_action_summary()
    print(f"Total information states: {summary['total_states']}")
    print("Action distribution (most likely action per state):")
    for action, count in summary['action_distribution'].items():
        percentage = (count / summary['total_states']) * 100
        print(f"  {action}: {count} states ({percentage:.1f}%)")
    print()
    
    # Example 5: Access specific information states
    print("5. Accessing Specific Information States:")
    print("Available information states:")
    for i, info_state in enumerate(strategy.policy.keys()):
        if i >= 3:  # Show first 3 only
            break
        action_probs = strategy.policy[info_state]
        print(f"  {info_state}: {action_probs}")
    print()
    
    # Example 6: Check if info state exists
    print("6. Checking Information State Existence:")
    first_info_state = next(iter(strategy.policy.keys()))
    print(f"Does {first_info_state} exist in policy? {first_info_state in strategy.policy}")
    print()
    
    # Example 7: Iterate through policy
    print("7. Iterating Through Policy (first 3 entries):")
    for i, (info_state, action_probs) in enumerate(strategy.policy.items()):
        if i >= 3:
            break
        best_action = max(action_probs.items(), key=lambda x: x[1])
        print(f"  {info_state}: Best action is {best_action[0].name} ({best_action[1]:.1%})")
    print()
    
    # Example 8: Convert to/from dictionary
    print("8. Converting Policy to Dictionary:")
    policy_dict = strategy.policy.to_dict()
    print(f"Policy dictionary has {len(policy_dict)} entries")
    
    # Create new policy from dictionary
    new_policy = strategy.policy.from_dict(policy_dict)
    print(f"New policy created from dictionary has {len(new_policy)} entries")
    print()
    
    # Example 9: Policy string representation
    print("9. Policy String Representation:")
    print(f"Policy object: {strategy.policy}")
    print(f"Policy length: {len(strategy.policy)}")

if __name__ == "__main__":
    main()
