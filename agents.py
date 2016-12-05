import random
from snakeAgent import Agent
from util import * 

class MultiAgentSearchAgent(Agent):
  """
  Abstract class that can be extended for agents that use depth for eval fns. 
  """

  def __init__(self, depth = '2'):
    self.index = 0 # Snake is always agent index 0
    self.depth = int(depth)

class GreedyAgent(Agent):

  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    if len(legalActions) == 0:
      return []
    scores = [(distanceToClosestMouse(state.generateSuccessor(self.agentIndex, action)), action) \
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

    # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
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

            return max(choices)
            
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

  
  def evaluationFunction(self, state):
    
    # straight_length_without_turn = getStraightLength(state)
    # straight_length_without_turn = 0
        
    
    weights = {
        'score': (1, state.score),
        'manhattan_distance_to_closest_mouse': (0.2, distanceToClosestMouse(state)) 
        # 'straight_length_without_turn': (1, straight_length_without_turn)
    }
    
    # for key, weight in weights.iteritems(): print key, weight[0], weight[1]
    score = sum([val[0]*val[1] for key, val in weights.iteritems()])
     
    # print score, self.depth
    return score

class RandomMouse(Agent):
  
  def getAction(self, state):
    legalActions = state.getLegalActions(self.agentIndex)
    return random.choice(legalActions)