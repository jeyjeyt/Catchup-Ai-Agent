# Board Creation

## `get_board()`

The `get_board()` function creates the game board.

The board is divided into two parts:

- The first half contains the rows from 9 to 6.
- The second half contains the rows from 5 to 1.

The function uses the string `"ABCDEFGHI"` to create the cells of the board.

## 1. Creating the board

First, an empty list called `board` is created. This list will contain all the rows of the board.

The letters used to create the cells are stored in the string `"ABCDEFGHI"`.

The row numbers are divided into two groups: `[9, 8, 7, 6]` for the first half and `[5, 4, 3, 2, 1]` for the second half.

This is because the shape of the board changes after row 6.

## 2. Creating the first half

For every row, an empty list called `initial_row` is created. This list will contain all the cells of that particular row.

The variable `i` determines where to start in the string `"ABCDEFGHI"`. It starts at `4`, which corresponds to the letter `E`.

For each new row, `i` decreases by one. Therefore, each row starts one letter earlier:

- `i = 4` → E F G H I
- `i = 3` → D E F G H I
- `i = 2` → C D E F G H I
- `i = 1` → B C D E F G H I

The row number is combined with each letter to create the individual cells.

For example, the first half produces:

- E9 F9 G9 H9 I9
- D8 E8 F8 G8 H8 I8
- C7 D7 E7 F7 G7 H7 I7
- B6 C6 D6 E6 F6 G6 H6 I6

After each row is completed, it is added to the `board` list. Then `i` is decreased by one so that the next row starts one letter earlier.

## 3. Creating the second half

For the second half, `i` starts at `9`, meaning that all the letters in `"ABCDEFGHI"` are initially used.

For each new row, `i` decreases by one. This makes the slice of the string progressively shorter:

- `i = 9` → A B C D E F G H I
- `i = 8` → A B C D E F G H
- `i = 7` → A B C D E F G
- `i = 6` → A B C D E F
- `i = 5` → A B C D E

The row number is then combined with each letter to create the cells.

This produces:

- A5 B5 C5 D5 E5 F5 G5 H5 I5
- A4 B4 C4 D4 E4 F4 G4 H4
- A3 B3 C3 D3 E3 F3 G3
- A2 B2 C2 D2 E2 F2
- A1 B1 C1 D1 E1

The code does not actually remove letters from the original string. Instead, `letters[:i]` creates a slice containing only the first `i` letters.

## 4. Returning the board

Once all nine rows have been created, the function returns the complete `board`.

The function is then called and the resulting board is stored in the variable `board`.

The final board is a list containing nine rows, with each cell represented by a letter and a number, such as `E9`, `A5`, or `E1`.




## `create_empty_state(board)`

The `create_empty_state()` function creates an empty state for the board.

It takes the previously created `board` as an input and creates a dictionary called `state`.

### 1. Creating the state

First, an empty dictionary is created:

- `state = {}`

This dictionary will store every cell of the board as a key.

### 2. Going through the board

The function uses two `for` loops to go through every row and every cell in the board.

For each cell, the cell is added to the dictionary as a key.

The value of every cell is initially set to `None`.

For example, if the board contains:

- `E9`
- `F9`
- `G9`

the state will contain:

- `E9: None`
- `F9: None`
- `G9: None`

`None` means that the cell is currently empty and does not contain a game piece.

### 3. Returning the state

After all the rows and cells have been processed, the function returns the completed `state` dictionary.

The result is a dictionary containing every cell of the board, with `None` as its initial value.

This creates an empty representation of the board that can later be updated when pieces are placed on the cells.