from board import get_score, find_groups
from game import generate_moves
from board import is_board_full
from game import stones_allowed
from board import get_neighbors


"""This is the alpha-beta pruning implementation"""

def evaluate(state, my_color):
    """evaluation score of the current state from my_color's point of view"""
    score_white, score_black = get_score(state)
    if my_color == "W":
        return score_white - score_black
    else: 
        return score_black - score_white

def evaluate_v2(state, my_color):
    """evaluate the largest and second-largest groups from my_color's point of view
    evaluation score = 10 * (my_largest - opponent_largest) +1* (my_second_largest - opponent_second_largest)"""
    groups_white, groups_black = find_groups(state)

    largest_white = 0
    second_largest_white = 0
    for group_size in groups_white:
        if group_size > largest_white:
            second_largest_white = largest_white
            largest_white = group_size
        elif group_size > second_largest_white:
            second_largest_white = group_size

    largest_black = 0
    second_largest_black = 0
    for group_size in groups_black:
        if group_size > largest_black:
            second_largest_black = largest_black
            largest_black = group_size
        elif group_size > second_largest_black:
            second_largest_black = group_size

    if my_color == "W":
        my_largest = largest_white
        my_second_largest = second_largest_white
        opponent_largest = largest_black
        opponent_second_largest = second_largest_black
    else: 
        my_largest = largest_black
        my_second_largest = second_largest_black
        opponent_largest = largest_white
        opponent_second_largest = second_largest_white

    return (
        10 * (my_largest - opponent_largest)
        + my_second_largest
        - opponent_second_largest
    )

def get_candidate_cells(state):
    """returns a list of empty cells that are adjacent 
    to at least one stone"""
    candidates = []
    for cell in state:
        if state[cell] is None:
            for neighbor in get_neighbors(cell,state):
                if state[neighbor] is not None:
                    candidates.append(cell)
                    break # one stone nearby is enough 
    if not candidates: # empty board, no stones placed yet so use all empty cells
        for cell in state:
            if state[cell] is None:
                candidates.append(cell)

    return candidates 


def alpha_beta(
    state, depth, alpha, beta, maximizing_player, my_color, previous_score,
    eval_function=evaluate #which evaluation function to use 
):
    """evaluates the current state using the alpha-beta pruning algorithm
    depth= number of levels to search in the game tree
    alpha= the best value that the maximizer currently can guarantee at that level or above
    beta= the best value that the minimizer currently can guarantee at that level or above
    maximizing_player= True if the current player is the maximizer, False if the current player is the minimizer
    previous_score= the score of the player who just moved, from before their move"""
    if depth == 0 or is_board_full(state): # because the game is over or we have reached the maximum depth
        return eval_function(state, my_color)

    if my_color == "W": 
        opponent_color = "B"
    else:
        opponent_color = "W"
    
    if maximizing_player:
        current_color = my_color
    else:
        current_color = opponent_color
    score_white, score_black = get_score(state)
    if current_color == "W":
        cur_score, other_score = score_white, score_black #the next level needs to know if the player's score went up
    else:
        cur_score, other_score = score_black, score_white

    max_stones = stones_allowed(False, cur_score, other_score, previous_score) # the search follows the same rules as the game

    if maximizing_player:
        max_eval = float('-inf')
        moves = generate_moves(state, max_stones,cells=get_candidate_cells(state))
        for move in moves:
            new_state = state.copy()
            for cell in move:
                new_state[cell] = my_color
            eval_score = alpha_beta(
                new_state, depth - 1, alpha, beta, False, my_color, cur_score,
                eval_function
            )
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha: # prune the remaining branches of the tree, the opponent already has a better option elsewhere, so they would never let the game reach this branch
                break
        return max_eval
    else:
        min_eval = float('inf')
        moves = generate_moves(state, max_stones, cells=get_candidate_cells(state))
        for move in moves:
            new_state = state.copy()
            for cell in move:
                new_state[cell] = opponent_color
            eval_score = alpha_beta(
                new_state, depth - 1, alpha, beta, True, my_color, cur_score,
                eval_function
            )
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def best_move_alpha_beta(
    state, my_color, max_stones, depth, eval_function=evaluate
):
    """the best move for the current player using the alpha-beta pruning algorithm
    and the eval_function picks v1 or v2"""
    if my_color == "W":
        my_score = get_score(state)[0]
    else:
        my_score = get_score(state)[1]
    best_eval = float('-inf')
    chosen_move = None
    alpha = float('-inf')
    beta = float('inf')

    for move in generate_moves(state, max_stones, cells=get_candidate_cells(state)):
        new_state = state.copy()
        for cell in move:
            new_state[cell] = my_color
        eval_score = alpha_beta(
            new_state, depth - 1, alpha, beta, False, my_color, my_score,
            eval_function
        ) # depth -1 because we have already made one move
        if eval_score > best_eval:
            best_eval = eval_score
            chosen_move = move  
        alpha = max(alpha, eval_score)

    return chosen_move

 