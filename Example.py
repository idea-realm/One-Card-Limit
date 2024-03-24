from pokergame import Hand, HumanPlayer, ComputerPlayer
from strategy import strategy
import os, time


if __name__ == "__main__":
    
    players = [
        HumanPlayer("Human", 100),
        ComputerPlayer("AI", 100, strategy)
    ]

    for i in range(20):
        print(f"Hand {i+1}")
        for player in players: 
            print(f"{player.name}, {player.stack_size}") 
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        IP = players[i % 2]
        OP = players[(i + 1) % 2]
        hand = Hand(ante=1, bet_size=1)
        hand.play_hand(IP, OP)
        
        time.sleep(3)
        os.system('cls')
        
        