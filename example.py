from one_card_limit import *

stacks = [100, 100]
for _ in range(10):
    test = OneCardLimitGame(5, 3)
    Players = [Strategy(), Strategy()]
    test.start_hand()
    while not test.is_complete:
        action = Players[test.acting_player.pos].get_action(test.state)  # Get action from the strategy for the current player
        test.next_action(action)
        print(test.dealer_message())
    stacks[0] += test.players[0].stack
    stacks[1] += test.players[1].stack
    print(stacks)