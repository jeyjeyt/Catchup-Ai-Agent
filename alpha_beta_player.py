from board import get_score
from game import generate_moves
from board import is_board_full
from game import stones_allowed
from board import get_neighbors


def evaluate(state, my_color):
    score_white, score_black = get_score(state)
    if my_color == "W":
        return score_white - score_black
    else: 
        return score_black - score_white

def get_candidate_cells(state):
    candidates = []
    for cell in state:
        if state[cell] is None:
            for neighbor in get_neighbors(cell,state):
                if state[neighbor] is not None:
                    candidates.append(cell)
                    break # one stone nearby is enough 
    if not candidates:
        for cell in state:
            if state[cell] is None:
                candidates.append(cell)

    return candidates 

def best_move(state, my_color, max_stones):
    moves = generate_moves(state, max_stones, cells=get_candidate_cells(state))
    best_evaluation = float('-inf')
    chosen_move = None

    for move in moves:
        candidate_state = state.copy()
        for cell in move:
            candidate_state[cell] = my_color

        candidate_evaluation = evaluate(candidate_state, my_color)
        is_better_move = candidate_evaluation > best_evaluation
        if is_better_move:
            best_evaluation = candidate_evaluation
            chosen_move = move

    return chosen_move


def alpha_beta(state, depth, alpha, beta, maximizing_player, my_color, previous_score):
    if depth == 0 or is_board_full(state):
        return evaluate(state, my_color)

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
        cur_score, other_score = score_white, score_black
    else:
        cur_score, other_score = score_black, score_white

    max_stones = stones_allowed(False, cur_score, other_score, previous_score)

    if maximizing_player:
        max_eval = float('-inf')
        moves = generate_moves(state, max_stones,cells=get_candidate_cells(state))
        for move in moves:
            new_state = state.copy()
            for cell in move:
                new_state[cell] = my_color
            eval_score = alpha_beta(
                new_state, depth - 1, alpha, beta, False, my_color, cur_score
            )
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
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
                new_state, depth - 1, alpha, beta, True, my_color, cur_score
            )
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def best_move_alpha_beta(state, my_color, max_stones, depth):
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
            new_state, depth - 1, alpha, beta, False, my_color,my_score)
        if eval_score > best_eval:
            best_eval = eval_score
            chosen_move = move  
        alpha = max(alpha, eval_score)

    return chosen_move

 