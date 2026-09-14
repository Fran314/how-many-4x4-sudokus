import math
import time
import csv

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

# In theory, we could evaluate all the distinct solutions by fixing the values
# of the first row of the empty sudoku to be [1, 2, ..., N], like so:
# ```python
# # Empty sudoku with arbitrary fixed first row, does counts only truly distinct solutions
# emptySudoku[0:N] = [value for value in range(1, N + 1)]
# distinctSolutions = findSolutions(emptySudoku, N)
# ```
#
# However, since we have already computer ALL the possible solutions, we can
# just take from these only the ones that already start with [1, 2, ..., N],
# as follows
distinctSolutions = [
    solution for solution in allSolutions if solution[0:N] == list(range(1, N + 1))
]
print("Number of distinct solutions:", len(distinctSolutions))

allPuzzlesPerSolution: list[list[int]] = []
start = time.time()
for i, solution in enumerate(allSolutions):
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
        subset = {b for b in range(N**2) if (subsetMask & (1 << b))}
        possibleSolutions = set.intersection(
            *[cellToPosibleSolutions[c] for c in subset]
        )
        if possibleSolutions != {i}:
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
    allPuzzlesPerSolution.append(puzzles)

    print(
        f"\r{i + 1:03}/{len(allSolutions)}, elapsed time: {(end - start):.2f}s", end=""
    )
# print("\r\x1b[K", end="")  # clear last progress line
print()

print(
    "Number of possible puzzles:",
    sum([len(allPuzzlesPerSolution[i]) for i in range(len(allPuzzlesPerSolution))]),
)

# Note! By construction of how we do the recursion in `findSolutions`, the first
# #len(distinctSolutions) solutions in allSolutions are actually the solutions starting with
# `1 2 ... N` in the first row (recursion goes cell by cell left-to-right top-to-bottom, and the
# recursion on each possible value has the same order of the actual values)
# This means that the first #len(distinctSolutions) in allPuzzles are actually the puzzles for the
# distinct solutions, meaning that they are all the puzzles up to permutations.
distinctPuzzlesPerSolution = [
    allPuzzlesPerSolution[i] for i in range(len(distinctSolutions))
]

print(
    "Number of distinct puzzles:",
    sum(
        [
            len(distinctPuzzlesPerSolution[i])
            for i in range(len(distinctPuzzlesPerSolution))
        ]
    ),
)

# === WRITE ===
with open("all-solutions.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(allSolutions)

with open("distinct-solutions.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(distinctSolutions)


with open("all-puzzles.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    for i in range(len(allPuzzlesPerSolution)):
        solution = allSolutions[i]
        puzzles = allPuzzlesPerSolution[i]
        for puzzleMask in puzzles:
            puzzle = [
                solution[b] if (puzzleMask & (1 << b)) else 0 for b in range(N**2)
            ]
            writer.writerow([f"{i:03}"] + puzzle)

with open("distinct-puzzles.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    for i in range(len(distinctPuzzlesPerSolution)):
        solution = distinctSolutions[i]
        puzzles = distinctPuzzlesPerSolution[i]
        for puzzleMask in puzzles:
            puzzle = [
                solution[b] if (puzzleMask & (1 << b)) else 0 for b in range(N**2)
            ]
            writer.writerow([f"{i:03}"] + puzzle)
