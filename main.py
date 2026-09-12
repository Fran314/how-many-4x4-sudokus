# If the following square looks like random characters, do NOT use `printSudokuUnicode`, use `printSudokuAscii` instead
#
#          Unicode square
#         ╔═══╤═══╦═══╤═══╗
#         ║   │   ║   │   ║
#         ╟───┼───╫───┼───╢
#         ║   │   ║   │   ║
#         ╠═══╪═══╬═══╪═══╣
#         ║   │   ║   │   ║
#         ╟───┼───╫───┼───╢
#         ║   │   ║   │   ║
#         ╚═══╧═══╩═══╧═══╝
#
# The following square, instead, should look readable but a bit rough
#
#            Ascii square
#         +---+---+---+---+
#         |   :   |   :   |
#         + - + - + - + - +
#         |   :   |   :   |
#         +---+---+---+---+
#         |   :   |   :   |
#         + - + - + - + - +
#         |   :   |   :   |
#         +---+---+---+---+
#

import math
import time

N = 4
SQRT_N = int(math.sqrt(N))


# Helpers
def _index2pos(i: int) -> tuple[int, int]:
    return (i % N, i // N)


def _pos2index(x: int, y: int) -> int:
    return x + y * N


def _sameRowCells(i: int) -> list[int]:
    (_, y) = _index2pos(i)
    return [_pos2index(cx, y) for cx in range(N)]


def _sameColCells(i: int) -> list[int]:
    (x, _) = _index2pos(i)
    return [_pos2index(x, cy) for cy in range(N)]


def _sameBoxCells(i: int) -> list[int]:
    (x, y) = _index2pos(i)

    # x & y coords of the BOX where cell of index i is
    bx = x // SQRT_N
    by = y // SQRT_N

    return [
        _pos2index(bx * SQRT_N + cx, by * SQRT_N + cy)
        for cx in range(SQRT_N)
        for cy in range(SQRT_N)
    ]


# Precompute all possible values for efficiency
sameRowCells = {i: _sameRowCells(i) for i in range(N**2)}
sameColCells = {i: _sameColCells(i) for i in range(N**2)}
sameBoxCells = {i: _sameBoxCells(i) for i in range(N**2)}


def printSudokuUnicode(sudoku: list[int]):
    # ╔═══╤═══╦═══╤═══╗
    # ║   │   ║   │   ║
    # ╟───┼───╫───┼───╢
    # ║   │   ║   │   ║
    # ╠═══╪═══╬═══╪═══╣
    # ║   │   ║   │   ║
    # ╟───┼───╫───┼───╢
    # ║   │   ║   │   ║
    # ╚═══╧═══╩═══╧═══╝
    topLine = "╔"
    midThin = "╟"
    midBold = "╠"
    btmLine = "╚"
    for i in range(SQRT_N):
        for j in range(SQRT_N):
            if j != SQRT_N - 1:
                topLine += "═══╤"
                midThin += "───┼"
                midBold += "═══╪"
                btmLine += "═══╧"
            elif i != SQRT_N - 1:
                topLine += "═══╦"
                midThin += "───╫"
                midBold += "═══╬"
                btmLine += "═══╩"
            else:
                topLine += "═══╗"
                midThin += "───╢"
                midBold += "═══╣"
                btmLine += "═══╝"

    print(topLine)
    for y in range(N):
        print("║", end="")
        for x in range(N):
            i = _pos2index(x, y)
            val = sudoku[i] or " "
            end = "║" if x % SQRT_N == SQRT_N - 1 else "│"
            print(f" {val} ", end=end)
        print()

        if y % SQRT_N != SQRT_N - 1:
            print(midThin)
        elif y != N - 1:
            print(midBold)
        else:
            print(btmLine)


def printSudokuAscii(sudoku: list[int]):
    # +---+---+---+---+
    # |   :   |   :   |
    # + - + - + - + - +
    # |   :   |   :   |
    # +---+---+---+---+
    # |   :   |   :   |
    # + - + - + - + - +
    # |   :   |   :   |
    # +---+---+---+---+
    boldLine = "+" + ("---+" * N)
    thinLine = "+" + (" - +" * N)

    print(boldLine)
    for y in range(N):
        print("|", end="")
        for x in range(N):
            i = _pos2index(x, y)
            val = sudoku[i] or " "
            vert = "|" if x % SQRT_N == SQRT_N - 1 else ":"
            print(f" {val} {vert}", end="")
        print()

        if y % SQRT_N != SQRT_N - 1:
            print(thinLine)
        else:
            print(boldLine)


def findSolutions(sudoku: list[int], curr: int) -> list[list[int]]:
    if curr == N**2:  # No cells remaining to be filled, solution found
        return [sudoku]

    # All the cells to check: cells in same row, cells in same column, cells in same square.
    _cells2Check = sameRowCells[curr] + sameColCells[curr] + sameBoxCells[curr]
    # Only check cells with indices lower than i, as the other are not yet set.
    cells2Check = {other for other in _cells2Check if other < curr}
    othersValues = {sudoku[other] for other in cells2Check}
    validValues = {value for value in range(1, N + 1) if not value in othersValues}

    if len(validValues) == 0:  # No valid digit, so no valid solution. Return empty
        return []

    solutions = []
    for value in validValues:
        newSudoku = sudoku.copy()
        newSudoku[curr] = value
        solutions += findSolutions(newSudoku, curr + 1)
    return solutions


# Genuinely empty sudoku, counts permutations of digits
emptySudoku = [0] * (N**2)


allSolutions = findSolutions(emptySudoku, 0)
print("Number of total solutions:", len(allSolutions))

# Empty sudoku with arbitrary fixed first row, does counts only truly distinct solutions
emptySudoku[0:N] = [value for value in range(1, N + 1)]
distinctSolutions = findSolutions(emptySudoku, N)
for solution in distinctSolutions:
    printSudokuAscii(solution)
print("Number of distinct solutions:", len(distinctSolutions))

allPuzzles = 0
start = time.time()
for k, solution in enumerate(allSolutions):
    cellToPosibleSolutions = [
        # For each cell c, precompute all the solutions that have value solution[c] in cell c
        {j for (j, other) in enumerate(allSolutions) if (other[c] == solution[c])}
        for c in range(N**2)
    ]

    puzzles: list[int] = []

    # Iterate on all possible subsets
    # Large margins of improvements here: we do NOT need to iterate on ALL possible subsets, only
    # the plausible ones. For example, if a subset is of size N-2 or less, it surely cannot lead
    # to a unique solution, so it can be discarded early. Similarly, it's likely that we can
    # discard big subsets as they almost surely have a smaller valid subset in them.
    # However, getting an actual valid upperbound seems not so simple
    # masks = [i for i in range(2 ** (N**2)) if N - 1 <= i.bit_count() <= (N**2) / 2]
    for subsetMask in range(1, 2 ** (N**2)):
        subset = {i for i in range(N**2) if (subsetMask & (1 << i))}
        possibleSolutions = set.intersection(
            *[cellToPosibleSolutions[i] for i in subset]
        )
        if possibleSolutions != {k}:
            continue

        isMinimal = True
        for other in puzzles:
            if subsetMask & other == other:
                isMinimal = False
                break
        if not isMinimal:
            continue
        puzzles.append(subsetMask)

    end = time.time()
    allPuzzles += len(puzzles)
    print(
        f"\r{k + 1:03}/{len(allSolutions)}, elapsed time: {(end - start):.2f}s", end=""
    )

print()
print("Number of possible puzzles:", allPuzzles)
