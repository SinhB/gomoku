from operator import add
import numpy as np
from numba import njit, int64

def check_side(side, player, eating=False):
    consec = 0
    additional = 0
    is_after_blank = False
    is_consec = True
    block = False

    #If is on the board side
    if len(side) == 0:
        return 0, 0, False, True
    
    #Only if eating
    if len(side) >= 3:
        if side[0] == -player and side[1] == -player and side[2] == player:
            new_side = np.copy(side)
            new_side[0] = 0
            new_side[1] = 0
            return check_side(new_side, player, eating=True)

    for i in range(0, min(len(side), 6)):
        if side[i] == player:
            if is_consec:
                consec += 1
            else:
                additional += 1
        elif side[i] == 0:
            if is_after_blank:
                return consec, additional, eating, block
            is_after_blank = True
            is_consec = False
        elif side[i] == -player:
            if is_after_blank:
                if not additional:
                    return consec, additional, eating, False
            return consec, additional, eating, True
    if i == 0 and side[i] == 0:
        return consec, additional, eating, block
    if i == len(side) - 1:
        if not(is_after_blank and not additional):
            block = True
    return consec, additional, eating, block


def check_line(line, starting_index, player, multiplicator_five, multiplicator_open_four, multiplicator_open_three, multiplicator_semi_closed_four, multiplicator_semi_closed_three, multiplicator_open_two, multiplicator_semi_closed_two):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    
    l_consec, l_additional, l_eating, l_block = check_side(left, player, False)
    r_consec, r_additional, r_eating, r_block = check_side(right, player, False)
    
    
    close_threat = False
    semi_closed = False
    open_threat = False
    
    if l_block and r_block:
        close_threat = True
    elif (l_block and not r_block) or (not l_block and r_block):
        semi_closed = True
    else:
        open_threat = True

    total_stone = l_consec + l_additional + r_consec + r_additional
    has_empty = True if (l_additional or r_additional) else False
        
    # Player serie
    five = 0
    open_four = 0
    semi_closed_four = 0
    closed_four = 0
    open_three = 0
    semi_closed_three = 0
    closed_three = 0
    open_two = 0
    semi_closed_two = 0
    closed_two = 0
    
    if total_stone >= 4:
        five += 1
    elif total_stone == 3:
        if close_threat:
            closed_four += 1
        if semi_closed:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
    elif total_stone == 2:
        if close_threat:
            closed_three += 1
        if semi_closed:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
    elif total_stone == 1:
        if close_threat:
            closed_two += 1
        if semi_closed:
            semi_closed_two += 1
        if open_threat:
            open_two += 1

    has_empty = False
    if r_additional:
        if (l_consec + r_additional == 2) or (r_consec + r_additional == 2):
            if semi_closed:
                semi_closed_three += 1
            if open_threat:
                open_three += 1
            has_empty = True
    if l_additional:
        if (r_consec + l_additional == 2) or (l_consec + l_additional == 2):
            if semi_closed:
                semi_closed_three += 1
            if open_threat:
                open_three += 1
            has_empty = True
    if r_additional:
        if (l_consec + r_additional == 3) or (r_consec + r_additional == 3):
            if semi_closed:
                semi_closed_four += 1
            if open_threat:
                open_four += 1
            has_empty = True
    if l_additional:
        if (r_consec + l_additional == 3) or (l_consec + l_additional == 3):
            if semi_closed:
                semi_closed_four += 1
            if open_threat:
                open_four += 1
            has_empty = True
    score = 0
    minus_empty = 0
    if has_empty:
        minus_empty = 100

    if five:
        score = multiplicator_five - minus_empty
    elif open_four:
        score = multiplicator_open_four - minus_empty
    elif semi_closed_four:
        score = multiplicator_semi_closed_four - minus_empty
    elif open_three:
        score = multiplicator_open_three - minus_empty
    elif semi_closed_three:
        score = multiplicator_semi_closed_three - minus_empty
    elif open_two:
        score = multiplicator_open_two
    elif semi_closed_two:
        score = multiplicator_semi_closed_two - minus_empty
    return score, five, open_three, l_eating, r_eating


    # return has_empty, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five
