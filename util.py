from collections import defaultdict
from collections import deque
import heapq

def addTuples(tuple1, tuple2):
    return (tuple1[0]+tuple2[0], tuple1[1]+tuple2[1])

def distanceToClosestMouse(state):
    distanceToMouse = [manhattanDistance(i, state.snakePositions[0])**(.5) for i in state.micePositions]
    closestIndex = 0
    for i in range(1, len(distanceToMouse)):
        if distanceToMouse[i] < distanceToMouse[closestIndex]:
            closestIndex = i
    return manhattanDistance(state.micePositions[closestIndex], state.snakePositions[0])

def numBlockedAdjacentTiles(state):
    allToCheck = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
    allToCheck = [addTuples(state.snakePositions[0], action) for action in allToCheck]
    allToCheck = [pos for pos in allToCheck if pos in state.snakePositions[2:]]
    return len(allToCheck)


def getStraightLength(state):
    #CASE 1: Snake of length 1, 2
    if len(state.snakePositions) <= 2: #here the straight length so far is just len of snake
        return len(state.snakePositions)
    #CASE 2: Snake of length 3 or more  
    currentDirection = (state.snakePositions[0][0]-state.snakePositions[1][0], state.snakePositions[0][1]-state.snakePositions[1][1]) #this represents our current direction
    currStraight = 2
    head = state.snakePositions[0]
    while currStraight < len(state.snakePositions) and state.snakePositions[currStraight] == (head[0] - currStraight*currentDirection[0], head[1] - currStraight*currentDirection[1]):
        currStraight += 1
    return currStraight

def manhattanDistance( xy1, xy2 ):
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )  

def centroid(points):
    """ 
    Computes the centroid for all the mice on the board. 
    """
    x_sum = 0.0
    y_sum = 0.0
    for x_i, y_i in points:
        x_sum += x_i
        y_sum += y_i
    return (x_sum, y_sum)

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[0] - p2[1]) ** 2) ** 0.5

def getNumSnakeCorners(snakePositions):
    """ 
    Computes the number of 'corners' formed by turns in the Snake. 
    """
    count = 2
    for i in range(len(snakePositions)):
        snakeX1, snakeY1 = snakePositions[i]
        try:
            snakeX2, snakeY2 = snakePositions[i + 2]
            xDiff = snakeX1 - snakeX2
            yDiff = snakeY1 - snakeY2
            if (xDiff == 1 or xDiff == -1) and (yDiff == 1 or yDiff == -1):
                count += 1
        except IndexError:
            pass
    return count

def getSnakeRectangleArea(snakePositions, dimensions):
    """
    This function returns a the rectangle area defined by the row and
    column ranges of the snape positions.
    """
    minRow, minCol = dimensions
    maxRow, maxCol = (0, 0)
    for pos in snakePositions:
        posRow, posCol = pos
        if posRow < minRow:
            minRow = posRow
        if posRow > maxRow:
            maxRow = posRow
        if posCol < minCol:
            minCol = posCol
        if posCol > maxCol:
            maxCol = posCol
    return (maxRow - minRow) * (maxCol - minCol)


def isAValidLocation(pos, snakePositions, dimensions):
    """
    A helper function for the updateAcceisblePoints() recurrence, returns
    whether a position exists on the board and is not occupied by the
    snake
    """
    return pos[0] >= 0 and pos[0] < dimensions[0] and \
           pos[1] >= 0 and pos[1] < dimensions[1] and \
           pos not in snakePositions

def updateAccessiblePositions(start, accessiblePositions, snakePositions, dimensions):
    """
    A recursive search which updates the set accessiblePositions with all
    positions accessible form the start position, given the current snake
    potisions and the dimensions
    """
    startRow, startCol = start
    nextPositions = [(startRow, startCol + 1), (startRow, startCol - 1), (startRow + 1, startCol), (startRow - 1, startCol)]
    for nextPos in nextPositions:
        if isAValidLocation(nextPos, snakePositions, dimensions) and nextPos not in accessiblePositions:
            accessiblePositions.add(nextPos)
            updateAccessiblePositions(nextPos, accessiblePositions, snakePositions, dimensions)

def getAreaBlockedBySnake(snakeList, dimensions):
    """
    This functions returns the sum area currently accessible from
    every edge position on the board, where accessibility is defined 
    such that you can reach one position from another without crossing 
    the snake.

    Depends on updateAccessiblePositions() and isAValidLocation()
    """
    accessiblePositions = set()
    snakePositions = set(snakeList)
    rows, cols = dimensions
    edgePositions = set()
    for col in range(cols):
        edgePositions.add((0, col))
        edgePositions.add((rows, col))
    for row in range(rows):
        edgePositions.add((row, 0))
        edgePositions.add((row, cols))
    for edge in edgePositions:
        if edge in accessiblePositions or edge in snakePositions:
            continue
        updateAccessiblePositions(edge, accessiblePositions, snakePositions, dimensions)
    return rows * cols - len(accessiblePositions)