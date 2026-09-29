
def get_board():
    board = []
    letters = "ABCDEFGHI"
    first_half_rows = [9,8,7,6]
    second_half_rows = [5,4,3,2,1]

    """first half of the board"""  
    i = 4
    for row in first_half_rows: 
        initial_row =[]
        for letter in letters[i:]: 
            initial_row.append(letter + str(row))    
        board.append(initial_row)
        i = i - 1 


    """second half of the board"""
    i = 9
    for row in second_half_rows: 
        initial_row =[]
        for letter in letters[:i]: 
            initial_row.append(letter + str(row))
            
        board.append(initial_row)
        i = i - 1 

    return board

board = get_board()
#print(board)
#print("Number of rows:", len(board))
#number_of_cells = 0
#for row in board:
#    number_of_cells += len(row)
#    
#print("Total number of cells:", number_of_cells)

def create_empty_state(board):
    state = {}
    for row in board:
        for cell in row:
            state[cell] = None
    return state

state = create_empty_state(board)
    
def print_board(board,state):
    max_row_length = max(len(row) for row in board)
    for row in board:
        row_number = row[0][1:]
        row_str = ""
        for cell in row:
            if state[cell] is None:
                row_str += "[ ] "
            else:
                row_str += "[" + str(state[cell]) + "] "
        padding = " " * (2 * (max_row_length - len(row)))
        print(row_number + " " + padding + row_str.rstrip())

print_board(board, state)