from shapely import geometry
from collections import defaultdict
import heapq

# takes snake positions contained in state variable
def getCornerHash(snakePositions):
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

def getCornerPolygon(snakePositions):
    snakePositionsByX = defaultdict(list)
    for snakePos in snakePositions:
        heapq.heappush(snakePositionsByX[snakePos[0]], snakePos) 
    sortedXIndices = sorted(snakePositionsByX)
    leftToTop = sorted(snakePositionsByX[sortedXIndices[0]])
    rightToBottom = []
    for i in range(1, len(sortedXIndices) - 1):
        positionsGivenX = snakePositionsByX[sortedXIndices[i]]
        leftToTop += heapq.nlargest(1, positionsGivenX)
        if len(positionsGivenX) > 1:
            rightToBottom += heapq.nsmallest(1, positionsGivenX)
    rightToBottom += sorted(snakePositionsByX[sortedXIndices[-1]])
    rightToBottom.reverse()
    return geometry.Polygon([[p[0], p[1]] for p in (leftToTop + rightToBottom)])

snakePositions = [(5,0), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (5,1), (6,1), (7,1)]
print getCornerPolygon(snakePositions).area