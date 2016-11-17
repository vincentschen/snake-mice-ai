import random
import subprocess
from copy import deepcopy

MOVE_PENALTY = 1
MOUSE_REWARD = 20
MICE_TO_WIN = 50
  
class GameRules: 
  """
  Manages initialization and termination of a game
  """
  
  def newGame(self, dimensions, agents, numMice):
    game = Game(self, agents)
    game.state = GameState(dimensions, numMice)
    return game

  def process(self, state, game):
    if state.isWin():
      self.win(state, game)
    if state.isLose():
      self.lose(state, game)

  def win(self, state, game):
    print "Win (Score = %d)" % state.score
    game.gameOver = True

  def lose(self, state, game):
    print "Lose (Score = %d" % state.score
    game.gameOver = True

class SnakeRules:
  """
  Handles state changes for snake agent
  """
  
  def getLegalActions(state):
    possible_results = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    results = []
    agentPos = state.getSnakePositions[0]
    for move in possible_results:
      if isValidLocation(state, (agentPos[0] + move[0], agentPos[1] + move[1])):
        results.append(move)
    return results

  # valid location is any square in the grid, 
  # even if there's a mouse or snake tile there
  def isValidLocation(state, location):
    if location[0] >= state.dimensions[0] or location[1] >= state.dimensions[1]:
      return False
    for loc in [state.getSnakePositions()]:
      if loc == location:
        return False
    return True

  def applyAction(state, action):
    newLoc = (state.getSnakePositions()[0][0] + action[0], state.getSnakePositions()[0][1] + action[1])
    # itself or a wall, game over
    if not isValidLocation(newLoc):
      state.isLose = True
    # new tile has a mouse
    elif newLoc in state.getMicePositions():
      eatenMouseIndex = state.getMicePositions().index(newLoc)
      state.micePositions[eatenMouseIndex] = MouseRules.randomLocation(state)
      state.snakePositions.insert(0, newLoc)
      state.score += MOUSE_REWARD
      state.miceEaten += 1
      if state.miceEaten >= MICE_TO_WIN:
        state.isWin = True
    #new tile is empty
    else:   
      state.snakePositions.insert(0, newLoc)
      state.snakePositions.pop()
      state.score -= MOVE_PENALTY 

class MouseRules:
  """
  Handles state changes for mice agents
  """
  
  def getLegalActions(state, agentIndex):
    possible_results = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    results = []
    agentPos = state.getMicePositions()[agentIndex-1]
    for move in possible_results:
      if isValidLocation(state, (agentPos[0] + move[0], agentPos[1] + move[1])):
        results.append(move)
    return results

  def applyAction(state, action, agentIndex):
    newLoc = (state.micePositions[agentIndex-1] + action[0], state.micePositions[agentIndex-1] + action[1])
    state.micePositions[agentIndex-1] = newLoc

  #valid location is any square in the grid without a mouse or snake tile
  def isValidLocation(state, location):
    if location[0] >= state.dimensions[0] or location[1] >= state.dimensions[1]:
      return False
    for loc in [state.getSnakePositions() + state.getMicePositions()]:
      if loc == location:
        return False
    return True

  #returns a random location on the board not taken up by snake or mice
  def randomLocation(state):
    while True:
      possible = (random.randint(0, state.dimensions[0] - 1), random.randint(0, state.dimensions[1] - 1))
      if isValidLocation(possible):
        return possible

class SnakeAgent:
  
  def __init__(self):
    self.agentIndex = 0

  def manhattanDistance( xy1, xy2 ):
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )
  
  def getAction(self, state):
    legalActions = state.getLegalActions(agentIndex)
    scores = [self.evaluationFunction(state, action) for action in legalActions]
    bestScore = max(scores)
    bestIndices = [i for i, action in enumerate(scores) if scores[i] == bestScore]
    return legalActions[random.choice(bestIndices)]
  
  def evaluationFunction(self, state, action):
    distanceToMouse = [manhattanDistance(i, state.snakePositions[0]) for i in state.micePositions]
    closestIndex = 0
    for i in range(1, len(distanceToMouse)):
      if distanceToMouse[i] < distanceToMouse[closestIndex]:
        closestIndex = i
    newSnakeHeadLoc = (state.snakePositions[0][0] + action[0], state.snakePositions[0][1] + action[1])
    return manhattanDistance(state.micePositions[closestIndex], newSnakeHeadLoc)

class MouseAgent:
  
  def __init__(self, agentIndex):
    self.agentIndex = agentIndex
  
  def getAction(self, state):
    legalActions = state.getLegalActions(agentIndex)
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
    self.snakePositions = [MouseRules.randomLocation(dimensions)]
    self.micePositions = [MouseRules.randomLocation(dimensions) for i in range(numMice)]

  def getLegalActions(self, agentIndex = 0):
    #if it's over-no legal action
    if self.isWin() or self.isLose(): 
      return []
    if agentIndex == 0:  # Pacman is moving
      return SnakeRules.getLegalActions(self) #TODO: IMPLEMENT LEGAL ACTIONS FUNCTIONS 
    else:
      return MouseRules.getLegalActions(self, agentIndex) #TODO: IMPLEMENT LEGAL ACTIONS FUNCTIONS 
  
  def generateSuccessor(self, agentIndex, action):
    # Check that successors exist
    if self.isWin() or self.isLose(): 
      raise Exception('Can\'t generate a successor of a terminal state.')
    # Copy current state
    state = GameState(self)
    # Let agent's logic deal with its action's effects on the board
    if agentIndex == 0:  # Snake is moving
      SnakeRules.applyAction(state, action) #TODO: implement snakerules
    else:                # A mouse
      MouseRules.applyAction(state, action, agentIndex) #TODO: implement mouserules
    return state

  def getState(self):
    return self

  def getMicePositions(self, agentIndex = 0):
    return self.micePositions

  def getSnakePositions(self):
    return self.snakePositions

  def getScore(self):
    return self.score

  def isLose(self):
    return self.isLose

  def isWin(self):
    return self.isWin

  def displayGame(self):
    process = subprocess.Popen("clear")
    numRows, numCols = self.dimensions
    grid = [["[ ]" for col in range(numCols)] for row in range(numRows)]
    for mouseX, mouseY in self.micePositions:
        grid[mouseX][mouseY] = "[m]"
    headX, headY = self.snakePositions[0]
    grid[headX][headY] = "[S]"
    for snakeX, snakeY in self.snakePositions[1:]:
        grid[snakeX][snakeY] = "[s]"
    screen = ""
    for row in range(numRows):
        for col in range(numCols):
            screen += grid[row][col]
        screen += "\n"
    print screen
    print "Score: %d" % score

class Game:
  """
  Manages control flow of a game
  """

  def __init__(self, rules, agents):
    self.gameOver = False
    self.rules = rules
    self.agents = agents
    self.numSteps = 0

  def run(self):
    self.state.displayGame()
    agentIndex = 0
    while not self.gameOver:
      agent = self.agents[agentIndex]
      observedState = self.state.deepcopy()
      action = agent.getAction(observedState)
      self.state = self.state.generateSuccessor(agentIndex, action)
      self.state.displayGame()
      self.rules.process()
      if agentIndex == len(self.agents) + 1:
        self.numSteps += 1
      agentIndex = (agentIndex + 1) % len(self.agents)
      
def runGames (dimensions, numMice, numGames):
  agents = [SnakeAgent()] + [MouseAgent(i) for i in range(1, numMice + 1)]
  rules = GameRules()
  games = []
  for i in range(numGames):
    game = rules.newGame(dimensions, agents, numMice)
    game.run()
    games.append(game)
  
  #pacman scoring
  scores = [game.state.getScore() for game in games]
  wins = [game.state.isWin() for game in games]
  winRate = wins.count(True) / float(len(wins))
  print 'Average Score:', sum(scores) / float(len(scores))
  print 'Scores:       ', ', '.join([str(score) for score in scores])
  print 'Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate)
  print 'Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins])
  
  return games

if __name__ == '__main__':
  runGames((30, 30), 3, 1)

"""
snakeAgent.py 
  oracle
  basline
  keyboard 
  different models/heuristics 

    
Implementation Order: 

    GameState
    SnakeRules
    MiceRules    
    GameController
    Game
      runGame
    SnakeAgents
"""