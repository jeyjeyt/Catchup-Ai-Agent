import time
import alpha_beta_player
from board import get_board, create_empty_state, is_board_full, get_score
from game import stones_allowed, the_winner_is, generate_moves
from alpha_beta_player import best_move_alpha_beta, evaluate, evaluate_v2

# keep the real candidate-cells function, so we can switch it off and on
real_candidate_cells = alpha_beta_player.get_candidate_cells


def all_empty_cells(state):
    """Replacement used to switch the candidate-cells trick OFF."""
    return [cell for cell in state if state[cell] is None]


def play_game(white_player, black_player, use_candidates=True):
    """Plays one full game. Each player is (depth, eval_function).
    Returns the winner and the time each side used."""
    if use_candidates:
        alpha_beta_player.get_candidate_cells = real_candidate_cells
    else:
        alpha_beta_player.get_candidate_cells = all_empty_cells

    state = create_empty_state(get_board())
    current_player = "W"
    is_first_turn = True
    previous_score = 1
    players = {"W": white_player, "B": black_player}
    time_used = {"W": 0.0, "B": 0.0}

    while not is_board_full(state):
        white_score, black_score = get_score(state)
        if current_player == "W":
            my_score, other_score = white_score, black_score
        else:
            my_score, other_score = black_score, white_score
        max_stones = stones_allowed(is_first_turn, my_score, other_score, previous_score)
        previous_score = my_score

        depth, eval_function = players[current_player]
        start = time.time()
        move = best_move_alpha_beta(state, current_player, max_stones, depth, eval_function)
        time_used[current_player] += time.time() - start

        for cell in move:
            state[cell] = current_player
        is_first_turn = False
        current_player = "B" if current_player == "W" else "W"

    alpha_beta_player.get_candidate_cells = real_candidate_cells  # switch back on
    return the_winner_is(state), time_used


def show(title, winner, time_used):
    print(title)
    print("   winner:", winner,
          "| White:", round(time_used["W"], 1), "s",
          "| Black:", round(time_used["B"], 1), "s")


if __name__ == "__main__":
    # ---------- Experiment 1: all cells vs candidate cells ----------
    print("=== Experiment 1: all cells vs candidate cells ===")
    state = create_empty_state(get_board())
    state["E5"] = "W"
    state["F5"] = "W"
    state["C3"] = "B"
    print("   moves to consider (2 stones), all cells:      ",
          len(generate_moves(state, 2)))
    print("   moves to consider (2 stones), candidate cells:",
          len(generate_moves(state, 2, cells=real_candidate_cells(state))))
    winner, t = play_game((1, evaluate), (1, evaluate), use_candidates=False)
    show("   full game, depth 1, ALL cells:", winner, t)
    winner, t = play_game((1, evaluate), (1, evaluate), use_candidates=True)
    show("   full game, depth 1, CANDIDATE cells:", winner, t)

    # ---------- Experiment 2: search depth ----------
    print()
    print("=== Experiment 2: depth 1 vs depth 2 (candidate cells, v1) ===")
    winner, t = play_game((1, evaluate), (2, evaluate))
    show("   Game A: White = depth 1, Black = depth 2:", winner, t)
    winner, t = play_game((2, evaluate), (1, evaluate))
    show("   Game B: White = depth 2, Black = depth 1:", winner, t)

    # ---------- Experiment 3: evaluation function ----------
    print()
    print("=== Experiment 3: evaluation v1 vs v2 (depth 2) ===")
    winner, t = play_game((2, evaluate), (2, evaluate_v2))
    show("   Game A: White = v1, Black = v2:", winner, t)
    winner, t = play_game((2, evaluate_v2), (2, evaluate))
    show("   Game B: White = v2, Black = v1:", winner, t)