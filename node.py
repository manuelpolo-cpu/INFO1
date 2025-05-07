import math

class Node:
    def __init__ (node, name, coordinate_x, coordinate_y):
        node.name = str(name)
        node.coordinate_x = float(coordinate_x)
        node.coordinate_y = float(coordinate_y)
        node.neighbors = []

def AddNeighbor(n1,n2):
    i = 0
    while i < len(n1.neighbors):
        if n2.name == n1.neighbors[i].name:
            return False
        i += 1
    n1.neighbors.append(n2)
    return True

def Distance(n1,n2):
    vector = [(n2.coordinate_x-n1.coordinate_x),(n2.coordinate_y-n1.coordinate_y)]
    return math.sqrt(vector[0]**2+vector[1]**2)