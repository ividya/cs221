#!/usr/bin/env python
# encoding: utf-8

from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB

class Learner:
  def __init__(self, data_train, data_test):
    #data is a list of tuples (x,y), where x is a list representing a feature vector
    #and y is the classification of the feature vector
    self.train_data = list()
    self.test_data = list()
    
    self.train_data.extend(data_train)
    self.test_data.extend(data_test)
    
    #Create a dictionary of different classifiers
    self.clf = dict()
    self.clf["SGD"] = SGDClassifier(loss="hinge", penalty="l2", n_iter=100, shuffle=True)
    self.clf["SVM"] = svm.SVC()
    self.clf["NB"] = MultinomialNB()
    
    #Create a dictionary of "results" for each classifier
    #Each result is itself a dictionary of how many misclassified
    self.results = dict()
  
  '''
  Train the classifier specified by "classifier"
  '''
  def learn(self, classifier):
    X = list()
    Y = list()
    for x,y in self.train_data:
      X.append(x)
      Y.append(y)
    self.clf[classifier].fit(X, Y)
  
  '''
  Test the classifier specified by "classifier" on test data
  '''
  def test(self, classifier, testdata="test"):
    correct = 0.0
    total = 0.0
    wrong = dict()
    data = list()
    
    if (testdata == "train"):
      data.extend(self.train_data)
    else:
      data.extend(self.test_data)
    
    for x,y in data:
      predicted = self.predict(x, classifier)
      if predicted == y:
        correct += 1
      else:
        if not y in wrong.keys():
          wrong[y] = 1
        else:
          wrong[y] += 1
      total += 1
    if total != 0:
      self.results[classifier + "_" + testdata] = wrong
      return correct/total
    else:
      return -1
  
  '''
  Predict the classification of feature vector x using "classifier"
  '''
  def predict(self, x, classifier):
    return self.clf[classifier].predict(x)


def readExamples(path):
  examples = list()
  exampleFile = open(path)
  for line in exampleFile: 
    inputs = [int(x) for x in line.split()]
    level = inputs.pop(0)
    examples.append((inputs, level))
  exampleFile.close()
  return examples

trainExamples = readExamples('train_results.txt')
validationExamples = readExamples('tests_results.txt')
learner = Learner(trainExamples, validationExamples)

print "------------------------"
for cl in learner.clf.keys():
  learner.learn(cl)
  print "%s:" % (cl)
  print "train success rate: %.4f, validation success rate: %.4f" % (learner.test(cl, "train"), learner.test(cl, "test"))
  print "Results:"
  print "Train: " + str(learner.results[cl + "_train"])
  print "Test: " + str(learner.results[cl + "_test"])
  print "------------------------"