#!/usr/bin/env python
# encoding: utf-8
"""
Features.py

Created by Vidya Ramesh on 2012-11-19.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import parser 
import sudoku

class Features: 
  
  #This will run arc-consistency 
  def arc_consistency(self, sudoku):
    domains = dict()
    for i in range(0, 9): 
      domains[i] = dict()
    size_of_domain = 0 
    total_domains = list()
    for round in range(10): 
      for i in range(9): 
        for j in range(9): 
          domains[i][j] = sudoku.getLegalMoves(i, j)
          size_of_domain += len(domains[i][j])
          if len(domains[i][j]) == 1: 
            sudoku.setSquare(i, j, domains[i][j][0])
      total_domains.append(size_of_domain)
      size_of_domain = 0
    return total_domains
  
  def feature_4(self, sudoku):
    max_number = -sys.maxint-1
    for i in range(9): 
      col = sudoku.getCol(i)
      number_filled = 0
      for x in col: 
        if x != 0: 
          number_filled += 1
      max_number = max(number_filled, max_number)
    for i in range(9): 
      row = sudoku.getRow(i)
      number_filled = 0
      for x in row: 
        if x != 0: 
          number_filled += 1
      max_number = max(number_filled, max_number)
    for i in range(3): 
      for j in range(3): 
        filled = 0
        square = sudoku.getSquare(i*3, j*3)
        for x in square: 
          if x != 0: 
            filled += 1
        max_number = max(filled, max_number)
    return max_number

  def feature_5(self, sudoku):
    counts = dict()
    for i in range(10): 
      counts[i] = 0
    for row in sudoku.puzzle: 
      for square in row: 
        counts[square] += 1
    maxval = 0
    for key in counts.keys():
      if key == 0: 
        continue
      keyval = counts[key]
      maxval = max(keyval, maxval)
    return maxval 
  
  def isSolvableByAC(self, sudoku):
    domains = dict()
    for i in range(0, 9): 
      domains[i] = dict()
    prev_domain = None
    size_of_domain = 0 
    while True:
      for i in range(9): 
        for j in range(9): 
          domains[i][j] = sudoku.getLegalMoves(i, j)
          size_of_domain += len(domains[i][j])
          if len(domains[i][j]) == 1: 
            sudoku.setSquare(i, j, domains[i][j][0])
      if (prev_domain == domains):
        return False
      if (sudoku.isComplete()):
        return True
      prev_domain = domains


puzzles = parser.Parser().parse("sudoku_tests.txt")
feature = Features()
arc_consistencies = dict()
solvables = dict()
for puzzle in puzzles: 
  arc_consistencies[puzzle] = feature.arc_consistency(puzzle)
for puzzle,values in arc_consistencies.items(): 
  print puzzle.getDifficulty(), values[9] - values[0], feature.isSolvableByAC(puzzle)
puzzles[0].reset()
print feature.feature_5(puzzles[0])