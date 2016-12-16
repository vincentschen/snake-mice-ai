import random
from snakeAgent import Agent
from util import *

def evaluationFunctionA(state):        
  
  weights = {
      'score': (20, state.score),    #                                   
      'distance_to_closest_mouse': (-1, distanceToClosestMouse(state)),                             # range
      'straight_length_without_turn': (1, getStraightLength(state)),                                # range 0 -> max(width, length)
    #   'legal_action_count': (20, len(state.getLegalActions()) > 1),                                        # range 0 -> 3
    #   'snake_rectangle_area': (3, getSnakeRectangleArea(state.snakePositions, state.dimensions)),    # range 0 -> width * length
    #   'area_blocked_by_snake': (-10, getAreaBlockedBySnake(state.snakePositions, state.dimensions)),
    #   'num_blocked_adjacent_tiles': (-1, 10*numBlockedAdjacentTiles(state)*state.miceEaten),
    #   'corners_in_snake': (-1, getNumSnakeCorners(state.snakePositions))
  }
  
  # for key, weight in weights.iteritems(): print key, weight[0], weight[1]
  score = sum([val[0]*val[1] for key, val in weights.iteritems()])
   
  return score

def evaluationFunctionB(state):        
  
  weights = {
    #   'score': (20, state.score),    #                                   
      'distance_to_closest_mouse': (-1, distanceToClosestMouse(state)),                             # range
      'straight_length_without_turn': (1, getStraightLength(state)),                                # range 0 -> max(width, length)
    #   'legal_action_count': (20, len(state.getLegalActions()) > 1),                                        # range 0 -> 3
    #   'snake_rectangle_area': (3, getSnakeRectangleArea(state.snakePositions, state.dimensions)),    # range 0 -> width * length
    #   'area_blocked_by_snake': (-10, getAreaBlockedBySnake(state.snakePositions, state.dimensions)),
      'num_blocked_adjacent_tiles': (-1, 10*numBlockedAdjacentTiles(state)*state.miceEaten),
    #   'corners_in_snake': (-1, getNumSnakeCorners(state.snakePositions))
  }
  
  # for key, weight in weights.iteritems(): print key, weight[0], weight[1]
  score = sum([val[0]*val[1] for key, val in weights.iteritems()])
   
  return score
  
def evaluationFunctionC(state):        
  weights = {
      'score': (20, state.score),    #                                   
      'distance_to_closest_mouse': (-1, distanceToClosestMouse(state)),                             # range
      'straight_length_without_turn': (1, getStraightLength(state)),                                # range 0 -> max(width, length)
      'legal_action_count': (20, len(state.getLegalActions()) > 1),                                        # range 0 -> 3
      'snake_rectangle_area': (3, getSnakeRectangleArea(state.snakePositions, state.dimensions)),    # range 0 -> width * length
      'area_blocked_by_snake': (-10, getAreaBlockedBySnake(state.snakePositions, state.dimensions)),
      'num_blocked_adjacent_tiles': (-1, 10*numBlockedAdjacentTiles(state)*state.miceEaten),
    #   'corners_in_snake': (-1, getNumSnakeCorners(state.snakePositions))
  }
 
  # for key, weight in weights.iteritems(): print key, weight[0], weight[1]
  score = sum([val[0]*val[1] for key, val in weights.iteritems()])
   
  return score
  
class MultiAgentSearchAgent(Agent):
  """
  Abstract class that can be extended for agents that use depth for eval fns. 
  """

  def __init__(self, evalFn, depth = '2'):
    self.index = 0 # Snake is always agent index 0
    self.evaluationFunction = evalFn
    self.depth = int(depth)

class GreedyAgent(Agent):

  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    if len(legalActions) == 0:
      return []
    scores = [(-1*distanceToClosestMouse(state.generateSuccessor(self.agentIndex, action)), action) \
        for action in legalActions]
        
    bestScore = max(scores)[0]
    bestChoices = [action for score, action in scores if score == bestScore]
    return random.choice(bestChoices)

class ExpectimaxAgent(MultiAgentSearchAgent):

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All agents should be modeled as choosing uniformly at random from their
      legal moves.
    """
    

    n = gameState.getNumAgents()         
    def recurse(state, index, depth):         
        # end state
        if state.lost() or state.won():
            return (state.getScore(), None)
            
        #returns (minimax value of state, optimal action)    
        if depth == 0:
            return (self.evaluationFunction(state), None)
            
        # Player(s) = Agent
        if (index == 0):
            choices = [(recurse(state.generateSuccessor(index, action), index+1, depth)[0], action) \
                for action in state.getLegalActions(index)] 
            
            if len(choices) == 0: return (0,[])
            else: return max(choices)
            
        legalActions = state.getLegalActions(index)
        uniformProbability = 1.0 / len(legalActions)
            
        # Player(s) = Non-last ghost
        if (index > 0 and index < n-1):
            total = 0
            for action in legalActions: 
                total += recurse(state.generateSuccessor(index, action), index+1, depth)[0]
                
            return (total * uniformProbability, action)
                
        # Player(s) = last ghost 
        if index == n-1:
            total = 0
            for action in legalActions: 
                total += recurse(state.generateSuccessor(index, action), 0, depth-1)[0]

            return (total * uniformProbability, action)
    
    expectimax, action = recurse(gameState, self.index, self.depth)
    return action

class MinimaxAgent(MultiAgentSearchAgent):
    
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

    """
    
    def allChoicesSame(list):
        # Returns boolean indicating whether all elements in the list are the same 
        return len(set(list)) <= 1
    
    n = gameState.getNumAgents()         
    def recurse(state, index, depth): 
        # end state
        if state.won() or state.lost():
            return (state.getScore(), None)
            
        #returns (minimax value of state, optimal action)    
        if depth == 0:
            return (self.evaluationFunction(state), None)
            
        # Player(s) = Snake
        if (index == 0):
            choices = [(recurse(state.generateSuccessor(index, action), index+1, depth)[0], action) \
                for action in state.getLegalActions(index)] 
            
            # posValues = [choice[0] for choice in choices]
            # if allChoicesSame(posValues):
            #     return random.choice(choices)
            # else: 
            if len(choices) == 0: return (0,[])
            return max(choices)
            
        # Player(s) = Non-last mice
        if (index > 0 and index < n-1):
            choices = [(recurse(state.generateSuccessor(index, action), index+1, depth)[0], action) \
                for action in state.getLegalActions(index)]                

            return min(choices)

        # Player(s) = last mice 
        if index == n-1:
            choices = [(recurse(state.generateSuccessor(index, action), 0, depth-1)[0], action) \
                for action in state.getLegalActions(index)]

            return min(choices)
    
    minimax, action = recurse(gameState, self.index, self.depth)
    return action
    
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (our solution is 49 lines of code, but don't worry if you deviate from this)
    def allChoicesSame(list):
        # Returns boolean indicating whether all elements in the list are the same 
        return len(set(list)) <= 1
    
    n = gameState.getNumAgents()    
    def recurse(state, index, depth, alpha, beta): 
        #returns (minimax value of state, optimal action)    
                
        # end state
        if state.won() or state.lost():
            return (state.getScore(), None) 
        
        if depth == 0:
            return (self.evaluationFunction(state), None)

        # Player(s) = Agent
        if (index == 0):
            choices = []
            for action in state.getLegalActions(index): 
                value = recurse(state.generateSuccessor(index, action), index+1, depth, alpha, beta)[0]
                # reset lower bound
                alpha = max(alpha, value)

                choices.append((value, action))
                
            if len(choices) == 0: return (0,[])
            else: return max(choices)
            
        # Player(s) = Non-last ghost
        if (index > 0 and index < n-1):
            choices = []
            for action in state.getLegalActions(index): 
                value = recurse(state.generateSuccessor(index, action), index+1, depth, alpha, beta)[0]
                
                # reset upper bound
                beta = min(beta, value)
                
                # not overlapping 
                if not (beta > alpha):
                    return (beta, action) 
                    
                choices.append((value, action))

            return min(choices)
        
        # Player(s) = last ghost 
        if index == n-1:
            choices = []
            for action in state.getLegalActions(index): 
                value = recurse(state.generateSuccessor(index, action), 0, depth-1, alpha, beta)[0]
                
                # reset upper bound
                beta = min(beta, value)
                
                # not overlapping 
                if not (beta > alpha):
                    return (beta, action) 
                    
                choices.append((value, action))

            return min(choices)
    
    alpha = -float("inf")
    beta = float("inf")     
    minimax, action = recurse(gameState, self.index, self.depth, alpha, beta)
    # print minimax, action
    return action

class MouseAgent(Agent):
    def __init__( self, index ):
        self.agentIndex = index
        
    def getAction( self, state ):
        pass

class RandomMouse(MouseAgent):
  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    return random.choice(legalActions)
    
class ScaredMouse(MouseAgent):
    def getAction(self, state):
        legalActions = state.getLegalActions(self.agentIndex)
        
        pos = state.getMicePositions(self.agentIndex)
        snakeHead = state.snakePositions[0]
        
        # Select best actions given the state
        distancesToSnake = [manhattanDistance( action, snakeHead ) for action in legalActions]
        bestScore = max( distancesToSnake )
        bestActions = [action for action, distance in zip( legalActions, distancesToSnake ) if distance == bestScore]
        
        return random.choice(bestActions)
