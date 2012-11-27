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
  for test_point in determined_set: 
    dist = compute_distance(data_point['features'], test_point['features'])
    if data_point['features'] == test_point['features'] or dist == 0: 
      data_point['level'] = test_point['level']
      return data_point
    else: 
      if dist in k_closest:
        k_closest[dist].append(test_point)
      else: 
        k_closest[dist] = list()
        k_closest[dist].append(test_point)
  sorted_list = k_closest.keys()
  sorted_list.sort()
  level = 0.0
  for i in range(k): 
    dist = sorted_list[i]
    points = k_closest[dist]
    level += len(points) * (1.0/dist) * points[0]['level']
  data_point['level'] = round(level)
  return data_point

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

