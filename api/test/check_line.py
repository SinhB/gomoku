import numpy as np
from numba import njit
from check_side import check_side

# @njit("Tuple((boolean, boolean, boolean, int64, int64, int64, int64, int64, int64, int64, int64, int64, int64))(int64[:], int64, int64)", fastmath=True)
def check_line(line, starting_index, player):
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
        if (l_consec or r_consec) or (not r_consec and not r_additional and l_additional) or (not l_consec and not l_additional and r_additional):
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

    return has_empty, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five
