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
  backTrackingResult = None

  arcConsistencyCounter = 0
  
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
      self.backTrackingResult = sudoku
      return True
    else:
      (i,j) = empties[0]
      domain = sudoku.getLegalMoves(i,j)
      moveStack.append(((i,j), sudoku.copy()))
      for value in domain:
        sudoku.setSquare(i,j,value)
        self.backTrackingCounter += 1
        if self.isSolvableByAC(sudoku):
          self.backTrackingResult = sudoku
          return True
        if not sudoku.hasEmptyDomain():
          if self.doBacktracking(sudoku, moveStack):
            return True
        sudoku = moveStack[-1][1].copy()
      moveStack.pop()
      return False
    

  def doRandomBacktracking(self, sudoku, moveStack):
    empties = sudoku.getEmptySquares()
    if (len(empties) == 0):
      self.backTrackingResult = sudoku
      return True
    else:
      (i,j) = empties[0]
      domain = sudoku.getLegalMoves(i,j)
      moveStack.append(((i,j), sudoku.copy()))
      random.shuffle(domain)
      for value in domain:
        sudoku.setSquare(i,j,value)
        self.backTrackingCounter += 1
        if self.isSolvableByAC(sudoku):
          self.backTrackingResult = sudoku
          return True
        if not sudoku.hasEmptyDomain():
          if self.doRandomBacktracking(sudoku, moveStack):
            return True
        sudoku = moveStack[-1][1].copy()
      moveStack.pop()
      return False       
  
  def feature_1(self, sudoku):
    return len(sudoku.getNonEmptySquares())

  def feature_2(self, sudoku):
    return self.arc_consistency(sudoku, 10)

  def feature_3(self, sudoku):
    if isSolvableByAC(sudoku):
      return 1
    return 0

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
  
  def solvableByAC(self, sudoku):
    prev_domain = 0 
    rounds = 0
    while True: 
      domains = self.arc_consistency(sudoku, 1)
      rounds += 1
      diff = domains[0] - prev_domain
      prev_domain = domains[0]
      if diff != 0: 
        continue
      else: 
        if sudoku.isComplete():
          self.arcConsistencyCounter = rounds
          return True
        else: 
          return False
  
  def isSolvableByAC(self, sudoku):
    domains = dict()
    for i in range(0, 9):
      domains[i] = dict()
    prev_domain = None
    size_of_domain = 0 
    while True:
      self.arcConsistencyCounter += 1
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
    self.arc_consistency(sudoku, 10)
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
  
  #This function assumes that the sudoku given is the initial unsolved puzzle
  #This is the order of the features in the vector: 
  #1) the number of given squares
  #2) maximum number of squares given in a set (where set is defined as row, column or 3 by 3 square)
  #3) maximum number of rows or columns filled in a square
  #4) maximum number of squares where a digit is in the domain.
  #5) the number of domain variables eliminated in the first 10 rules
  #6) maximum number of squares that can be filled by a single digit after 10 rounds of arc consistency 
  #7) solvable with arc consistency
  #8) how many times we have to backtrack, min: 1
  def feature_vector(self, sudoku):
    vector = list()
    #Add the level of the puzzle
    vector.append(sudoku.getIntLevel())
    #there are 7 features in each list that is returned
    #1) the number of given squares
    given_squares = 81 - len(sudoku.getEmptySquares())
    vector.append(given_squares)
    #4) maximum number of squares given in a set (where set is defined as row, column or 3 by 3 square)
    given_in_set = self.feature_4(sudoku)
    vector.append(given_in_set)
    #6) maximum number of rows or columns filled in a square
    max_row_or_cols = self.feature_5(sudoku)
    vector.append(max_row_or_cols)
    #7) maximum number of squares where a digit is in the domain.
    max_in_domain = self.feature_6(sudoku)
    vector.append(max_in_domain)
    #2) the number of domain variables eliminated in the first 10 rules
    eliminated_domains = self.arc_consistency(sudoku, 10)
    size_of_domain_difference = eliminated_domains[0] - eliminated_domains[len(eliminated_domains)-1]
    vector.append(size_of_domain_difference)
    #5) maximum number of squares that can be filled by a single digit after 10 rounds of arc consistency 
    squares_filled = self.feature_7(sudoku)
    sudoku.reset()
    vector.append(squares_filled)
    #3) solvable with arc consistency
    self.arcConsistencyCounter = 0
    solvable = self.solvableByAC(sudoku)
    if solvable: 
      solvable = self.arcConsistencyCounter
    else: 
      solvable = 0 
    vector.append(solvable)
    sudoku.reset()
    #8) how many times we have to backtrack to solve
    self.doBacktracking(sudoku, [])
    vector.append(self.backTrackingCounter)
    self.backTrackingCounter = 0  
    return vector
  
  def create_features_file(self, name_of_feature_file, puzzles):
    output = open(name_of_feature_file, "w+")
    for puzzle in puzzles: 
      vector = self.feature_vector(puzzle)
      print >>output, " ".join(str(x) for x in vector)


#puzzles = parser.Parser().parse("test_all_levels.txt")
#feature = Features()
#print "parsed!"
#feature.create_features_file("tests_results.txt", puzzles)
#arc_consistencies = dict()

#for puzzle in puzzles: 
  #feature.backTrackingCounter = 0
  #bt = feature.doBacktracking(puzzle, [])
  #print bt,feature.backTrackingCounter
#puzzles[0].reset()

