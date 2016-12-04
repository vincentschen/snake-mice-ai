from shapely import geometry
from collections import defaultdict
from collections import deque
import heapq

def getSnakeCornersHashedByX(snakePositions):
    """
    This function returns a dictionary mapping x-coordinate values to 
    lists of corner coordinates (snake positions) in a heapq configuration
    for which this value is the x-coordinate
    """
    xHashed = defaultdict(list)
    heapq.heappush(xHashed[snakePositions[0][0]], snakePositions[0]) 
    heapq.heappush(xHashed[snakePositions[-1][0]], snakePositions[-1]) 
    for i in range(len(snakePositions)):
        snakeX1, snakeY1 = snakePositions[i]
        try:
            snakeX2, snakeY2 = snakePositions[i + 2]
            xDiff = snakeX1 - snakeX2
            yDiff = snakeY1 - snakeY2
            if (xDiff == 1 or xDiff == -1) and (yDiff == 1 or yDiff == -1):
                corner = snakePositions[i + 1]
                heapq.heappush(xHashed[corner[0]], corner)
        except IndexError:
            pass
    return xHashed

def getSnakePolygon(snakePositions):
    """
    This function returns a polygon as defined in the shapely library
    composed of the points defining the perimeter of the snake for the
    x and y coorindate value ranges that it occupies
    """
    # dict of x values to lists of positions with that x value
    # sorted by increasing y value
    snakePositionsByRow = defaultdict(list)
    for snakeRow, snakeCol in snakePositions:
        heapq.heappush(snakePositionsByRow[snakeRow], (snakeRow, snakeCol)) 
    sortedRows = sorted(snakePositionsByRow)
    topPositions = snakePositionsByRow[sortedRows[0]]
    rightPositions = []
    bottomPositions = snakePositionsByRow[sortedRows[-1]]
    leftPositions = deque()
    # fill topPositions and bottomPositions in one pass, L to R
    for row in sortedRows[1:-1]:
        positionsGivenRow = snakePositionsByRow[row]
        rightPositions.append(heapq.nlargest(1, positionsGivenRow)[0])
        # no double counting
        if len(positionsGivenRow) > 1:
            leftPositions.appendleft(heapq.nsmallest(1, positionsGivenRow)[0])
    bottomPositions.reverse()
    perimeterPositions = topPositions + rightPositions + bottomPositions
    perimeterPositions.extend(leftPositions)
    print perimeterPositions
    return geometry.Polygon([[p[0], p[1]] for p in perimeterPositions])

def isAValidLocation(pos, snakePositions, dimensions):
    """
    A helper function for the updateAcceisblePoints() recurrence, returns
    whether a position exists on the board and is not occupied by the
    snake
    """
    return pos[0] >= 0 and pos[0] < dimensions[0] and \
           pos[1] >= 0 and pos[1] < dimensions[1] and \
           pos not in snakePositions

def updateAccessiblePoints(start, accessiblePositions, snakePositions, dimensions):
    """
    A recursive search which updates the set accessiblePoints with all
    positions accessible form the start position, given the current snake
    potisions and the dimensions
    """
    startRow, startCol = start
    nextPositions = [(startRow, startCol + 1), (startRow, startCol - 1), (startRow + 1, startCol), (startRow - 1, startCol)]
    for nextPos in nextPositions:
        if isAValidLocation(nextPos, snakePositions, dimensions) and nextPos not in accessiblePositions:
            print nextPos
            accessiblePositions.add(nextPos)
            updateAccessiblePoints(nextPos, accessiblePositions, snakePositions, dimensions)

def getAreaBlockedBySnake(snakeList, dimensions):
    """
    This functions returns the 
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
        updateAccessiblePoints(edge, accessiblePositions, snakePositions, dimensions)
    return rows * cols - len(accessiblePositions)

# testing input
# snakePositions = [(5,0), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (5,1), (6,1), (7,1)]
