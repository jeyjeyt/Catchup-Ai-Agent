### `stones_allowed(is_first_turn, my_score, opponent_score, opponent_previous_score)`
This function decides the **maximum** number of stones the current player may place on their turn. The player can then choose to place fewer (for example, "up to 2" means 1 or 2). It follows the three cases of the Catchup rules:

- **First turn:** White's very first move is always exactly 1 stone, so the function returns 1.
- **Bonus turn:** a player may place up to 3 stones only if their opponent's score *went up* on the opponent's last turn **and** the opponent's score is now equal to or higher than their own. To know whether the opponent's score went up, the function compares the opponent's current score with their score before their last turn (`opponent_score > opponent_previous_score`). Just being behind is not enough: the bonus is a reaction to the opponent having *just* caught up or pulled ahead.
- **Normal turn:** in every other case, the player may place up to 2 stones.

The function does not depend on the color of the player: it only receives "my" score and "my opponent's" scores, so the same function works for both White and Black. It also does not touch the board. It only takes the information it needs and returns 1, 2 or 3, which makes it easy to test on its own.

### `the_winner_is(state)`
This function decides who won once the board is full. It first checks that the game is really over (`is_board_full`), then gets the sizes of all groups for both players (`find_groups`) and their scores (`get_score`).

- If one player's biggest group is larger than the other's, that player wins.
- If the biggest groups are equal, the tie-breaker starts. My idea was to **remove the biggest group from both lists and compare the next biggest ones**, repeating this until one player's group is larger. This way the lists do not need to be sorted: each round, `max()` finds the current biggest group, and removing it "moves" the comparison one place down (second-biggest, third-biggest, and so on). This also follows the rule that equally-sized groups can each be "used" once: if a player has two groups of 5, removing one of them still leaves the other to be compared in the next round.
- The loop runs with `while True`, because every round either returns a result or makes both lists shorter, so it always ends.
- After each removal, the function checks whether a list has become empty before comparing again, since `max()` of an empty list would crash. If both lists are empty at the same time, every group was tied, and the game is a **draw**. If only one list is empty, that player has run out of groups while the other still has one left. A missing group counts as size 0, so the player with groups left wins.