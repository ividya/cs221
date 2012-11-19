import sys
import re

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
        if "hard" in line: 
          current_puzzle.append("hard")
        if "easy" in line: 
          current_puzzle.append("easy")
        if "medium" in line: 
          current_puzzle.append("medium")
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
          new_row.append("0")
        else: 
          new_row.append(box)
      if len(row_list) != 9: 
        print "ERROR ERROR ERROR"
        print line
        break
      #blah balh 
      current_puzzle.append(new_row)
      if row == 11: 
        row = 0
        all_puzzles.append(current_puzzle)
        current_puzzle = list()
        continue
      row += 1
    print "Puzzles parsed:", len(all_puzzles)
    print all_puzzles[0]
  


parser = Parser()
parser.parse(sys.argv[1])