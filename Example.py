from player import HumanPlayer, ComputerPlayer
from pokergame import Hand
from strategy import strategy
import os, time


if __name__ == "__main__":
    
    players = [
        HumanPlayer("Human", 100),
        ComputerPlayer("Computer", 100, strategy)
    ]

    for i in range(20):
        print(f"Hand {i+1}")
        for player in players: 
            print(f"{player.name}, {player.stack_size}") 
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        IP = players[i % 2]
        OP = players[(i + 1) % 2]
        Hand(IP = IP, OP = OP, ante=1, bet_size=1)
        
        time.sleep(3)
        os.system('cls')
        
        