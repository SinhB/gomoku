"""Utils"""

import time
from enum import Enum
from functools import wraps

BLACK_VALUE = 1
WHITE_VALUE = -1


class Color(Enum):
    BLACK = BLACK_VALUE
    WHITE = WHITE_VALUE

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name

    def swap(self):
        if self.value == BLACK_VALUE:
            return Color.WHITE
        return Color.BLACK


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        # print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
