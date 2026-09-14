# How many 4x4 sudokus?

Random script to evaluate how many solutions and puzzles (up to permutations)
there are for 4x4 sudokus.

The contents of this script are discussed in this
[blog post](https://baldino.dev/blog/there-are-only-twelve-4x4-sudokus/)

|                                       | Result |
| ------------------------------------- | ------ |
| All possible solutions                | 288    |
| Structurally distinct solutions       | 12     |
| All minimal puzzles                   | 85632  |
| Structurally distinct minimal puzzles | 3568   |

The repo contains CSV files for the pre-computed solutions (all & distinct) and
puzzles (all & distinct):

- [all solutions (9.2 KB)](./all-solutions.csv)
- [distinct solutions (384 B)](./distinct-solutions.csv)
- [all puzzles (3.1 MB)](./all-puzzles.csv)
- [distinct puzzles (128 KB)](./distinct-puzzles.csv)

The CSV scheme for solutions is just `r1c1, r1c2, r1c3, r1c4, r2c1, ...`.

The CSV scheme for puzzles has the index of the corresponding solution as the
first value of each entry (0-padded, 0-indexed, in the same order as they appear
in the corresponding `*-solutions.csv`), then the values of the puzzle in the
same order `r1c1, r1c2, r1c3, r1c4, r2c1, ...`. A 0 means that the corresponding
digit is not given in the puzzle.
