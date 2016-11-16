##########snake.py##########
def runGames (layout, snake, mice, display, numGames)
	# calculates overall stats: the average score, win rate, etc. 
  # calls GameController.NewGame
  
class GameController: #AKA ClassicGameRules in pacman.py
  newGame ()
    initializes GameState() 	
  	initializes Game()
  
  process () # checks to see if game is over
  win ()
  lose ()
  getProgress () # for showing score? 
	
	# other things related to total time? etc. etc. 
  
class GameState: # initializes game state and holds info accessible by Game
  # functions split for agent type
  data = {}
  data[snakePositions] = []
  data[mousePositions] = []
  data[layout] = []

  def __init__(self, layout):
    data[isLose] = False
    data[isWin] = False
    data[layout] = layout

  def getLegalActions( self, agentIndex = 0 ):
  	#if it's over—no legal action
		if self.isWin() or self.isLose(): 
  		return []
		if agentIndex == 0:  # Pacman is moving
    	return SnakeRules.getLegalActions( self ) #TODO: IMPLEMENT LEGAL ACTIONS FUNCTIONS 
    else:
    	return MouseRules.getLegalActions( self, agentIndex ) #TODO: IMPLEMENT LEGAL ACTIONS FUNCTIONS 
  
  
  generateSuccessor()
  	# generates current GameState() 
  	# checks current agent
  	# ticks (update score)
  	# 
        """
    Returns the successor state after the specified agent takes the action.
    """
    # Check that successors exist
    if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

    # Copy current state
    state = GameState(self)

    # Let agent's logic deal with its action's effects on the board
    if agentIndex == 0:  # Snake is moving
      state.data._eaten = [False for i in range(state.getNumAgents())]
      PacmanRules.applyAction( state, action )
    else:                # A ghost is moving
      GhostRules.applyAction( state, action, agentIndex )

    # Time passes
    if agentIndex == 0:
      state.data.scoreChange += -TIME_PENALTY # Penalty for waiting around
    else:
      GhostRules.decrementTimer( state.data.agentStates[agentIndex] )

    # Resolve multi-agent effects
    GhostRules.checkDeath( state, agentIndex )

    # Book keeping
    state.data._agentMoved = agentIndex
    state.data.score += state.data.scoreChange
    return state


  getState() / getStates()

  hasFood()

  def getPosition(agentIndex = 0):
    if agentIndex == 0:
      return self.data.snakePositions
    else:
      return self.data.mousePositions[agentIndex-1]

  def getPositions(agentIndex = 0):
    if agentIndex == 0:
      return self.data.snakePositions
    else:
      return self.data.mousePositions

  def isLose():
    return self.data.isLose

  def isWin()
    return self.data.isWin

##########game.py##########
class Game: # manages control flow 
	getProgress() 
  agentCrash() #? do we need this 
  run()
  	for every agent
  		agent.registerInitialState(state)
  
  	while game not over: # one agent per loop - line 581 game.py
  		# choose action for agent
  		# generate successor for agent i.e. execute action
  		# updating display
  		# controller processing state (rules in original) - line 672 game.py
  		# increment or roll over on agents
"""
snakeAgent.py 
  oracle
  basline
  keyboard 
  different models/heuristics 

    
Implementation Order: 
    SnakeRules
    MiceRules
    GameState
    GameController
    Game
    	runGame
    SnakeAgents
    
"""
    
    
    
    
    
    
    
    
    
    
    