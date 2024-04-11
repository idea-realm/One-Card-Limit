from hand import Hand, Human, Computer

if __name__ == "__main__":
    hand = Hand(5,2)
    tree = hand.get_game_tree()
    print(tree)
    human = Human(0,"OP")
    computer = Computer(1,"IP")
    this_hand = hand.play_hand(human, computer)
    print(this_hand)