class Sudoku:
  def __init__(self, puzzle):
    self.classification = puzzle.pop(0)
    self.puzzle = puzzle
    self.initialPuzzle = puzzle

  def getRow(self, i):
    return self.puzzle[i]

  def getColumn(self, j):
    column = [0] * 9
    for row in self.puzzle:
      column[j] = self[row][j]
    return column

  def getSquare(self, i, j):
    row = i / 3
    col = j / 3

    square = [0] * 9
    k = 0
    for r in range(row * 3, row * 3 + 3):
      for c in range(col * 3, col * 3 + 3):
        square[k] = puzzle[r][c]
        k += 1
    return square

  def getLegalMoves(self, i, j):
    if not self.puzzle[i][j] == 0:
      return []
    digits = range(1,10)
    for x in self.getRow(i):
      if digits.count(x) > 0:
        digits.remove(x)
    for y in self.getCol(j):
      if digits.count(y) > 0:
        digits.remove(y)
    for z in self.getSquare(i,j):
      if digits.count(z) > 0:
        digits.remove(z)
    return digits

  def setSquare(self, i, j, value):
    if puzzle[i][j] == 0:
      puzzle[i][j] = value

  
 
