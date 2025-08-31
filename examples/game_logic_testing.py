from one_card_limit.core.game_logic import Action, Card, GameConfig, HandState, InfoState, generate_all_handstates, generate_handstate_infostates
from typing import Dict, List

config = GameConfig(deck_size=3, max_raises=2, ante= 2)
combos = config.get_all_card_combos()
print("All possible card combinations:", combos)
all_handstates = generate_all_handstates(config)
print(f"Generated {len(all_handstates)} hand states and info states.")
actions: Dict[str, List[List]] = {}
for handstate in all_handstates:
    if handstate.is_over:
        action_str = "".join(str(action) for action in handstate.actions)
        if action_str not in actions:
            actions[action_str] = []
        actions[action_str].append(handstate.stacks)
        
print("Unique action sequences and corresponding stack states:")
for action_seq, stacks in actions.items():
    print(f"Actions: {action_seq} -> Stack States: {stacks}")

        

