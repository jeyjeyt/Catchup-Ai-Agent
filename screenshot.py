from board import get_board, create_empty_state, print_board, get_neighbors, find_groups

board = get_board()

# --- Image 1: neighbors of E5 ---
state = create_empty_state(board)
state["E5"] = None                         # the cell we look at
for cell in get_neighbors("E5", state):
    state[cell] = "N"                      # its neighbors
print("Neighbors of E5:", get_neighbors("E5", state))
print_board(board, state)

print()

# --- Image 2: groups ---
state = create_empty_state(board)
for cell in ["E5", "F5", "F6", "A1"]:
    state[cell] = "W"
state["C3"] = "B"
print_board(board, state)
print("find_groups ->", find_groups(state))