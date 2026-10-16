from board import get_score
from itertools import combinations
from board import is_board_full
from game import stones_allowed


def evaluate(state, my_color):
    score_white, score_black = get_score(state)
    if my_color == "W":
        return score_white - score_black
    else: 
        return score_black - score_white

def generate_moves(state, max_stones):
    empty_cells = []
    for cell in state:
        if state[cell] is None:
            empty_cells.append(cell)
    if not empty_cells or max_stones < 1:
        return []

    moves = []
    for num_stones in range(1, min(max_stones, len(empty_cells)) + 1):
        for combination in combinations(empty_cells, num_stones):
            moves.append(combination)
    return moves

def best_move(state, my_color, max_stones):
    moves = generate_moves(state, max_stones)
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
        moves = generate_moves(state, max_stones)
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
        moves = generate_moves(state, max_stones)
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

    for move in generate_moves(state, max_stones):
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

if __name__ == "__main__":
    import time
    from board import get_board, create_empty_state, print_board

    board = get_board()
    state = create_empty_state(board)

    # small test position
    state["E5"] = "W"
    state["F5"] = "W"
    state["C3"] = "B"
    print_board(board, state)

    # --- depth 1 (should match best_move) ---
    print("best_move   Black:", best_move(state, "B", 2))
    print("best_move   White:", best_move(state, "W", 2))
    print("alpha-beta  Black:", best_move_alpha_beta(state, "B", 2, 1))
    print("alpha-beta  White:", best_move_alpha_beta(state, "W", 2, 1))

    # --- depth 2 (timed) ---
    start = time.time()
    print("alpha-beta depth 2 Black:", best_move_alpha_beta(state, "B", 2, 2))
    print("Time:", round(time.time() - start, 1), "seconds")