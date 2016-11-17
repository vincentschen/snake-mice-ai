import mouseRules #TODO

"""
Handles state changes for snake agent
"""

def getLegalActions(state):
    possible_results = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    results = []
    agentPos = state.getSnakePositions()[0]
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
      state.micePositions[eatenMouseIndex] = mouseRules.randomLocation(state)
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