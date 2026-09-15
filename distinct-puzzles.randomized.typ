#set page(paper: "a5", margin: (x: 1cm, y: 1.5cm))
#let sudokuWidth = 3cm
#set text(font: "Roboto")

#let mapSymbols = value => {
  if value == "0" {
    none
  } else if value == "1" {
    text(size: 1cm, math.square, baseline: -.1cm, stroke: .005cm)
  } else if value == "2" {
    text(size: 1.1cm, math.circle, baseline: -.08cm)
  } else if value == "3" {
    text(size: .7cm, math.star.stroked, baseline: -.01cm, stroke: .015cm)
  } else if value == "4" {
    text(size: 1.1cm, math.triangle, baseline: -.1cm, stroke: .01cm)
  }
}
#let puzzles = (
  csv("distinct-puzzles.randomized.csv").map(entry => {
    entry.map(mapSymbols)
  })
)


#align(center)[
  #v(25%)
  #set text(size: 24pt, weight: 500)
  Every 4x4 sudoku puzzle, \ in random order
]
#pagebreak()
#pagebreak()
#set page(numbering: "1")

#v(5%)
#h(.5cm) There are only 3568 distinct minimal 4x4 sudoku puzzles#footnote[a 4x4 sudoku puzzle is defined as a partially filled 4x4 sudoku grid with a unique solution. It is _minimal_ if by removing any of the given digits, the solution becomes not unique anymore. Two puzzles that have the same structure but permutated digits, are counted as one. If you count permutated puzzles as different puzzles, the number goes up to 85632.]. If you print them 3cm wide on an A5 paper, you'd only need 179 pages. If you did 2 pages per day (less than 30 minutes of sudoku per day) you'd be done in less than three months.

And then, you could go around saying that you "have done the 4x4 sudokus". Like, all of them.

If that feels like something you want to do, this is the book for you!

This book contains every possible distinct minimal 4x4 sudoku puzzle, in random order. Since the puzzles are given up to permutations of the digits, they are presented not with digits but with symbols (so that each symbol can potentially represent any digit). The four symbols are:

#align(center)[
  #text(size: 1cm, math.square, baseline: .05cm, stroke: .005cm)
  #text(
    size: 1.1cm,
    math.circle,
    baseline: .15cm,
  )
  #text(
    size: .7cm,
    math.star.stroked,
    baseline: .075cm,
    stroke: .015cm,
  )
  #text(size: 1.1cm, math.triangle, baseline: .09cm, stroke: .01cm)
]

#v(1.25cm)
*Rules:* fill each 4x4 grid with the four symbols above such that in every row, every column, and every outlined 2x2 box each symbol appears exactly once.


#pagebreak()
#pagebreak()
#set page(paper: "a5", margin: (x: 1cm, y: 1.5cm))
#for puzzle in puzzles {
  box(
    grid(
      columns: (
        sudokuWidth / 4,
        sudokuWidth / 4,
        sudokuWidth / 4,
        sudokuWidth / 4,
      ),
      rows: (
        sudokuWidth / 4,
        sudokuWidth / 4,
        sudokuWidth / 4,
        sudokuWidth / 4,
      ),
      align: center + horizon,
      stroke: (x, y) => (
        left: if calc.rem(x, 2) == 0 { .07cm } else { .025cm },
        right: if calc.rem(x, 2) == 0 { .025cm } else { .07cm },
        top: if calc.rem(y, 2) == 0 { .07cm } else { .025cm },
        bottom: if calc.rem(y, 2) == 0 { .025cm } else { .07cm },
      ),
      ..puzzle,
    ),
  )
  h(1fr)
}

#pagebreak(to: "odd")
#set page(margin: (x: 1.25cm, y: 1.5cm))

#v(10%)

On date #box[#line(length: 5cm, stroke: .02cm)] , \

I, #box[#line(length: 7cm, stroke: .02cm)]  , have solved every 4x4 sudoku puzzle. \

#v(1cm)

#h(1fr)
#box(
  align(center)[
    Signature \ \
    #line(length: 6cm, stroke: .02cm)
  ],
)
