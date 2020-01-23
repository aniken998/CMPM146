from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    heapQ = []
    closeList = {}
    heappush(heapQ, (0, initial_position, None))
    while len(heapQ) > 0:
        currentNode = heappop(heapQ)
        closeList[currentNode[1]] = (currentNode[2], currentNode[0])
        if(currentNode[1] == destination):
            path = []
            path.append(destination)
            thisNode = closeList[destination]
            while thisNode[0] != None:
                path.append(thisNode[0])
                thisNode = closeList[thisNode[0]]
            return path
        else:
            for (position, cost) in adj(graph, currentNode[1]):
                if position not in closeList:
                    nodeExist = False
                    for node in heapQ:
                        if(position == node[1]):
                            nodeExist = True
                            if(currentNode[0] + cost) < node[0]:
                                heapQ.remove(node)
                                heappush(heapQ, (currentNode[0] + cost, position, currentNode[1]))
                    if(not nodeExist):
                        heappush(heapQ, (cost + currentNode[0], position, currentNode[1]))
    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    all=graph["spaces"].items()

    result={}
    for (dest,unused) in all:
        path = dijkstras_shortest_path(initial_position, dest, graph, adj)
        i=0
        cost=0
        if path!=None:
            if len(path)==1:
                result[dest]=0
            while (i<len(path)-1):
                cost+=distance(path[i],path[i+1],graph)
                i=i+1
            result[dest]=cost
    return result
    pass
    
def distance(pos1,pos2,level):
    adjcell=navigation_edges(level, pos1)
    for cell in adjcell:
        if pos2==cell[0]:
            return cell[1]
    return null




def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    result = []
    x = cell[0]
    y = cell[1]
    rt2=2**0.5/2
    all = {(x - 1, y - 1, rt2), (x - 1, y, 0.5), (x - 1, y + 1, rt2), (x, y - 1, 0.5), (x, y + 1, 0.5), (x + 1, y - 1, rt2), (x + 1, y, 0.5),
           (x + 1, y + 1, rt2)}
    for (a, b, p) in all:
        if a >= 0 and b >= 0 and (not (a, b) in level['walls']) and (a,b) in level['spaces'] and (not (x, y) in level['walls']):
            cost=(level['spaces'][(a,b)]+level['spaces'][(x,y)])*p
            result.append(((a,b),cost))
    return result
    pass


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    
    costs = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    if(path != None):
        print("total cost = ", costs[dst], "\n")
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')



