"""This module defines the board structure and 
provides functions to create and print the board state."""

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



"""This module place the stones on the board and 
provides functions to update the board state."""

def place_stone(state,cell,stone_color):
    cell = cell.strip().upper()
    #cell is not in the state
    if cell not in state:
        print("Invalid cell")
        return False 

    #cell is already occupied
    if cell in state and state[cell] is not None:
        print("Cell is already occupied")
        return False

    #place the color on the cell
    stone_color = stone_color.strip().upper()
    if stone_color != "W" and stone_color != "B":
        print("Invalid stone color")
        return False

    state[cell] = stone_color
    return True 

#if __name__ == "__main__":
#    board = get_board()
#    state = create_empty_state(board)
#
#    place_stone(state, "E5", "W")    # good move → should work
#    place_stone(state, "E5", "B")    # same cell → "Cell is already occupied"
#    place_stone(state, "Z9", "W")    # doesn't exist → "Invalid cell"
#
#    print_board(board, state)

"""Finding groups"""

def get_neighbors(cell, state):
    letters = "ABCDEFGHI"
    row = int(cell[1:])
    col = letters.index(cell[0])

    neighbors = []
    neighbors.append(letters[col] + str(row - 1))  # Down
    neighbors.append(letters[col] + str(row + 1))  # Up
    if col > 0:
        neighbors.extend((letters[col - 1] + str(row), letters[col - 1] + str(row - 1)))
    if col < len(letters) - 1:
        neighbors.extend((letters[col + 1] + str(row), letters[col + 1] + str(row + 1)))

    return [neighbor for neighbor in neighbors if neighbor in state]


def find_groups(state):
    visited = []
    group_white = []
    group_black = []

    for cell in state:
        if cell not in visited and state[cell] is not None:
            score = 1
            visited.append(cell)
            to_check = [cell]
            while to_check:
                current = to_check.pop()
                neighbors = get_neighbors(current, state)
                for neighbor in neighbors:
                    if neighbor not in visited and state[neighbor] is not None:
                        if state[neighbor] == state[cell]:
                            score += 1
                            visited.append(neighbor)
                            to_check.append(neighbor)

            if state[cell] == "W":
                group_white.append(score)
            else:
                group_black.append(score)
    

    return group_white,group_black

def get_score(state):
    group_white, group_black = find_groups(state)
    if not group_white:
        score_white = 1
    else:
        score_white = max(group_white)
    if not group_black:
        score_black= 1
    else:
        score_black = max(group_black)

    return score_white, score_black


"""Game Over """

def is_board_full(state):
    for cell in state:
        if state[cell] is None: 
            return False 
    return True 