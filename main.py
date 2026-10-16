from board import get_board,create_empty_state,print_board,is_board_full,place_stone,get_score
from game import stones_allowed,the_winner_is
from alpha_beta_player import best_move_alpha_beta, evaluate_v2

"""Runs a game of Catchup: the program plays one color, 
the operator types the opponent's moves."""

board = get_board()
state = create_empty_state(board)
SEARCH_DEPTH = 2


current_player = "W" # white alwasy starts first
is_first_turn = True # white first's turn is only 1 stone 
opponent_previous_score = 1 # last player score before their turn
while True: # keep asking until W or B is entered
    program_color = input("Which color does the program play? (W/B): ").strip().upper()
    if program_color in ("W", "B"):
        break
    print("Invalid color. Enter W or B.")
history = []
while is_board_full(state) is False:
    history.append((state.copy(), current_player, is_first_turn, opponent_previous_score)) # save the game state before each turn
    white_score, black_score = get_score(state)
    if current_player == "W":
        my_score = white_score
        opponent_score = black_score
    elif current_player == "B":
        my_score= black_score
        opponent_score = white_score
    max_stones_allowed = stones_allowed(is_first_turn,my_score,opponent_score,opponent_previous_score)
    opponent_previous_score = my_score # saves this player’s score before they move for the next player’s bonus check
    stones_placed = 0
    undo_requested = False
    if current_player == program_color: # alpha-beta player turn
        moves = best_move_alpha_beta(state, current_player, max_stones_allowed, SEARCH_DEPTH, evaluate_v2)
        for cell in moves:
            place_stone(state, cell, current_player)
        print("Program plays: " + " ".join(moves))
    else: # human player turn
        while stones_placed < max_stones_allowed and not is_board_full(state):
            print_board(board,state)
            if current_player == "W":
                cell = input("Player White you have placed "+ str(stones_placed) +" stones."+ "Place one more out of "+str(max_stones_allowed)+ " allowed!")
            else:
                cell = input("Player Black you have placed "+ str(stones_placed) +" stones."+ "Place one more out of "+str(max_stones_allowed)+ " allowed!")
            if cell.strip().lower() == "undo": # go back to the start of this turn
                state, current_player, is_first_turn, opponent_previous_score = history.pop()
                undo_requested = True
                break
            if cell.strip().lower() == "done" and stones_placed >= 1: # ends the turn early
                break
            placed = place_stone(state,cell,current_player)
            if placed:
                stones_placed += 1

    if undo_requested:
        continue
    is_first_turn = False
    if current_player == "W":
        current_player = "B"
    else :
        current_player = "W"

# show the final board and the winner
print_board(board,state)
if the_winner_is(state)== "White":  
    print("The Winner is Player White!")
elif the_winner_is(state) == "Black":
    print("The Winner is Player Black!")
else:
    print("It's a draw!")
