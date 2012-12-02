import sys
import re
import sudoku

class Parser: 
  
  def parse(self, filename): 
    the_file = open(filename)
    
    pattern = "[0-9\.]"
    prog = re.compile(pattern)
    all_puzzles = list()
    current_puzzle = list()
    row = 0
    for line in the_file: 
      if row == 0: 
        if "very easy" in line:
          current_puzzle.append("very easy")
        else: 
          if "hard" in line: 
            current_puzzle.append("hard")
          if "easy" in line: 
            current_puzzle.append("easy")
          if "medium" in line: 
            current_puzzle.append("medium")
          if "fiendish" in line: 
            current_puzzle.append("fiendish")
        row += 1
        continue
      if row == 4 or row == 8: 
        row += 1
        continue
      #Read in the current row to the row dict
      row_list = list()
      row_list = prog.findall(line)
      new_row = list()
      for box in row_list: 
        if box == ".": 
          new_row.append(0)
        else: 
          new_row.append(int(box))
      if len(row_list) != 9: 
        print "ERROR ERROR ERROR"
        print line
        break
      #blah balh 
      current_puzzle.append(new_row)
      if row == 11: 
        row = 0
        all_puzzles.append(current_puzzle)
        if len(current_puzzle) != 10: 
          print current_puzzle
          print "ASFDLJASLFKJDSAs"
        current_puzzle = list()
        continue
      row += 1
    print "Puzzles parsed:", len(all_puzzles)
    sudokus = list()
    for puzzle in all_puzzles: 
      sudokus.append(sudoku.Sudoku(puzzle))
    return sudokus

  