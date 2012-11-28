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
import random

class Features:
  backTrackingCounter = 0 
  
  #This will run arc-consistency 
  def arc_consistency(self, sudoku, numRounds):
    domains = dict()
    for i in range(0, 9): 
      domains[i] = dict()
    size_of_domain = 0 
    total_domains = list()
    for round in range(numRounds): 
      for i in range(9): 
        for j in range(9): 
          domains[i][j] = sudoku.getLegalMoves(i, j)
          size_of_domain += len(domains[i][j])
          if len(domains[i][j]) == 1: 
            sudoku.setSquare(i, j, domains[i][j][0])
      total_domains.append(size_of_domain)
      size_of_domain = 0
    return total_domains

  def doBacktracking(self, sudoku, moveStack):
    empties = sudoku.getEmptySquares()
    if (len(empties) == 0):
      return True
    else:
      (i,j) = empties[0]
      domain = sudoku.getLegalMoves(i,j)
      moveStack.append(((i,j), sudoku.copy()))
      for value in domain:
        sudoku.setSquare(i,j,value)
        self.backTrackingCounter += 1
        if self.isSolvableByAC(sudoku):
          return True
        if not sudoku.hasEmptyDomain():
          if self.doBacktracking(sudoku, moveStack):
            return True
        sudoku = moveStack[-1][1].copy()
      moveStack.pop()
      return False
    
    
  
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

  def feature_6(self, sudoku):
    squares = []
    for i in range(3):
      for j in range(3):
        squares.append(sudoku.getSquare(i*3,j*3))
    maxNumComplete = 0
    for square in squares:
      numComplete = 0
      rows = [square[0:3], square[3:6], square[6:9]]
      cols = []
      for i in range(3):
        cols.append([rows[j][i] for j in range(3)])
      rows.extend(cols)
      
      for row in rows:
        if row.count(0) == 0:
          numComplete += 1
      if numComplete > maxNumComplete:
        maxNumComplete = numComplete
      if maxNumComplete == 3:
        break
    return maxNumComplete
  
  #this must be run after arc_consistency is run 10 times -> see feature.arc_consistency
  def feature_7(self, sudoku):
    counts = dict()
    for i in range(10): 
      counts[i] = 0
    for i in range(9): 
      for j in range(9): 
        domain = sudoku.getLegalMoves(i, j)
        for d in domain: 
          counts[d] += 1
    maxvalue = 0
    for key in counts.keys(): 
      if key == 0: 
        continue
      maxvalue = max(counts[key], maxvalue)
    return maxvalue


puzzles = parser.Parser().parse("sudoku_tests.txt")
feature = Features()
arc_consistencies = dict()

for puzzle in puzzles: 
  feature.backTrackingCounter = 0
  bt = feature.doBacktracking(puzzle, [])
  print bt,feature.backTrackingCounter
puzzles[0].reset()

