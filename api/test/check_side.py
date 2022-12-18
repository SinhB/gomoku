import numpy as np
from numba import njit

# @njit("Tuple((int64, int64, boolean, boolean))(int64[:], int64, boolean)", fastmath=True)
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