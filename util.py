def getStraightLength(self, state, action):
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