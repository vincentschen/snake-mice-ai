import random
import subprocess
import time
import numpy
from copy import deepcopy
import snakeRules, mouseRules 
import config

class GameRules: 
  """
  Manages initialization and termination of a game
  """
  
  def newGame(self, dimensions, agents, numMice):
    game = Game(self, agents)
    game.state = GameState(dimensions, numMice)
    return game

  def process(self, state, game):
    if state.won():
      self.win(state, game)
    if state.lost():
      self.lose(state, game)

  def win(self, state, game):
    print "Win (Score = %d)" % state.score
    game.gameOver = True

  def lose(self, state, game):
    print "Lose (Score = %d" % state.score
    game.gameOver = True

class SnakeAgent:
  
  def __init__(self):
    self.agentIndex = 0
  
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
    #uncomment the following line to return average distance
    #return float(1)/float(numpy.mean(distanceToMouse))
    closestIndex = 0
    for i in range(1, len(distanceToMouse)):
      if distanceToMouse[i] < distanceToMouse[closestIndex]:
        closestIndex = i
    newSnakeHeadLoc = (state.snakePositions[0][0] + action[0], state.snakePositions[0][1] + action[1])
    return -1*manhattanDistance(state.micePositions[closestIndex], newSnakeHeadLoc)

class MouseAgent:
  
  def __init__(self, agentIndex):
    self.agentIndex = agentIndex
  
  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    return random.choice(legalActions)

class GameState: 
  """
  Holds holds info accessible by Game instance
  """

  def __init__(self, dimensions, numMice):
    self.isLose = False
    self.isWin = False
    self.dimensions = dimensions
    self.score = 0
    self.miceEaten = 0
    self.numMice = numMice
    
    randomLocations = set()
    while len(randomLocations) < numMice + 1:
      randomLocations.add((random.randint(0, dimensions[0]-1), random.randint(0, dimensions[1]-1)))

    self.snakePositions = [randomLocations.pop()]
    self.micePositions = list(set(randomLocations))
  
  def getLegalActions(self, agentIndex = 0):
    #if it's over-no legal action
    if self.won() or self.lost(): 
      return []
    if agentIndex == 0:
      return snakeRules.getLegalActions(self)
    else:
      return mouseRules.getLegalActions(self, agentIndex)
  
  def generateSuccessor(self, agentIndex, action):
    # Check that successors exist
    if self.won() or self.lost(): 
      raise Exception('Can\'t generate a successor of a terminal state.')
    
    # Copy current state
    state = GameState(self.dimensions, self.numMice)
    state.score = self.score
    state.miceEaten = self.miceEaten
    state.micePositions = deepcopy(self.micePositions)
    state.snakePositions = deepcopy(self.snakePositions)

    # Let agent's logic deal with its action's effects on the board
    if agentIndex == 0:  # Snake is moving
      snakeRules.applyAction(state, action) #TODO: implement snakeRules
    else:                # A mouse
      mouseRules.applyAction(state, action, agentIndex) #TODO: implement mouseRules
    return state

  def getState(self):
    return self

  def getMicePositions(self, agentIndex = 0):
    return self.micePositions

  def getSnakePositions(self):
    return self.snakePositions

  def getScore(self):
    return self.score

  def lost(self):
    return self.isLose

  def won(self):
    return self.isWin

  def displayGame(self):
    # process = subprocess.Popen("clear")
    numRows, numCols = self.dimensions
    grid = [["   " for col in range(numCols)] for row in range(numRows)]
    for mouseX, mouseY in self.micePositions:
        grid[mouseX][mouseY] = " * "
    headX, headY = self.snakePositions[0]
    grid[headX][headY] = " 0 "
    for snakeX, snakeY in self.snakePositions[1:]:
        grid[snakeX][snakeY] = " O "
    screen = ""
    for row in range(numRows):
        for col in range(numCols):
            screen += grid[row][col]
        screen += "\n"
    print screen
    print "Score: %d" % self.getScore()

class Game:
  """
  Manages control flow of a game
  """

  def __init__(self, rules, agents, snakeSpeed = 2):
    self.gameOver = False
    self.rules = rules
    self.agents = agents
    self.numSteps = 0
    self.snakeSpeed = snakeSpeed

  def agentGenerator(self, maxIndex):
    index = 0
    while True:
      yield index
      if index == maxIndex - 1:
        index = 0
        self.numSteps += 1
      elif self.numSteps % self.snakeSpeed == 0:
        index = index + 1
      else:
        index = index
        self.numSteps += 1

  def run(self):
    if config.DISPLAY:
      self.state.displayGame()
    agentIndexer = self.agentGenerator(len(self.agents))
    while not self.gameOver:
      agentIndex = agentIndexer.next()
      agent = self.agents[agentIndex]
      observedState = deepcopy(self.state)
      action = agent.getAction(observedState)
      if action == []:
        break
      self.state = self.state.generateSuccessor(agentIndex, action)
      if config.DISPLAY:
        self.state.displayGame()
      self.rules.process(self.state, self)
      time.sleep(config.SLEEP_TIME)
      
      
def runGames (numGames = config.DEFAULT_NUM_GAMES, dimensions = config.DEFAULT_DIMENSONS, numMice = config.DEFAULT_NUM_MICE):
  agents = [SnakeAgent()] + [MouseAgent(i) for i in range(1, numMice + 1)]
  rules = GameRules()
  games = []
  for i in range(numGames):
    game = rules.newGame(dimensions, agents, numMice)
    game.run()
    games.append(game)
  
  #pacman scoring
  scores = [game.state.getScore() for game in games]
  wins = [game.state.won() for game in games]
  winRate = wins.count(True) / float(len(wins))
  print 'Average Score:', sum(scores) / float(len(scores))
  print 'Scores:       ', ', '.join([str(score) for score in scores])
  print 'Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate)
  print 'Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins])
  
  return games

if __name__ == '__main__':
  runGames()

"""
snakeAgent.py 
  oracle
  basline
  keyboard 
  different models/heuristics 

    
Implementation Order: 

    GameState
    snakeRules
    MiceRules    
    GameController
    Game
      runGame
    SnakeAgents
"""