import random

"""
Handles state changes for mice agents
"""

MOVE_PENALTY = 1
MOUSE_REWARD = 20
MICE_TO_WIN = 50

def getLegalActions(state, agentIndex):
    possible_results = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    results = []
    agentPos = state.getMicePositions()[agentIndex-1]
    for move in possible_results:
      if isValidLocation(state, (agentPos[0] + move[0], agentPos[1] + move[1])):
        results.append(move)
    return results

def applyAction(state, action, agentIndex):
    
    previousMouseLocation = state.micePositions[agentIndex-1]
    previousMouseX = previousMouseLocation[0]
    previousMouseY = previousMouseLocation[1]
    
    newLoc = (previousMouseX + action[0], previousMouseY + action[1])
    state.micePositions[agentIndex-1] = newLoc

#valid location is any square in the grid without a mouse or snake tile
def isValidLocation(state, location):
    if location[0] >= state.dimensions[0] or location[1] >= state.dimensions[1]:
      return False
    for loc in state.getSnakePositions() + state.getMicePositions():
      if loc == location:
        return False
    return True

#returns a random location on the board not taken up by snake or mice
def randomLocation(state):
    while True:
      possible = (random.randint(0, state.dimensions[0] - 1), random.randint(0, state.dimensions[1] - 1))
      if isValidLocation(state, possible):
        return possible