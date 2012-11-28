class Sudoku:
  def __init__(self, puzzle):
    self.classification = puzzle.pop(0)
    self.puzzle = puzzle
    self.initialPuzzle = list()
    for row in self.puzzle: 
      self.initialPuzzle.append(list(row))
    if len(self.puzzle) < 9: 
      print "eRROR"
      print len(self.puzzle)
      print self.puzzle

  def getDifficulty(self):
    return self.classification

  def hasEmptyDomain(self):
    for i in range(9):
      for j in range(9): 
        if len(getLegalMoves(i, j)) == 0: 
          return True
    return False
  

  def getEmptySquares(self):
    squares = list()
    for i in range(9): 
      for j in range(9): 
        if self.puzzle[i][j] == 0: 
          squares.append((i, j))
    return squares

  def getRow(self, i):
    return self.puzzle[i]

  def getCol(self, j):
    column = [0] * 9
    for i in range(9):
      column[i] = self.puzzle[i][j]
    return column

  def copy(self): 
    new_puzzle = list()
    new_puzzle.append(self.classification)
    for row in self.puzzle: 
      new_puzzle.append(list(row))
    new_s = Sudoku(new_puzzle)
    return new_s
  
  def getSquare(self, i, j):
    row = i / 3
    col = j / 3

    square = [0] * 9
    k = 0
    for r in range(row * 3, row * 3 + 3):
      for c in range(col * 3, col * 3 + 3):
        square[k] = self.puzzle[r][c]
        k += 1
    return square

  def reset(self):
    self.puzzle = self.initialPuzzle
  

  def getLegalMoves(self, i, j):
    if self.puzzle[i][j] > 0:
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
    if self.puzzle[i][j] == 0:
      self.puzzle[i][j] = value

  def isComplete(self):
    for i in range(9):
      for j in range(9):
        if (self.puzzle[i][j] == 0):
          return False
    return True

  def printPuzzle(self):
    for row in self.puzzle:
      print row
 
