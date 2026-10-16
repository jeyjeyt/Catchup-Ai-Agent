import time
from board import get_board, create_empty_state, is_board_full, get_score, print_board
from game import stones_allowed, the_winner_is
from alpha_beta_player import best_move_alpha_beta


def play_one_game(depth_white, depth_black, show_board=True):
    board = get_board()
    state = create_empty_state(board)
    current_player = "W"
    is_first_turn = True
    previous_score = 1
    depths = {"W": depth_white, "B": depth_black}
    time_used = {"W": 0.0, "B": 0.0}

    while not is_board_full(state):
        # how many stones may the current player place (same rules as main.py)
        white_score, black_score = get_score(state)
        if current_player == "W":
            my_score, other_score = white_score, black_score
        else:
            my_score, other_score = black_score, white_score
        max_stones = stones_allowed(is_first_turn, my_score, other_score, previous_score)
        previous_score = my_score

        # let the program choose, and measure how long it thinks
        start = time.time()
        move = best_move_alpha_beta(state, current_player, max_stones, depths[current_player])
        time_used[current_player] += time.time() - start

        for cell in move:
            state[cell] = current_player

        # show every move
        print(current_player, "plays", " ".join(move),
              "(max", max_stones, ") | time used so far:",
              round(time_used[current_player], 1), "s")
        if show_board:
            print_board(board, state)
            print()

        is_first_turn = False
        current_player = "B" if current_player == "W" else "W"

    print("Final board:")
    print_board(board, state)
    return the_winner_is(state), time_used


if __name__ == "__main__":
    winner, time_used = play_one_game(3, 3)
    print("Winner:", winner)
    print("Time used by White:", round(time_used["W"], 1), "seconds")
    print("Time used by Black:", round(time_used["B"], 1), "seconds")