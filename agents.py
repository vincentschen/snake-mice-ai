import random
from snakeAgent import Agent
from util import * 

class GreedyAgent(Agent):

  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    if len(legalActions) == 0:
      return []
    scores = [self.evaluationFunction(state, action) for action in legalActions]
    bestScore = max(scores)
    bestIndices = [i for i, action in enumerate(scores) if scores[i] == bestScore]
    return legalActions[random.choice(bestIndices)]
  
  def evaluationFunction(self, state, action):
    distanceToMouse = [manhattanDistance(i, state.snakePositions[0])**(.5) for i in state.micePositions]
    #uncomment the following line to return average distance
    # return float(1)/float(numpy.mean(distanceToMouse))
    closestIndex = 0
    for i in range(1, len(distanceToMouse)):
      if distanceToMouse[i] < distanceToMouse[closestIndex]:
        closestIndex = i
    newSnakeHeadLoc = (state.snakePositions[0][0] + action[0], state.snakePositions[0][1] + action[1])
    return -1*manhattanDistance(state.micePositions[closestIndex], newSnakeHeadLoc)

class ExpectimaxAgent(Agent):

  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    if len(legalActions) == 0:
      return []
    scores = [self.evaluationFunction(state, action) for action in legalActions]
    bestScore = max(scores)
    bestIndices = [i for i, action in enumerate(scores) if scores[i] == bestScore]
    return legalActions[random.choice(bestIndices)]
  
  def evaluationFunction(self, state, action):
    
    straight_length_without_turn = getStraightLength(state)
    # straight_length_without_turn = 0
    
    weights = {
        'score': (1, state.score), 
        'straight_length_without_turn': (1, straight_length_without_turn)
    }
    
    # for key, weight in weights.iteritems(): print key, weight[0], weight[1]
    
    score = sum([val[0]*val[1] for key, val in weights.iteritems()])
    return score

class RandomMouse(Agent):
  
  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    return random.choice(legalActions)