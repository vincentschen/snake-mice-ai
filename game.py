import sys
from optparse import OptionParser
import random
import time
from copy import deepcopy
import snakeRules, mouseRules
import agents
import config
import evaluationFunctions

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
    
  def getNumAgents(self): 
    return self.numMice + 1

  def lost(self):
    return self.isLose

  def won(self):
    return self.isWin

  def displayGame(self):
    numRows, numCols = self.dimensions
    grid = [[" %s " % (config.GRID_SPACE) for col in range(numCols)] for row in range(numRows)]
    for mouseX, mouseY in self.micePositions:
        grid[mouseX][mouseY] = " %s " % (config.MOUSE)
    headX, headY = self.snakePositions[0]
    grid[headX][headY] =  " %s " % (config.SNAKE_HEAD)
    for snakeX, snakeY in self.snakePositions[1:]:
        grid[snakeX][snakeY] = " %s " % (config.SNAKE_BODY)
    screen = ""
    for row in range(numRows):
        for col in range(numCols):
            screen += grid[row][col]
        screen += "\n"
    print screen
    print "Score: %d" % self.getScore()

class Agent:
  """
  An abstract agent that must define a getAction method.
  """
  def __init__(self, index=0):
    self.agentIndex = index

  def getAction(self, state):
    """
    The Agent will receive a GameState and return an action.
    """
    raise NotImplementedError()

class Game:
  """
  Manages control flow of a game
  """

  def __init__(self, rules, agents, snakeSpeed = config.SNAKE_SPEED):
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

  def run(self, quiet):
    if not quiet:
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
      if not quiet:
        if config.SHOW_EACH_AGENT_MOVE:
          self.state.displayGame()
          time.sleep(config.SLEEP_TIME)

        else:
          # show simultaneous movements  
          if agentIndex == 0: 
            self.state.displayGame()
            time.sleep(config.SLEEP_TIME)
      
      self.rules.process(self.state, self)
      
          
def runGames (snakeAgent, mouseAgent, numGames = config.DEFAULT_NUM_GAMES, 
    quiet = config.DISPLAY, dimensions = config.DEFAULT_DIMENSONS, numMice = config.DEFAULT_NUM_MICE):
  agents = [snakeAgent] + [mouseAgent(i) for i in range(1, numMice + 1)]
  rules = GameRules()
  games = []
  for i in range(numGames):
    game = rules.newGame(dimensions, agents, numMice)
    game.run(quiet)
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

def main(argv):
    print argv
    
    parser = OptionParser()
    parser.add_option("-s", "--snake", action="store", type="string", dest="snakeAgent")
    parser.add_option("-n", "--numGames", action="store", type="int", dest="numGames")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
    parser.add_option("-d", "--depth", action="store", type="int", dest="depth")
    parser.add_option("-e", "--evalFn", action="store", type="string", dest="evalFn")

    (options, args) = parser.parse_args(argv)
    
    mouseAgent = agents.RandomMouse
    
    # set evaluation funciton 
    evalFn = agents.evaluationFunctionA #default 
    if options.evalFn.lower() == 'a':
        evalFn = agents.evaluationFunctionA
    elif options.evalFn.lower() == 'b':
        evalFn = agents.evaluationFunctionB
    elif options.evalFn.lower() == 'c':
        evalFn = agents.evaluationFunctionC
    
    # set snakeAgent
    snakeAgent = None
    if options.snakeAgent == "greedy":
        snakeAgent = agents.GreedyAgent
    elif options.snakeAgent == "oracle":
        snakeAgent = agents.GreedyAgent
        config.IS_ORACLE = True 
    elif options.snakeAgent == "expectimax": 
        snakeAgent = agents.ExpectimaxAgent
    elif options.snakeAgent == "minimax":
        snakeAgent = agents.MinimaxAgent
        mouseAgent = agents.ScaredMouse
    elif options.snakeAgent == "alphabeta": 
        snakeAgent = agents.AlphaBetaAgent
        mouseAgent = agents.ScaredMouse

    if options.depth is not None and options.evalFn is not None: initializedSnakeAgent = snakeAgent(evalFn, options.depth)
    else: initializedSnakeAgent = snakeAgent()
    
    if options.numGames is not None: runGames(initializedSnakeAgent, mouseAgent, numGames = options.numGames, quiet = options.quiet)
    else: runGames(initializedSnakeAgent, mouseAgent, quiet = options.quiet)

if __name__ == '__main__':
  main(sys.argv[1:])