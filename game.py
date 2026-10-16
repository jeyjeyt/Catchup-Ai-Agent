from board import is_board_full, find_groups, get_score
from itertools import combinations
"""Turn rules and end of the game"""

def stones_allowed(is_first_turn,my_score,opponent_score,opponent_previous_score):
    """returns the maximum number of stones that the current player may place on this turn"""
    if is_first_turn == False:
        if my_score <= opponent_score and opponent_score > opponent_previous_score: # if the current player is behind or tied and the opponent's score went up on their last turn, they may place 3 stones
            return 3
        else: 
            return 2
    else :
        return 1 # if it is the first turn, the current player may place only 1 stone

def generate_moves(state, max_stones, cells=None):
    """generates all possible moves for the current player given the current state 
    and the maximum number of stones they can place"""
    if cells is None:
        empty_cells = []
        for cell in state:
            if state[cell] is None:
                empty_cells.append(cell)
    else:
        empty_cells = cells 
        
    if not empty_cells or max_stones < 1:
        return []

    moves = []
    for num_stones in range(1, min(max_stones, len(empty_cells)) + 1): # generate all combinations of empty cells for 1 to max_stones, but never more than the number of empty cells
        for combination in combinations(empty_cells, num_stones): # the order of the stones does not matter, so each set of cells is listed only once
            moves.append(combination)
    return moves

def the_winner_is(state):  
    """returns the winner of the game or Draw""" 
    if is_board_full(state) == True:
        group_white, group_black = find_groups(state)
        score_white, score_black = get_score(state)
        if score_white > score_black: # if one player has a higher score than the other, they are the winner
            return "White"
        elif score_white < score_black:
            return "Black"
        else:
            while True: # if both biggest groups are equal then we apply the tiebreaker rule
                group_white.remove(max(group_white))
                group_black.remove(max(group_black))
                if not group_white and group_black: # if one player has no groups and the other does, the player with groups is the winner
                    return "Black"
                if not group_black and group_white:
                    return "White"
                if not group_black and not group_white:
                    return "Draw"
                else:
                    if max(group_white) > max(group_black):
                        return "White"
                    if max(group_white) < max(group_black):
                        return "Black"
                
        


