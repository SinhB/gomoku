from operator import add
import numpy as np
from numba import njit, int64

@njit("Tuple((int64, int64, boolean, boolean, boolean, boolean, boolean, boolean))(int64[:], int64, boolean)", fastmath=True)
def check_side(side, player, eating=False):
    consec = 0
    consec_op = 0
    additional = 0
    is_after_blank = False
    is_consec = True
    is_additional = True
    check_eating = True
    starting_blank = False
    starting_op = False
    closing_blank = False
    closing_op = False
    could_get_eat = False
    
    for i in range(0, min(len(side), 6)):
        if side[i] == player:
            if check_eating and consec_op == 2:
                eating = True
                new_side = np.copy(side)
                new_side[i-1] = 0
                new_side[i-2] = 0
                return check_side(new_side, player, eating=True)
            check_eating = False
            if not consec_op:
                if is_consec:
                    consec += 1
                else:
                    additional += 1
        if side[i] == 0:
            check_eating = False
            if i == 0:
                starting_blank = True
            if i == 1 and consec == 1:
                could_get_eat = True
            if is_after_blank or consec_op:
                if consec_op and not eating:
                    closing_op = True
                else:
                    closing_blank = True
                break
            is_after_blank = True
            is_consec = False
        if side[i] == -player:
            if i == 0:
                starting_op = True
            if is_after_blank:
                if not additional:
                    closing_blank = True
                else:
                    closing_op = True
                break
            consec_op += 1
            is_consec = False

    if i == len(side) - 1 and is_after_blank and side[i] != player:
        closing_blank = True
    elif i == len(side) - 1:
        closing_op = True
    return consec, additional, eating, starting_blank, starting_op, closing_blank, closing_op, could_get_eat


@njit("Tuple((int64, int64, int64, boolean, boolean))(int64[:], int64, int64, int64, int64, int64, int64, int64, int64, int64)", fastmath=True)
def check_line(
    line,
    starting_index,
    player,
    multiplicator_five,
    multiplicator_open_four,
    multiplicator_open_three,
    multiplicator_semi_closed_four,
    multiplicator_semi_closed_three,
    multiplicator_open_two,
    multiplicator_semi_close_two
):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    
    l_consec, l_additional, l_eating, l_starting_blank, l_starting_op, l_closing_blank, l_closing_op, l_could_get_eat = check_side(left, player, False)
    r_consec, r_additional, r_eating, r_starting_blank, r_starting_op, r_closing_blank, r_closing_op, r_could_get_eat = check_side(right, player, False)
    
    
    close_threat = False
    semi_close = False
    open_threat = False
    
    
    if l_closing_op and r_closing_op:
        close_threat = True
    elif (l_closing_op and not r_closing_op) or (not l_closing_op and r_closing_op):
        semi_close = True
    else:
        open_threat = True
    
    total_consec = l_consec + r_consec
    
     # Player serie
    closed_two = 0
    semi_closed_two = 0
    open_two = 0

    closed_three = 0
    semi_closed_three = 0
    open_three = 0

    closed_four = 0
    semi_closed_four = 0
    open_four = 0

    five = 0
    
    if total_consec == 1:
        if close_threat:
            closed_two += 1
        if semi_close:
            semi_closed_two += 1
        if open_threat:
            open_two += 1
    if total_consec == 2:
        if close_threat:
            closed_three += 1
        if semi_close:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
    if total_consec == 3:
        if close_threat:
            closed_four += 1
        if semi_close:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
    if total_consec >= 4:
        five += 1
    
    has_empty = False
    if r_additional:
        if (l_consec + r_additional == 2) or (r_consec + r_additional == 2):
            if semi_close:
                semi_closed_three += 1
            if open_threat:
                open_three += 1
            has_empty = True
    if l_additional:
        if (r_consec + l_additional == 2) or (l_consec + l_additional == 2):
            if semi_close:
                semi_closed_three += 1
            if open_threat:
                open_three += 1
            has_empty = True
    if r_additional:
        if (l_consec + r_additional == 3) or (r_consec + r_additional == 3):
            if semi_close:
                semi_closed_four += 1
            if open_threat:
                open_four += 1
            has_empty = True
    if l_additional:
        if (r_consec + l_additional == 3) or (l_consec + l_additional == 3):
            if semi_close:
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
        score = multiplicator_semi_close_two - minus_empty
    return score, five, open_three, l_eating, r_eating
