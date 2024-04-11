from pokergame import Hand, Player
import os, time

if __name__ == "__main__":
    players = [
        Player("Player 1"),
        Player("Player 2")
    ]
    for i in range(10):
        print(f"Hand {i+1}")
        for player in players: 
            print(f"{player.name}, {player.stack_size}") 
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        IP = players[i % 2]
        OP = players[(i + 1) % 2]
        hand = Hand([IP,OP], max_raises = 2)
        
        hand.play_hand()
        time.sleep(5)
        os.system('cls')
        
