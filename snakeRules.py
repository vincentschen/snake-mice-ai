import mouseRules #TODO


"""
Handles state changes for snake agent
"""
IS_ORACLE = False

# MOUSE_REWARD = 10
MOVE_PENALTY = 1

MICE_TO_WIN = 200
MOUSE_REWARD_MULTIPLIER = 1



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
    if location[0] >= state.dimensions[0] or location[0] < 0 or location[1] >= state.dimensions[1] or location[1] < 0:
      return False
    if not IS_ORACLE:
      for loc in state.getSnakePositions():
        if loc == location:
          return False
    return True

def applyAction(state, action):
    newLoc = (state.getSnakePositions()[0][0] + action[0], state.getSnakePositions()[0][1] + action[1])
    # itself or a wall, game over
    if not isValidLocation(state, newLoc):
      state.isLose = True
    # new tile has a mouse
    elif newLoc in state.getMicePositions():
      eatenMouseIndex = state.getMicePositions().index(newLoc)
      state.micePositions[eatenMouseIndex] = mouseRules.randomLocation(state)
      state.snakePositions.insert(0, newLoc)
      state.miceEaten += 1
      state.score += state.miceEaten * MOUSE_REWARD_MULTIPLIER
      if state.miceEaten >= MICE_TO_WIN:
        state.isWin = True
    # current tile has a mouse, wowowow!
    elif state.getSnakePositions()[0] in state.getMicePositions():
      eatenMouseIndex = state.getMicePositions().index(state.getSnakePositions()[0])
      state.micePositions[eatenMouseIndex] = mouseRules.randomLocation(state)
      state.score += state.miceEaten * MOUSE_REWARD_MULTIPLIER
      state.miceEaten += 1
      if state.miceEaten >= MICE_TO_WIN:
        state.isWin = True
      state.snakePositions.insert(0, newLoc)
    #new tile is empty
    else:   
      state.snakePositions.insert(0, newLoc)
      state.snakePositions.pop()
      state.score -= MOVE_PENALTY 


