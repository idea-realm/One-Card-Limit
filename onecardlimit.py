from cards import Card, Deck
from enum import Enum
from typing import Tuple, Dict
import random, time

class Action(Enum):
    CHECK = 1
    RAISE = 2
    CALL = 3
    FOLD = 4
    def __str__(self) -> str:
        return self.name.lower()
    def __repr__(self) -> str:
        if self.name == "CHECK":
            return "x"
        else:
            return self.name.lower()[0]

class HandPlayer:
    def __init__(self, pos: int, card: Card, stack: int) -> None:
        self.pos = pos
        self.card = card
        self.stack = stack
        self.name = ["OP", "IP"][self.pos]

    def __eq__(self, __value: object) -> bool:
        return (self.card == __value.card) and (self.stack == __value.stack) and (self.pos == __value.pos)
    
    def __hash__(self) -> int:
        return hash((self.pos, self.card, self.stack))
   
    def __str__(self) -> str:
        return self.name

class HandState:  
    def __init__(self, cards: Tuple[Card], stacks: Tuple[int, int], actions: Tuple[Action] = [], max_raises: int = 2) -> None:
        ante = 1
        self.cards = cards
        self.players = tuple([HandPlayer(i, self.cards[i], stacks[i] - ante) for i in [0,1]])
        self.actions = actions
        self.max_raises = max_raises
        self.pot = 2 * ante
        self.raise_size = ante
        self.curr_bet = 0
        self.raises = 0
        self.is_over = False
        self.winner: int
        self.result: int
        self.acting_pos = 0
        
        if self.actions:
            for action in self.actions:
                if action == Action.RAISE:
                    self.pot += self.raise_size + self.curr_bet
                    self.players[self.acting_pos].stack -= (self.raise_size + self.curr_bet)
                    self.curr_bet = self.raise_size
                    self.raises += 1
                    self.raise_size *= 2
                elif action == Action.CALL:
                    self.pot += self.curr_bet
                    self.players[self.acting_pos].stack -= self.curr_bet
                    self.is_over = True
                elif action == Action.CHECK and self.acting_pos == 1:
                    self.is_over = True
                elif action == Action.FOLD:
                    self.is_over = True
                
                if self.is_over:
                    if action != Action.FOLD:
                        self.winner = max([0,1], key = lambda pos: self.players[pos].card.val)
                    else:
                        self.winner = (self.acting_pos + 1) % 2
                    self.players[self.winner].stack += self.pot
                    self.result = self.players[0].stack - stacks[0]
                
                self.acting_pos = (self.acting_pos + 1) % 2      
    
    def get_next_state(self, action: Action) -> 'HandState':
        if action not in self.get_valid_actions():
            raise ValueError(f"Invalid action: {action.name}")
        new_actions = self.actions + [action]
        return HandState(self.cards, (self.players[0].stack, self.players[1].stack), new_actions)
    
    def get_valid_actions(self) -> tuple[Action]:
        if not self.actions or self.actions[-1] == Action.CHECK:
            return (Action.CHECK, Action.RAISE)
        if self.actions[-1] == Action.RAISE:
            options = [Action.CALL, Action.FOLD]
            if self.raises < self.max_raises:
                options.append(Action.RAISE)
            return tuple(options)
       
    def __eq__(self, othr):
        is_same_cls = isinstance(othr, type(self))
        is_same_state = ((self.players == othr.players) and (self.actions == othr.actions))
        return is_same_cls and is_same_state
        
    def __hash__(self):
        return hash((self.players, tuple(self.actions)))
    
    def __str__(self) -> str:
        if self.actions:
            action_str = [action.name.lower() for action in self.actions]
        else:
            action_str = "[]"
        state =  f"{self.players[0].card}, {self.players[1].card}, {action_str}"
        if self.is_over:
            state += " " + str(self.players[0].stack)
        return state

    def __repr__(self) -> str:
        cards = [str(player.card) for player in self.players]
        actions = [repr(action) for action in self.actions]
        state_string = cards + actions
        if self.is_over:
            state_string += "->" + str(self.result)
        return f"handstate({''.join(state_string)})"

    def dealer_message(self) -> None:
        if self.actions:
            last_action = self.actions[-1]
            last_player = self.players[(self.acting_pos + 1) % 2]
            match last_action:
                case Action.CHECK:
                    print(f"{last_player} checks")
                case Action.CALL:
                    print(f"{last_player} calls {self.curr_bet}")
                case Action.RAISE:
                    print(f"{last_player} raises to {self.raise_size}, {self.curr_bet} to call")
                case Action.FOLD:
                    print(f"{last_player} folds")
        else:
            print("Antes posted, cards dealt")
            
        if self.is_over:    
            if last_action != Action.FOLD:
                print("---SHOWDOWN---")
                msg = [f"{player.name} shows {player.card}" for player in self.players] 
                print(*msg, sep="\n")
                time.sleep(2)
                print("--------------")
            print(f"{self.players[self.winner]} wins pot of {self.pot}")
        
        time.sleep(3)

class Agent:
    def __init__(self, pos: int, name: str = None):
        self.pos = pos
        if name:
            self.name = name
        else:
            self.name = ["OP", "IP"][self.pos]    
        self.hand_history = dict[HandState : Action]
        
    def decide_action(self, state: HandState) -> Action:
        pass

class Human(Agent):
    def __init__(self, pos: int, name: str = None):
        super().__init__(pos, name)
        
    def decide_action(self, state: HandState) -> Action:
        print("---------------------")
        print(f"You have {state.players[self.pos].card}")
        options = state.get_valid_actions()
        while True:
            for i, action in enumerate(options, start=1):
                print(f"{i}. {action.name}")
            try:
                selection = int(input("Select an action: "))
                if 1 <= selection <= len(options):
                    print("---------------------")
                    return options[selection - 1]
                else:
                    print("Please select a valid action.")
            except ValueError:
                print("Please enter a number.")          

class Strategy:
    def __init__(self, action_probabilities: Dict[HandState, Dict[Action, float]]):
        self.action_probabilities = action_probabilities

    def get_action_probabilities(self, state: HandState) -> Dict[Action, float]:
        return self.action_probabilities.get(state, {})

    def __str__(self) -> str:
        result = []
        for state, actions in self.action_probabilities.items():
            action_strs = [f"{action}: {prob:.2f}" for action, prob in actions.items()]
            result.append(f"{state}: {{{', '.join(action_strs)}}}")
        return "\n".join(result)
    
    def __repr__(self) -> str:
        return str(self.action_probabilities)
    
    
class Computer(Agent):
    def __init__(self, pos: int, name: str = None, strategy: Strategy = None):
        self.strategy = strategy
        super().__init__(pos, name)
    
    def decide_action(self, state: HandState) -> Action:
        if self.strategy:
            action_probabilities = self.strategy.get_action_probabilities(state)
            actions, probabilities = zip(*action_probabilities.items())
            return random.choices(actions, probabilities)[0]
        else:
            options = state.get_valid_actions()
            return random.choice(options)

class Game:
    def __init__(self, deck_size: int, max_raises: int) -> None:
        self.deck = Deck(deck_size)
        self.max_raises = max_raises
        self.card_combos = [(c1,c2) for c1 in self.deck for c2 in self.deck if c1 != c2]
        self.game_tree = self.get_game_tree()
        self.all_states = self.get_all_states()
        
    def play_hand(self, OP: Agent, IP: Agent, stacks: Tuple[int, int]) -> HandState:
        players = [OP,IP]
        cards = (self.deck.deal(), self.deck.deal())
        state = HandState(cards, stacks, max_raises = self.max_raises)
        while not state.is_over:
            state.dealer_message()
            next_action = players[state.acting_pos].decide_action(state)
            state = state.get_next_state(next_action)
        state.dealer_message()
        return state
        
    def get_game_tree(self, state: HandState = None) -> dict:
        if isinstance(state, HandState):
            if state.is_over:
                return state
        
            state_dict = {}
            for option in state.get_valid_actions():
                state_dict[option] = self.get_game_tree(state.get_next_state(option))
            return {state : state_dict}
        
        else:
            result = {}
            for combo in self.card_combos:
                this_combo = HandState(combo, (0, 0), [], max_raises = self.max_raises)
                result.update(self.get_game_tree(this_combo))
            return result
        
    def get_all_states(self, state: HandState = None) -> list[HandState]:
        if isinstance(state, HandState):
            if state.is_over:
                return [state]
        
            all_states = []
            for option in state.get_valid_actions():
                next_state = state.get_next_state(option)
                all_states.append(next_state)
                all_states += self.get_all_states(next_state) 
            return all_states
            
        else:
            result = []
            for combo in self.card_combos:
                this_combo = HandState(combo, (0, 0), [], max_raises = self.max_raises)
                combo_states = self.get_all_states(this_combo)
                result.extend(combo_states)
                
            return result
