# Example strategy for ComputerPlayer

strategy = {
    ("10", "Open"): [0.5,0.5], # % Check, % Bet
    ("10", "OP_Check"): [0.5,0.5], # % Check, % Bet
    ("10", "OP_Bet"): [0,1], # % Call, % Fold
    ("10", "IP_Bet"): [0,1], # % Call, % Fold
    ("J", "Open"): [0.5,0.5], 
    ("J", "OP_Check"): [0.5,0.5], 
    ("J", "OP_Bet"): [0.5,0.5],
    ("J", "IP_Bet"): [0.5,0.5],
    ("Q", "Open"): [0.5,0.5],
    ("Q", "OP_Check"): [0.5,0.5], 
    ("Q", "OP_Bet"): [0.5,0.5],
    ("Q", "IP_Bet"): [0.5,0.5],
    ("K", "Open"): [0.5,0.5],
    ("K", "OP_Check"): [0.5,0.5], 
    ("K", "OP_Bet"): [0.5,0.5],
    ("K", "IP_Bet"): [0.5,0.5],
    ("A", "Open"): [0.5,0.5],
    ("A", "OP_Check"): [0,1], 
    ("A", "OP_Bet"): [1,0],
    ("A", "IP_Bet"): [1,0]
}
