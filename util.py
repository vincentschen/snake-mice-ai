from shapely import geometry
from collections import defaultdict
from collections import deque
import heapq

def getStraightLength(state, action):
  #CASE 1: Snake of length 1
  if len(state.snakePositions) == 1: #here any action will result in a straight length of 2
    return 2
  #CASE 2: Snake of length 2
  currentDirection = (state.snakePositions[0][0]-state.snakePositions[1][0], state.snakePositions[0][1]-state.snakePositions[1][1]) #this represents our current direction
  if len(state.snakePositions) == 2: #here the right action will result in a straight length of 2
    if action == currentDirection:
      return 3
    else:
      return 2
  #CASE 3: Snake of length 3 or more
  #you picked the wrong direction, so we get two, the minimum
  if(action != currentDirection):
    return 2
  #you picked the right action, so we can keep this straight line going
  else:
    currStraight = 2
    head = state.snakePositions[0]
    while currStraight < len(state.snakePositions) and state.snakePositions[currStraight] == (head[0] - currStraight*currentDirection[0], head[1] - currStraight*currentDirection[1]):
      currStraight += 1
    return currStraight + 1 #plus one for our direction being correct

def manhattanDistance( xy1, xy2 ):
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )  

# k-norm TODO: not working
def centroid(points):
    x_sum = 0.0
    y_sum = 0.0
    for x_i, y_i in points:
        x_sum += x_i
        y_sum += y_i
    return (x_sum, y_sum)

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[0] - p2[1]) ** 2) ** 0.5

def k_heuristic(head, points):
    """
    Let Head be the point represented by $head
    Let N be the number of points in $points
    Let C be the set C[1], C[1,2], C[1,2,3], ..., C[1,2,3,...,N] where C_i is the centroid composed of the ith closest points to Head
    Returns the Nth root of the summation of distances from Head to all C_i raised to the ith power 
    """
    # TODO: MAKE THIS BROKEN HEURISTIC WORK
    centroids = [centroid(points[i:]) for i in range(len(points))]
    distances_to_centroids = sorted([distance(head, point) for point in centroids])
    summation = sum([distances_to_centroids[len(points) - 1 - i] ** (i + 1) for i in range(len(points) - 1, -1, -1)])
    norm = summation ** (1.0 / len(points))
    return norm

def k_norm(head, points):
    """
    Let N be the number of points in $points
    Returns the K-Norm of distances from head to points where the greatest distance is raised to the Nth power
    """
    distances_to_points = sorted([distance(head, point) for point in points])
    summation = sum([distances_to_points[i] ** (i + 1) for i in range(len(points))]) 
    norm = summation ** (1.0 / len(points))
    return norm 

# TODO: Use this function for some heuristic?
def getSnakeCornersHashedByRow(snakePositions):
    """
    This function returns a dictionary mapping row values to 
    lists of corner coordinates (snake positions) in a heapq configuration
    for which this value is the row
    """
    rowHashed = defaultdict(list)
    heapq.heappush(rowHashed[snakePositions[0][0]], snakePositions[0]) 
    heapq.heappush(rowHashed[snakePositions[-1][0]], snakePositions[-1]) 
    for i in range(len(snakePositions)):
        snakeX1, snakeY1 = snakePositions[i]
        try:
            snakeX2, snakeY2 = snakePositions[i + 2]
            xDiff = snakeX1 - snakeX2
            yDiff = snakeY1 - snakeY2
            if (xDiff == 1 or xDiff == -1) and (yDiff == 1 or yDiff == -1):
                corner = snakePositions[i + 1]
                heapq.heappush(rowHashed[corner[0]], corner)
        except IndexError:
            pass
    return rowHashed

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