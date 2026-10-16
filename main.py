from board import get_board,create_empty_state,print_board,is_board_full,place_stone,get_score
from game import stones_allowed,the_winner_is
from alpha_beta_player import best_move_alpha_beta

board = get_board()
state = create_empty_state(board)
SEARCH_DEPTH = 1


current_player = "W"
is_first_turn = True
opponent_previous_score = 1
while True:
    program_color = input("Which color does the program play? (W/B): ").strip().upper()
    if program_color in ("W", "B"):
        break
    print("Invalid color. Enter W or B.")
history = []
while is_board_full(state) is False:
    history.append((state.copy(), current_player, is_first_turn, opponent_previous_score))
    white_score, black_score = get_score(state)
    if current_player == "W":
        my_score = white_score
        opponent_score = black_score
    elif current_player == "B":
        my_score= black_score
        opponent_score = white_score
    max_stones_allowed = stones_allowed(is_first_turn,my_score,opponent_score,opponent_previous_score)
    opponent_previous_score = my_score
    stones_placed = 0
    undo_requested = False
    if current_player == program_color:
        moves = best_move_alpha_beta(state, current_player, max_stones_allowed, SEARCH_DEPTH)
        for cell in moves:
            place_stone(state, cell, current_player)
        print("Program plays: " + " ".join(moves))
    else:
        while stones_placed < max_stones_allowed and not is_board_full(state):
            print_board(board,state)
            if current_player == "W":
                cell = input("Player White you have placed "+ str(stones_placed) +" stones."+ "Place one more out of "+str(max_stones_allowed)+ " allowed!")
            else:
                cell = input("Player Black you have placed "+ str(stones_placed) +" stones."+ "Place one more out of "+str(max_stones_allowed)+ " allowed!")
            if cell.strip().lower() == "undo":
                state, current_player, is_first_turn, opponent_previous_score = history.pop()
                undo_requested = True
                break
            if cell.strip().lower() == "done" and stones_placed >= 1:
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

print_board(board,state)
if the_winner_is(state)== "White":  
    print("The Winner is Player White!")
elif the_winner_is(state) == "Black":
    print("The Winner is Player Black!")
else:
    print("It's a draw!")
