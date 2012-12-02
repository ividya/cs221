#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Vidya Ramesh on 2012-11-26.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.

Very Easy - 0
Easy - 1
Medium - 2
Hard - 3
Fiendishly Hard - 4
"""

import sys
import math
import random

def compute_distance(vector1, vector2):
  total = 0
  for i in range(len(vector1)): 
    total += (vector1[i] - vector2[i]) * (vector1[i] - vector2[i])
  return math.sqrt(total)

#Assumption is that data_point = dict, containing 'level' and 'features'
#Assumption is that determined_set is a set of data points with a given level 
#returning data point with level set
def run_algorithm(data_point, determined_set, k): 
  k_closest = dict()
  true_points = list()
  for test_point in determined_set: 
    dist = compute_distance(data_point['features'], test_point['features'])
    if data_point['features'] == test_point['features'] or dist == 0: 
      data_point['level'] = test_point['level']
      true_points.append(test_point)
    else: 
      if dist in k_closest:
        k_closest[dist].append(test_point)
      else: 
        k_closest[dist] = list()
        k_closest[dist].append(test_point)
  if len(true_points) > 1: 
    random_choice = random.choice(true_points)
    data_point['level'] = random_choice['level']
    return data_point
  if len(true_points) == 1: 
    return data_point 
  sorted_list = k_closest.keys()
  sorted_list.sort()
  level = 0.0
  total_distance = 0
  only_k_values = list()
  so_far = 0
  found_k = False
  for i in range(k): 
    dist = sorted_list[i]
    points = k_closest[dist]
    for point in points:
      if so_far == k: 
        found_k = True
        break 
      only_k_values.append((dist, point))
      so_far += 1
    if found_k: 
      break
  for dist,point in only_k_values:
    total_distance += dist
    level += dist * point['level']
  level = level/total_distance
  data_point['level'] =  round(level)
  return data_point

def run_all_test_points(test_features, train_features, k):
  test_points = open(test_features)
  train_features = open(train_features)
  results = list()
  determined_set = list()
  for line in train_features: 
    inputs = [int(x) for x in line.split()]
    level = inputs.pop(0)
    point = dict()
    point['features'] = inputs
    point['level'] = level
    determined_set.append(point)
  for line in test_points: 
    inputs = [int(x) for x in line.split()]
    true_level = inputs.pop(0)
    point = dict()
    point['true_level'] = true_level
    point['features'] = inputs
    results.append(run_algorithm(point, determined_set, k))
  wrong_result = 0
  correct_result = 0
  diff = 0
  for result in results: 
    if result['level'] != result['true_level']: 
      diff += abs(result['level'] - result['true_level'])
      wrong_result += 1
    else: 
      correct_result += 1
  output_file = "knn_output" + str(k) + ".txt"
  knn_output = open(output_file, "w+")
  print >>knn_output, "classified wrong: ", wrong_result
  print "classified wrong: ", wrong_result
  print >>knn_output, "classified correctly: ", correct_result
  print "classified correctly: ", correct_result
  diff = diff / wrong_result
  print >>knn_output, "difference on average: ", diff
  print "difference on average: ", diff

run_all_test_points("tests_results.txt", "train_results.txt", int(sys.argv[1]))
'''
data = dict()
data['features'] = [1, 1]
test_set = list()
for i in range(1, 16): 
  test_point = dict()
  test_point['level'] = i % 5
  test_point['features'] = [i, i]
  test_set.append(test_point)
print test_set
print run_algorithm(data, test_set, 3)
'''

