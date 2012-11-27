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
      if (sudoku.isComplete):
        return True
      prev_domain = domains


puzzles = parser.Parser().parse("sudoku_tests.txt")
feature = Features()
arc_consistencies = dict()
for puzzle in puzzles: 
  arc_consistencies[puzzle] = feature.arc_consistency(puzzle)
  print feature.isSolvableByAC(puzzle)
for puzzle,values in arc_consistencies.items(): 
  print puzzle.getDifficulty(), values[9] - values[0]
