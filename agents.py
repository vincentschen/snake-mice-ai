import random
from snakeAgent import Agent

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
    def getStraightLength(self, state, action):
      if len(state.snakePositions) <= 1: #here any action will result in a straight length of 2
        return 2
      #this represents our current direction
      currentDirection = (state.snakePositions[0][0]-state.snakePositions[1][0], state.snakePositions[0][1]-state.snakePositions[1][1])
      #you picked the right action, so we can keep this straight line going
      if(action == currentDirection):
        currStraight = 3
        for pos in state.snakePositions[2:]:
          latest = state.snakePositions[straightLength-2]
          if pos == (latest[0] - currentDirection[0], latest[1] -currentDirection[1]) #subtract the current direction (cause we're working backwards)\
            straightLength += 1
          else:
            return straightLength
      #you picked the wrong direction, so we get two, the minimum
      else:
        return 2

    def manhattanDistance( xy1, xy2 ):
      return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )  
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
    def manhattanDistance( xy1, xy2 ):
      return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )  
    distanceToMouse = [manhattanDistance(i, state.snakePositions[0])**(.5) for i in state.micePositions]
    closestIndex = 0
    for i in range(1, len(distanceToMouse)):
      if distanceToMouse[i] < distanceToMouse[closestIndex]:
        closestIndex = i
    newSnakeHeadLoc = (state.snakePositions[0][0] + action[0], state.snakePositions[0][1] + action[1])
    return -1*manhattanDistance(state.micePositions[closestIndex], newSnakeHeadLoc)

class RandomMouse(Agent):
  
  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    return random.choice(legalActions)