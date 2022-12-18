import itertools
import check_lines
import numpy as np
import time
import json

default_multiplicators = [
    11069,
    1536,
    1372,
    511,
    432,
    -58,
    -1,
    10137
]

def get_hash(multiplicators, test=False):
    # print(multiplicators)
    sides = [np.array(x) for x in itertools.product([-1, 0, 1], repeat=6)]

    lines = []
    start = time.time()
    total = 0
    hash_table = {}
    for i in range(0, len(sides)):
        for j in range(0, len(sides)):
            line = np.append(sides[i], 0)
            line = np.append(line, sides[j])
            lines.append((line, len(sides[i])))
            a = check_lines.check_line(line, len(sides[i]), 1, multiplicators[0], multiplicators[1], multiplicators[2], multiplicators[3], multiplicators[4], multiplicators[5], multiplicators[6])
            b = check_lines.check_line(line, len(sides[i]), -1, multiplicators[0], multiplicators[1], multiplicators[2], multiplicators[3], multiplicators[4], multiplicators[5], multiplicators[6])
            hash_table[hash((line.tobytes(), len(sides[i]), 1))] = a
            hash_table[hash((line.tobytes(), len(sides[i]), -1))] = b

            total += 1

    # print("TIME", time.time() - start)
    # print("TOTAL", total)
    # print(f"Different hash : {len(hash_table.keys())}")

    # print(len(sides))
    if test:
        return lines, hash_table
    else:
        return hash_table


def check_hash_speed(lines, hash_table):
    print("CHECK HASH")
    print(len(lines))
    start1 = time.time()
    for line, starting_index in lines:
        a = check_lines.check_line(line, starting_index, 1, multiplicators[0], multiplicators[1], multiplicators[2], multiplicators[3], multiplicators[4], multiplicators[5], multiplicators[6])
        b = check_lines.check_line(line, starting_index, -1, multiplicators[0], multiplicators[1], multiplicators[2], multiplicators[3], multiplicators[4], multiplicators[5], multiplicators[6])
    stop1 = time.time()
    print(f"No hash time : {stop1 - start1}")

    start2 = time.time()
    for line, starting_index in lines:
        a = hash_table[hash((line.tobytes(), starting_index, 1))]
        b = hash_table[hash((line.tobytes(), starting_index, -1))]
    stop2 = time.time()
    print(f"Hash time : {stop2 - start2}")
    return stop1 - start1, stop2 - start2

def test_consistency(lines, hash_table):
    for line, starting_index in lines:
        a = check_lines.check_line(line, starting_index, 1, multiplicators[0], multiplicators[1], multiplicators[2], multiplicators[3], multiplicators[4], multiplicators[5], multiplicators[6])
        b = check_lines.check_line(line, starting_index, -1, multiplicators[0], multiplicators[1], multiplicators[2], multiplicators[3], multiplicators[4], multiplicators[5], multiplicators[6])
        a2 = hash_table[hash((line.tobytes(), starting_index, 1))]
        b2 = hash_table[hash((line.tobytes(), starting_index, -1))]
        assert a[0] == a2[0] and a[1] == a2[1] and a[2] == a2[2]
        assert b[0] == b2[0] and b[1] == b2[1] and b[2] == b2[2]
    print("Is equal")

if __name__ == "__main__":
    lines, hash_table = get_hash(default_multiplicators, True)
    print(len(hash_table.keys()))
    time_no_hash = 0
    time_hash = 0
    for i in range(0, 1):
        a, b = check_hash_speed(lines, hash_table)
        time_no_hash += a
        time_hash += b
    print(time_no_hash, time_no_hash / 20)
    print(time_hash, time_hash / 20)
    test_consistency(lines, hash_table)

    with open('hash_table.json', 'w') as outfile:
        json.dump(json.dumps(hash_table), outfile)