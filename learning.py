import util, random, math, sys
from math import exp, log
from util import Counter

import features
import sudoku

############################################################
# Feature extractors: a feature extractor should take a raw input x (tuple of
# tokens) and add features to the featureVector (Counter) provided.

def basicFeatureExtractor(x):
  url, title = x
  featureVector = util.Counter()

  features = features.feature_vector(x)
  i = 1
  for feature in features:
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
  numerator = -y*exp(-(dotProduct(featureVector,weights))*y)
  denominator = 1 + exp(-(dotProduct(featureVector,weights))*y)
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
    return featureVector * 0
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
  residual = dotProduct(featureVector, weights) - y
  return featureVector * residual

"""
Helper method to calculate the dot product of two vectors
"""
def dotProduct(vector1, vector2):
  prod = 0
  for key in vector1.keys(): prod += vector1[key] * vector2[key]
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
    self.weights = util.Counter()
    random.seed(42)

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
      for x, y in trainExamples:
        numUpdates += 1
        "*** YOUR CODE HERE (around 7 lines of code expected) ***"
        featureVector = self.featureExtractor(x)
        stepSize = options.initStepSize / (numUpdates**options.stepSizeReduction)
        penalty = util.Counter()
        if not reg == 0:
            penalty = self.weights * reg
        lGradient = lossGradient(featureVector, y, self.weights)
        self.weights -= (lGradient + penalty) * stepSize
        if numUpdates % 500 == 0: print numUpdates
        
      # Compute the objective function.
      # Here, we have split the objective function into two components:
      # the training loss, and the regularization penalty.
      # The objective function is the sum of these two values
      trainLoss = 0  # Training loss
      regularizationPenalty = 0  # L2 Regularization penalty
      "*** YOUR CODE HERE (around 5 lines of code expected) ***"
      for url in self.weights.keys():
        regularizationPenalty += ((self.weights[url])**2) / 2
      regularizationPenalty *= options.regularization
      for x, y in trainExamples:
        featureVector = self.featureExtractor(x)
        trainLoss = trainLoss + loss(featureVector, y, self.weights)
      self.objective = trainLoss + regularizationPenalty

      # See how well we're doing on our actual goal (error rate).
      trainError = util.getClassificationErrorRate(trainExamples, self.predict, 'train', options.verbose, self.featureExtractor, self.weights)
      validationError = util.getClassificationErrorRate(validationExamples, self.predict, 'validation', options.verbose, self.featureExtractor, self.weights)

      print "Round %s/%s: objective = %.2f = %.2f + %.2f, train error = %.4f, validation error = %.4f" % (round+1, options.numRounds, self.objective, trainLoss, regularizationPenalty, trainError, validationError)

    # Print out feature weights
    out = open('weights', 'w')
    for f, v in sorted(self.weights.items(), key=lambda x: -x[1]):
      print >>out, f + "\t" + str(v)
    out.close()

  """
  Classify a new input into either +1 or -1 based on the current weights
  (self.weights). Note that this function should be agnostic to the loss
  you are using for training.
  You may find the following fields useful:
    self.weights: Your current weights
    self.featureExtractor(): A function which takes a datum as input and
                             returns a featurized version of the datum.
  @param x An input example, not yet featurized.
  @return +1 or -1
  """
  def predict(self, x):
    "*** YOUR CODE HERE (around 3 lines of code expected) ***"
    phiX = self.featureExtractor(x)
    return math.copysign(1, self.weights * phiX)

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
