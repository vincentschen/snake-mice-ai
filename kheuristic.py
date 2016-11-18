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