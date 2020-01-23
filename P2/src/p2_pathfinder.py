
from heapq import heappop, heappush
from math import sqrt

def findBox(mesh, currentNode):
    for box in mesh["boxes"]:
        if (box[0] <= currentNode[0] and box[1] >= currentNode[0]) and (box[2] <= currentNode[1] and box[3] >= currentNode[1]):
            return box
    return None

def getPath(start_box, start_point, dest_point, mesh):
    adj_boxs = mesh['adj'][start_box]
    path_lengths = []
    if dest_point[0] <= start_box[1] and dest_point[0] >= start_box[0] and dest_point[1] <= start_box[3] and dest_point[0] >= start_box[2]:
        dest_box = findBox(mesh, dest_point)
        return [(dest_point, dest_box, calcLength(start_point, dest_point), calcLength(start_point, dest_point))]
    for adj_box in adj_boxs:
        # print('adj box as')
        # print(adj_box)
        axis_index_box = 0
        axis_index_point = 0
        if start_box[0] == adj_box[1]:
            axis_index_box = 2
            axis_index_point = 1
            share_edge_axis = 0 # start_box's left edge share 
        elif start_box[1] == adj_box[0]:
            axis_index_box = 2 
            axis_index_point = 1
            share_edge_axis = 1 # start_box's right edge share
        elif start_box[2] == adj_box[3]:
            axis_index_box = 0 
            axis_index_point = 0
            share_edge_axis = 2 # start_box's top edge share
        else:
            axis_index_box = 0 
            axis_index_point = 0
            share_edge_axis = 3 # start_box's bottom edge share
        lower_index, higher_index = compareIndex(start_box, adj_box, axis_index_box)
        if start_point[axis_index_point] >= lower_index and start_point[axis_index_point] <= higher_index:
            if axis_index_point == 1:
                adj_point = (start_box[share_edge_axis], start_point[axis_index_point])
            else:
                adj_point = (start_point[axis_index_point], start_box[share_edge_axis])
        elif start_point[axis_index_point] < lower_index:
            if axis_index_point == 1:
                adj_point = (start_box[share_edge_axis], lower_index)
            else:
                adj_point = (lower_index, start_box[share_edge_axis])
        else:
            if axis_index_point == 1:
                adj_point = (start_box[share_edge_axis], higher_index)
            else:
                adj_point = (higher_index, start_box[share_edge_axis])
        # start_box_mid_point = ((start_box[0] + start_box[1])/2, (start_box[2] + start_box[3])/2)
        # adj_box_mid_point = ((adj_box[0] + adj_box[1])/2, (adj_box[2] + adj_box[3])/2)
        path_lengths.append((adj_point, adj_box, calcLength(start_point, adj_point), calcLength(adj_point, dest_point)))
    return path_lengths

def calcLength(start_point, path_point):
    return sqrt((start_point[0]-path_point[0])**2 + (start_point[1]-path_point[1])**2)

def compareIndex(start_box, adj_box, index):
    # index = 2, x-axis edges of the 2 boxes arew shared;
    # index = 0, y-axis edges arew shared
    if start_box[index] > adj_box[index]: 
        # if start_box is higher than adj_box
        if start_box[index+1] > adj_box[index+1]:
            # if start_box's higher bound is higher than adj_box
            return (start_box[index], adj_box[index+1])
        else:
            return (start_box[index], start_box[index+1])
    else:
        if start_box[index+1] > adj_box[index+1]:
            return (adj_box[index], adj_box[index+1])
        else:
            return (adj_box[index], start_box[index+1])

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """    
    heapQ = []
    closeList = {}
    boxes = {}
    closeBox = {}
    path = []
    start_box = findBox(mesh, source_point)
    dest_box = findBox(mesh, destination_point)
    heappush(heapQ, (calcLength(source_point, destination_point), 0, source_point, None, start_box, None))
    boxes[start_box] = None
    while len(heapQ) > 0:
        currentNode = heappop(heapQ)
        current_box = currentNode[4]
        closeList[current_box] = (currentNode[4], currentNode[5], currentNode[2])# current box and parent box
        closeBox[current_box] = None
        if current_box == dest_box:
            boxes[dest_box] = None
            thisNode = closeList[dest_box]
            path.append((destination_point, currentNode[2]))
            # print("total cost = " , thisNode[1], "\n")
            while thisNode[1]:
                print("this node: ", thisNode)
                boxes[thisNode[0]] = None
                nextNode = closeList[thisNode[1]]
                path.append((thisNode[2], nextNode[2]))
                thisNode = nextNode
            return path, boxes.keys()
        else:
            # print('current boxes')
            # print(currentNode[2])
            # print(current_box)
            # print('adj boxes')
            # print(mesh['adj'][current_box])
            # print('next point')
            path_info = getPath(current_box, currentNode[2], destination_point, mesh)
            # print(getPath(current_box, currentNode[2], destination_point, mesh))
            for (position, next_box, pathCost, estCost) in path_info:
                currentPathCost = pathCost + currentNode[1]
                currentEstCost = estCost + currentPathCost
                if next_box not in closeBox or current_box == dest_box:
                    if position == destination_point:
                        print('dest found')
                    nodeExist = False
                    index = 0
                    for node in heapQ:
                        if next_box == node[5]:
                            nodeExist = True
                            if currentEstCost < node[0]:
                                heapQ.pop(index)
                                # boxes[next_box]
                                heappush(heapQ, (currentEstCost, currentPathCost, position, currentNode[2], next_box, current_box))
                            index += 1
                    if(not nodeExist):
                        # boxes[next_box] = None
                        heappush(heapQ, (currentEstCost, currentPathCost, position, currentNode[2], next_box, current_box))
        # print('queue')
        # print(heapQ)
    return None