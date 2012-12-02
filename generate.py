#!/usr/bin/env python
# encoding: utf-8
"""
generate.py

Created by Vidya Ramesh on 2012-11-28.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.

function generate(level): 
		if there are no stored puzzles at this level:
		while(true): 
			create an empty puzzle (where each square has all possible domains)
			while(there exists a domain d where length(d) > 1): 
				pick a random unassigned square s
				find the domain d of s 
				pick a random value v from d
				assign(s, v)
				arc_consistency(puzzle)
		
			r = random number between 9 and 72
			for r times: 
				remove_puzzle_squares(puzzle)
		
			classification = classify(puzzle)
			if classification == level: 
				break
			else: 
				stored_puzzles[classification].append(puzzle)
		else: 
			puzzle = stored_puzzles[level].pop()

		return puzzle
"""

import sys
import sudoku
import random 
import features
import knn

class Generate:
  
  stored = dict()
  feature = None

  def run(self, level):
    self.initialize()
    #self.basicCreate()
    return self.createSudoku(level)
  
  def initialize(self):
    self.stored['very easy'] = list()
    self.stored['easy'] = list()
    self.stored['medium'] = list()
    self.stored['hard'] = list()
    self.stored['fiendish'] = list()
    self.feature = features.Features()

  def classify(self, sudoku):
    feature_vector = self.feature.feature_vector(sudoku)
    level = feature_vector.pop(0)
    point = dict()
    point['features'] = feature_vector
    point = knn.classify(point, "train_results.txt", 5)
    level = int(point['level'])
    return level
  
  def createSudoku(self, level):
    extraGenerated = 0
    if len(self.stored[level]) == 0: 
      foundPuzzle = False
      while(not foundPuzzle): 
        su = sudoku.Sudoku(list())
        empties = su.getEmptySquares()
        randomChoice = random.choice(empties)
        domain = su.getLegalMoves(randomChoice[0], randomChoice[1])
        randomValue = random.choice(domain)
        su.setSquare(randomChoice[0], randomChoice[1], randomValue)
        self.feature.doRandomBacktracking(su, [])
        su = self.feature.backTrackingResult
      
        su.printSolution()
        
        if "easy" in level or "medium" in level: 
          keep = random.randrange(30, 35)
        else: 
          keep = random.randrange(17, 35)
        remove = 81 - keep
        for i in range(remove): 
          nonempties = su.getNonEmptySquares()
          choice = random.choice(nonempties)
          su.clearSquare(choice[0], choice[1])
        
        su.printPuzzle()
        
        su_level = self.classify(su)
        su.setClassification(su_level)
        if level == su.getDifficulty() or "easy" in level: 
          foundPuzzle = True
        else: 
          extraGenerated += 1
          self.stored[su.getDifficulty()].append(su)
    else: 
      su = self.stored[level].pop()
    return su
  
  def basicCreate(self):
    su = sudoku.Sudoku(list())
    empties = su.getEmptySquares()
    randomChoice = random.choice(empties)
    domain = su.getLegalMoves(randomChoice[0], randomChoice[1])
    randomValue = random.choice(domain)
    su.setSquare(randomChoice[0], randomChoice[1], randomValue)
    self.feature.doRandomBacktracking(su, [])
    su = self.feature.backTrackingResult
  

gen = Generate()
gen.run(sys.argv[1])