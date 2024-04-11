from hand import Game, Human, Computer

def get_user_input(prompt, input_type=int, condition=lambda x: True, error_message="Invalid input. Please try again."):
    while True:
        try:
            user_input = input_type(input(prompt))
            if condition(user_input):
                return user_input
            else:
                print(error_message)
        except ValueError:
            print(error_message)
            
def start_game():
    start = input("Enter any input to begin game: ").lower()
    if start == ValueError:
        print("Game not started. Exiting...")
        return

    deck_size = get_user_input("Choose a deck size: ", int, lambda x: x > 0 and x < 14, "Deck size must be between 3 and 13")
    max_raises = get_user_input("Enter maximum number of raises: ", int, lambda x: x >= 0, "Maximum number of raises must be a non-negative integer.")

    print(f"Starting game with deck size {deck_size} and maximum {max_raises} raises.")
    hand_num = 0
    stacks = [100,100]
    # Main game loop
    play_again = True
    while play_again:
        hand = Game(deck_size,max_raises)
        
        print("Game is running...")
        game_players = (Human(0,"OP"),Computer(1,"IP"))
        hand = hand.play_hand(game_players[hand_num], game_players[(hand_num + 1) % 2])
        stacks[0] += hand.result
        stacks[1] -= hand.result
        
        print("*-------------------*")
        print("Current Stacks:")
        print(f"You: {stacks[0]}")
        print(f"Computer: {stacks[1]}")
        print("*-------------------*")

        # Ask the user if they want to play another hand
        end_game = get_user_input("Do you want to stop? (y/n): ", str, lambda x: x in ["y", "n"], "please enter 'y' or 'n'")

        if end_game == "y":
            play_again == False
        hand_num += 1 
        
    print("Game ended.")
            
if __name__ == "__main__":
    start_game()
    
    




