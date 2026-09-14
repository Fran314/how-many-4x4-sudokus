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
import csv

N = 4
SQRT_N = int(math.sqrt(N))

type sudoku = list[int]


def sudokuToStrUnicode(sudoku: sudoku) -> str:
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
    topLine += "\n"
    midThin += "\n"
    midBold += "\n"

    output = topLine
    for y in range(N):
        output += "║"
        for x in range(N):
            i = x + y * N
            val = sudoku[i] or " "
            vert = "║" if x % SQRT_N == SQRT_N - 1 else "│"
            output += f" {val} {vert}"
        output += "\n"

        if y % SQRT_N != SQRT_N - 1:
            output += midThin
        elif y != N - 1:
            output += midBold
        else:
            output += btmLine
    return output


def sudokuToStrAscii(sudoku: sudoku) -> str:
    # +---+---+---+---+
    # |   :   |   :   |
    # + - + - + - + - +
    # |   :   |   :   |
    # +---+---+---+---+
    # |   :   |   :   |
    # + - + - + - + - +
    # |   :   |   :   |
    # +---+---+---+---+
    topLine = "+" + ("---+" * N) + "\n"
    midThin = "+" + (" - +" * N) + "\n"
    midBold = "+" + ("---+" * N) + "\n"
    btmLine = "+" + ("---+" * N)

    output = topLine
    for y in range(N):
        output += "|"
        for x in range(N):
            i = x + y * N
            val = sudoku[i] or " "
            vert = "|" if x % SQRT_N == SQRT_N - 1 else ":"
            output += f" {val} {vert}"
        output += "\n"

        if y % SQRT_N != SQRT_N - 1:
            output += midThin
        elif y != N - 1:
            output += midBold
        else:
            output += btmLine
    return output


# Given the string representation of a list of sudokus, group them so that
# there are #width sudokus per line. Basically (putting 3 sudokus per line):
#
#            [S1, S2, S3, S4, S5] -> "S1 S2 S3
#                                     S4 S5"
#
def groupStrSudokus(sudokus: list[str], width: int) -> str:
    output = ""
    height = math.ceil(len(sudokus) / width)
    for y in range(height):
        lines = [""] * (2 * N + 1)
        for x in range(width):
            if x + y * width >= len(sudokus):
                break
            sudoku = sudokus[x + y * width]
            for i, line in enumerate(sudoku.split("\n")):
                if x > 0:
                    lines[i] += "   "
                lines[i] += line

        if y > 0:
            output += "\n\n"
        output += "\n".join(lines)
    return output


allSolutions: list[sudoku] = []
distinctSolutions: list[sudoku] = []

with open("all-solutions.csv", "r") as f:
    data = csv.reader(f)
    allSolutions = [[int(cell) for cell in row] for row in data]

with open("distinct-solutions.csv", "r") as f:
    data = csv.reader(f)
    distinctSolutions = [[int(cell) for cell in row] for row in data]


allPuzzlesPerSolution: dict[int, list[sudoku]] = {
    i: [] for i in range(len(allSolutions))
}
distinctPuzzlesPerSolution: dict[int, list[sudoku]] = {
    i: [] for i in range(len(distinctSolutions))
}

with open("all-puzzles.csv", "r") as f:
    data = csv.reader(f)
    for row in data:
        solutionIndex = int(row[0])
        puzzle = [int(cell) for cell in row[1:]]
        allPuzzlesPerSolution[solutionIndex].append(puzzle)

with open("distinct-puzzles.csv", "r") as f:
    data = csv.reader(f)
    for row in data:
        solutionIndex = int(row[0])
        puzzle = [int(cell) for cell in row[1:]]
        distinctPuzzlesPerSolution[solutionIndex].append(puzzle)

# === WRITE === #
with open("all-solutions.ascii.txt", "w") as f:
    solutionsStrAscii = [sudokuToStrAscii(sol) for sol in allSolutions]
    output = groupStrSudokus(solutionsStrAscii, 6)
    f.write(output)

with open("all-solutions.unicode.txt", "w") as f:
    solutionsStrUnicode = [sudokuToStrUnicode(sol) for sol in allSolutions]
    output = groupStrSudokus(solutionsStrUnicode, 6)
    f.write(output)

with open("distinct-solutions.ascii.txt", "w") as f:
    solutionsStrAscii = [sudokuToStrAscii(sol) for sol in distinctSolutions]
    output = groupStrSudokus(solutionsStrAscii, 6)
    f.write(output)

with open("distinct-solutions.unicode.txt", "w") as f:
    solutionsStrUnicode = [sudokuToStrUnicode(sol) for sol in distinctSolutions]
    output = groupStrSudokus(solutionsStrUnicode, 6)
    f.write(output)

with open("all-puzzles.ascii.txt", "w") as f:
    for i in allPuzzlesPerSolution:
        solution = allSolutions[i]
        puzzles = allPuzzlesPerSolution[i]

        f.write("=" * 51 + f" Solution #{i:03} " + "=" * 51 + "\n")
        solStr = sudokuToStrAscii(solution)
        f.writelines(" " * 50 + line + "\n" for line in solStr.split("\n"))

        f.write("-" * 47 + " corresponding puzzles " + "-" * 47 + "\n")
        puzzlesStr = [sudokuToStrAscii(puzzle) for puzzle in puzzles]
        f.write(groupStrSudokus(puzzlesStr, 6) + "\n")

        f.write("=" * 117 + "\n")
        if i < len(allPuzzlesPerSolution) - 1:
            f.write("\n\n")

with open("all-puzzles.unicode.txt", "w") as f:
    for i in allPuzzlesPerSolution:
        solution = allSolutions[i]
        puzzles = allPuzzlesPerSolution[i]

        f.write("=" * 51 + f" Solution #{i:03} " + "=" * 51 + "\n")
        solStr = sudokuToStrUnicode(solution)
        f.writelines(" " * 50 + line + "\n" for line in solStr.split("\n"))

        f.write("-" * 47 + " corresponding puzzles " + "-" * 47 + "\n")
        puzzlesStr = [sudokuToStrUnicode(puzzle) for puzzle in puzzles]
        f.write(groupStrSudokus(puzzlesStr, 6) + "\n")

        f.write("=" * 117 + "\n")
        if i < len(allPuzzlesPerSolution) - 1:
            f.write("\n\n")

with open("distinct-puzzles.ascii.txt", "w") as f:
    for i in distinctPuzzlesPerSolution:
        solution = distinctSolutions[i]
        puzzles = distinctPuzzlesPerSolution[i]

        f.write("=" * 51 + f" Solution #{i:03} " + "=" * 51 + "\n")
        solStr = sudokuToStrAscii(solution)
        f.writelines(" " * 50 + line + "\n" for line in solStr.split("\n"))

        f.write("-" * 47 + " corresponding puzzles " + "-" * 47 + "\n")
        puzzlesStr = [sudokuToStrAscii(puzzle) for puzzle in puzzles]
        f.write(groupStrSudokus(puzzlesStr, 6) + "\n")

        f.write("=" * 117 + "\n")
        if i < len(distinctPuzzlesPerSolution) - 1:
            f.write("\n\n")


with open("distinct-puzzles.unicode.txt", "w") as f:
    for i in distinctPuzzlesPerSolution:
        solution = distinctSolutions[i]
        puzzles = distinctPuzzlesPerSolution[i]

        f.write("=" * 51 + f" Solution #{i:03} " + "=" * 51 + "\n")
        solStr = sudokuToStrUnicode(solution)
        f.writelines(" " * 50 + line + "\n" for line in solStr.split("\n"))

        f.write("-" * 47 + " corresponding puzzles " + "-" * 47 + "\n")
        puzzlesStr = [sudokuToStrUnicode(puzzle) for puzzle in puzzles]
        f.write(groupStrSudokus(puzzlesStr, 6) + "\n")

        f.write("=" * 117 + "\n")
        if i < len(distinctPuzzlesPerSolution) - 1:
            f.write("\n\n")
