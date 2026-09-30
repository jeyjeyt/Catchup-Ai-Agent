from board import is_board_full, find_groups, get_score

def stones_allowed(is_first_turn,my_score,opponent_score,opponent_previous_score):
    if is_first_turn == False:
        if my_score <= opponent_score and opponent_score > opponent_previous_score:
            return 3
        else: 
            return 2
    else :
        return 1

def the_winner_is(state):   
    if is_board_full(state) == True:
        group_white, group_black = find_groups(state)
        score_white, score_black = get_score(state)
        if score_white > score_black:
            return "White"
        elif score_white < score_black:
            return "Black"
        else:
            while True: 
                group_white.remove(max(group_white))
                group_black.remove(max(group_black))
                if not group_white and group_black:
                    return "Black"
                if not group_black and group_white:
                    return "White"
                if not group_black and not group_white:
                    return "Draw"
                else:
                    if max(group_white) > max(group_black):
                        return "White"
                    if max(group_white) < max(group_black):
                        return "Black"
                
        


