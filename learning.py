import util, random, math, sys
from math import exp, log
from util import Counter

import features
import sudoku


def getNumClassInSet(dataset):
  num = util.Counter()
  for x in dataset:
    num[x.classification] = num[x.classification] + 1
  return num

############################################################
# Feature extractors: a feature extractor should take a raw input x (tuple of
# tokens) and add features to the featureVector (Counter) provided.

def basicFeatureExtractor(x):
  featureVector = util.Counter()

  featureList = features.Features().feature_vector(x)
  i = 1
  for feature in featureList:
    featureVector[i] = feature
    i += 1

  return featureVector


############################################################
# You should implement the logistic, hinge, and squared loss.
# Each function takes a featureVector phi(x), output, y, weights, w and returns
# either the value of the loss at that point or the gradient of the loss at
# that point.

"""
The logistic loss, for a given weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 3)
@param weights: The weight vector assigning a weight to every feature
@return The scalar value of the logistic loss.
"""
def logisticLoss(featureVector, y, weights):
  "*** YOUR CODE HERE (around 2 lines of code expected) ***"
  wx = dotProduct(featureVector,weights)
  if (-wx)*y < -100: # basically 0
    return 0
  elif (-wx)*y > 100: # really, really big. Return infinity limit
    return (-wx)*y
  return log(1+exp((-wx)*y))

"""
The gradient of the logistic loss with respect to the weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The gradient [vector] of the logistic loss, with respect to w,
        the weights we are learning.
"""
def logisticLossGradient(featureVector, y, weights):
  "*** YOUR CODE HERE (around 3 lines of code expected) ***"
  if -(featureVector*weights)*y < -100: # basically 0
    return util.Counter()
  elif -(featureVector*weights)*y > 100: # really, really big. Return infinity limit.
    return featureVector * -y
  numerator = -y*exp(-dotProduct(featureVector,weights)*y)
  denominator = 1 + exp(-dotProduct(featureVector,weights)*y)
  return featureVector * (numerator/denominator)

"""
The hinge loss, for a given weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The scalar value of the hinge loss.
"""
def hingeLoss(featureVector, y, weights):
  "*** YOUR CODE HERE (around 2 lines of code expected) ***"
  loss = 1 - (weights*featureVector)*y
  return max(loss,0)

"""
The gradient of the hinge loss with respect to the weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The gradient [vector] of the hinge loss, with respect to w,
        the weights we are learning.
        You should not worry about the case when the hinge loss is exactly 1
"""
def hingeLossGradient(featureVector, y, weights):
  "*** YOUR CODE HERE (around 3 lines of code expected) ***"
  if (hingeLoss(featureVector, y, weights) == 0):
    return util.Counter()
  else:
    return featureVector * (-y)

"""
The squared loss, for a given weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The scalar value of the squared loss.
"""
def squaredLoss(featureVector, y, weights):
  "*** YOUR CODE HERE (around 2 lines of code expected) ***"
  residual = math.copysign(1,weights*featureVector) - y
  return (residual**2)/2

"""
The gradient of the squared loss with respect to the weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The gradient [vector] of the squared loss, with respect to w,
        the weights we are learning.
"""
def squaredLossGradient(featureVector, y, weights):
  "*** YOUR CODE HERE (around 2 lines of code expected) ***"
  residual = featureVector*weights - y
  return featureVector * residual

def dotProduct(vector1, vector2):
  prod = 0
  for key in vector1.keys():
    prod += vector1[key] * vector2[key]
  return prod
    

class StochasticGradientLearner():
  def __init__(self, featureExtractor):
    self.featureExtractor = util.memoizeById(featureExtractor)

  """
  This function takes a list of training examples and performs stochastic 
  gradient descent to learn weights.
  @param trainExamples: list of training examples (you should only use this to
                        update weights).
                        Each element of this list is a list whose first element
                        is the input, and the second element, and the second
                        element is the true label of the training example.
  @param validationExamples: list of validation examples (just to see how well
                             you're generalizing)
  @param loss: function that takes (x, y, weights) and returns a number
               representing the loss.
  @param lossGradient: function that takes (x, y, weights) and returns the
                       gradient vector as a counter.
                       Recall that this is a function of the featureVector,
                       the true label, and the current weights.
  @param options: various parameters of the algorithm
     * initStepSize: the initial step size
     * stepSizeReduction: the t-th update should have step size:
                          initStepSize / t^stepSizeReduction
     * numRounds: make this many passes over your training data
     * regularization: the 'lambda' term in L2 regularization
  @return No return value, but you should set self.weights to be a counter with
          the new weights, after learning has finished.
  """
  def learn(self, trainExamples, validationExamples, loss, lossGradient, options):
    #We have 5 classes, so we need 5 weight vectors to update
    self.weights = [util.Counter() for i in range(5)]
    random.seed(42)
    
    print getNumClassInSet(trainExamples)
    print getNumClassInSet(validationExamples)

    # You should go over the training data numRounds times.
    # Each round, go through all the examples in some random order and update
    # the weights with respect to the gradient.
    for round in range(0, options.numRounds):
      random.shuffle(trainExamples)
      numUpdates = 0  # Should be incremented with each example and determines the step size.
      # Loop over the training examples and update the weights based on loss and regularization.
      # If your code runs slowly, try to explicitly write out the dot products
      # in the code here (e.g., "for key,value in counter: counter[key] += ---"
      # rather than "counter * other_vector")
      reg = float(options.regularization) / len(trainExamples)
      for x in trainExamples:
        numUpdates += 1
        "*** YOUR CODE HERE (around 7 lines of code expected) ***"
        featureVector = self.featureExtractor(x)
        stepSize = options.initStepSize / (numUpdates**options.stepSizeReduction)

        for c in range(5):
          penalty = util.Counter()
          if not reg == 0:
              penalty = self.weights[c] * reg
          if x.getIntLevel() == c+1: y = 1
          else: y = -1
          lGradient = lossGradient(featureVector, y, self.weights[c])
          self.weights[c] -= (lGradient + penalty) * stepSize

      for i in range(len(self.weights)):
        print i+1, self.weights[i]
      # Compute the objective function.
      # Here, we have split the objective function into two components:
      # the training loss, and the regularization penalty.
      # The objective function is the sum of these two values
      trainLoss = 0  # Training loss
      regularizationPenalty = 0  # L2 Regularization penalty
      "*** YOUR CODE HERE (around 5 lines of code expected) ***"
      self.objective = dict()
      for c in range(5):
        for key in self.weights[c].keys():
          regularizationPenalty += ((self.weights[c][key])**2) / 2
        regularizationPenalty *= options.regularization
        for x in trainExamples:
          featureVector = self.featureExtractor(x)
          if x.getIntLevel() == c+1: y = 1
          else: y = -1
          trainLoss = trainLoss + loss(featureVector, y, self.weights[c])
        self.objective[c] = trainLoss + regularizationPenalty

      # See how well we're doing on our actual goal (error rate).
      trainError = self.getNumErrors(trainExamples) / len(trainExamples)
      validationError = self.getNumErrors(validationExamples) / len(validationExamples)

      print "Round %s/%s: train error = %.4f, validation error = %.4f" % (round+1, options.numRounds, trainError, validationError)
      for i in range(5):
        print "objective = %.2f" % (self.objective[i])

    # Print out feature weights
    out = open('weights.txt', 'w+')
    for i in range(len(self.weights)):
      print >>out, "label: " + i + " weights: " +" ".join(str(w) for w in self.weights[i])
    out.close()

  def getNumErrors(self, examples):
    errors = 0
    for x in examples:
      if x.getIntLevel() != self.predict(x):
        errors += 1
    return 1.0 * errors


  """
  Classify a new input based on the current weights (self.weights).
  Note that this function should be agnostic to the loss
  you are using for training.
  You may find the following fields useful:
    self.weights: Your current weights
    self.featureExtractor(): A function which takes a datum as input and
                             returns a featurized version of the datum.
  @param x An input example, not yet featurized.
  @return class with best possible chance of being correct
  """
  def predict(self, x):
    "*** YOUR CODE HERE (around 3 lines of code expected) ***"
    phiX = self.featureExtractor(x)
    predictors = [w * phiX for w in self.weights]
    m = max(predictors)
    return predictors.index(m) + 1

# After you have tuned your parameters, set the hyperparameter options:
# featureExtractor, loss, initStepSize, stepSizeReduction, numRounds, regularization, etc.
# The autograder will call this function before calling learn().
def setTunedOptions(options):
  "*** YOUR CODE HERE (around 6 lines of code expected) ***"
  loss = hingeLoss
  lossGradient = hingeLossGradient
  featureExtractor = basicFeatureExtractor
  options.initStepSize = 1
  options.stepSizeReduction = 0.2
  options.numRounds = 10
  options.regularization = 0.1

if __name__ == '__main__':
  util.runLearner(sys.modules[__name__], sys.argv[1:])
