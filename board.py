"""This module defines the board structure and 
provides functions to create and print the board state."""

def get_board():
    """creates the board structure as a list of lists, 
    where each inner list represents a row of the board"""
    board = []
    letters = "ABCDEFGHI"
    first_half_rows = [9,8,7,6]
    second_half_rows = [5,4,3,2,1]

    # top  half of the board: rows 9 to 6, each rows starts at E, D, C, B and all end at I
    i = 4
    for row in first_half_rows: 
        initial_row =[]
        for letter in letters[i:]: 
            initial_row.append(letter + str(row))    
        board.append(initial_row)
        i = i - 1 


    # bottom half of the board: rows 5 to 1, each row starts at A and ends at I, H, G, F, E respectively
    i = 9
    for row in second_half_rows: 
        initial_row =[]
        for letter in letters[:i]: 
            initial_row.append(letter + str(row))
            
        board.append(initial_row)
        i = i - 1 

    return board


def create_empty_state(board):
    """creates an empty state for the board"""
    state = {}
    for row in board:
        for cell in row:
            state[cell] = None
    return state


def print_board(board,state):
    """prints the board state"""
    max_row_length = max(len(row) for row in board)
    for row in board:
        row_number = row[0][1:] # get the row number from the first cell in the row
        row_str = ""
        for cell in row:
            if state[cell] is None:
                row_str += "[ ] "
            else:
                row_str += "[" + str(state[cell]) + "] "
        padding = " " * (2 * (max_row_length - len(row))) # add padding to align the rows
        print(row_number + " " + padding + row_str.rstrip())


"""This module place the stones on the board and 
provides functions to update the board state."""

def place_stone(state,cell,stone_color):
    """places a stone of the given color on the specified cell in the state"""
    cell = cell.strip().upper() # normalize the cell input to uppercase and remove whitespace 
    #cell is not in the state
    if cell not in state:
        print("Invalid cell")
        return False 

    #cell is already occupied
    if state[cell] is not None:
        print("Cell is already occupied")
        return False

    #place the color on the cell
    stone_color = stone_color.strip().upper()
    if stone_color != "W" and stone_color != "B":
        print("Invalid stone color")
        return False

    state[cell] = stone_color
    return True 


"""Finding groups"""

def get_neighbors(cell, state):
    """returns a list of neighboring cells for the given cell in the state"""
    letters = "ABCDEFGHI"
    row = int(cell[1:])
    col = letters.index(cell[0])

    neighbors = []
    neighbors.append(letters[col] + str(row - 1))  # Down
    neighbors.append(letters[col] + str(row + 1))  # Up
    if col > 0:
        neighbors.extend((letters[col - 1] + str(row), letters[col - 1] + str(row - 1))) # left and down-left
    if col < len(letters) - 1:
        neighbors.extend((letters[col + 1] + str(row), letters[col + 1] + str(row + 1))) # right and up-right 

    return [neighbor for neighbor in neighbors if neighbor in state] # filter out neighbors that are not in the state


def find_groups(state):
    """finds all groups of connected stones of the same color in the state"""
    visited = [] # list to keep track of visited cells 
    group_white = [] # list to keep track of the sizes of white groups
    group_black = [] #list to keep track of the sizes of black groups

    for cell in state:
        if cell not in visited and state[cell] is not None:
            group_size = 1
            visited.append(cell)
            to_check = [cell] # list to keep track of cells to check for neighbors
            while to_check:
                current = to_check.pop()
                neighbors = get_neighbors(current, state)
                for neighbor in neighbors:
                    if neighbor not in visited and state[neighbor] is not None:
                        if state[neighbor] == state[cell]:
                            group_size += 1
                            visited.append(neighbor)
                            to_check.append(neighbor)

            if state[cell] == "W":
                group_white.append(group_size)
            else:
                group_black.append(group_size)

    return group_white, group_black

def get_score(state):
    """returns the score for each player based on the size of their largest group"""
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