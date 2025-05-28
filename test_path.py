from node import *
from path import *
from graph import *
from segment import *


def tester():
    G = Graph()
    A = Node("A", 0, 0)
    B = Node("B", 5, 5)
    C = Node("C", 10, 0)
    D = Node("D", 15, 5)
    E = Node("E", 20, 0)
    F = Node("F", 5, -5)
    G_ = Node("G", 10, -5)
    H = Node("H", 15, -5)
    I = Node("I", 20, -5)
    J = Node("J", 25, 0)
    for node in [A, B, C, D, E, F, G_, H, I, J]:
        AddNode(G, node)
    AddNeighbor(A, B)
    AddNeighbor(A, F)
    AddNeighbor(A, C)
    AddNeighbor(B, C)
    AddNeighbor(C, D)
    AddNeighbor(D, E)
    AddNeighbor(F, G_)
    AddNeighbor(G_, H)
    AddNeighbor(H, I)
    AddNeighbor(I, J)
    AddNeighbor(E, J)
    AddNeighbor(C, G_)
    print("Buscando el camino más corto de A a J...")
    shortest_path = FindShortestPath(G, A, J)
    if shortest_path:
        print("Camino más corto encontrado:", [node.name for node in shortest_path.nodes])
        print("Costo total:", shortest_path.total_cost)
        figsize = (8, 6)
        xticks = range(-5, 26, 5)
        yticks = range(-5, 26, 5)
        PlotPath(G, shortest_path, figsize, xticks, yticks)
        plt.show()
    else:
        print("No se encontró un camino de A a J.")
    print("Buscando el camino más corto de C a I...")
    shortest_path_2 = FindShortestPath(G, C, I)
    if shortest_path_2:
        print("Camino más corto encontrado:", [node.name for node in shortest_path_2.nodes])
        print("Costo total:", shortest_path_2.total_cost)
        figsize = (8, 6)
        xticks = range(-5, 26, 5)
        yticks = range(-5, 26, 5)
        PlotPath(G, shortest_path_2, figsize, xticks, yticks)
        plt.show()
    else:
        print("No se encontró un camino de C a I.")
tester()