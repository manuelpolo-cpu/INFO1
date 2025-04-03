from segment import Segment
from node import Node
import math
import matplotlib.pyplot as plt
class Graph:
    def __init__(graph):
        graph.nodes = []
        graph.segments = []

def AddNode(graph, n):
    i = 0
    while i < len(graph.nodes):
        if graph.nodes[i].name == n.name:
            return False
        i += 1
    graph.nodes.append(n)
    return True

def AddSegment(graph, name, nameOriginNode, nameDestinationNode):
    i = 0
    encontrados = 0
    origin_node = None
    destination_node = None
    while i < len(graph.nodes) and encontrados != 2:
        if nameOriginNode == graph.nodes[i].name:
            origin_node = graph.nodes[i]
            encontrados += 1
        elif nameDestinationNode == graph.nodes[i].name:
            destination_node = graph.nodes[i]
            encontrados += 1
        i += 1
    if encontrados != 2:
        return False
    new_segment = Segment(name=name, origin=origin_node, destination=destination_node)
    graph.segments.append(new_segment)
    origin_node.neighbors.append(destination_node)
    return True

def GetClosest(Graph, x, y):
    if len(Graph.nodes) == 0:  # Se usa Graph con mayúscula, que es el nombre de la clase
        return None
    closest_node = None
    min_distance = float('inf')
    for node in Graph.nodes:
        distance = ((node.coordinate_x - x) ** 2 + (node.coordinate_y - y) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    return closest_node

def Plot(g):
    plt.figure(figsize=(8, 6))
    i = 0
    while i < len(g.segments):  # Usa g en lugar de graph
        segment = g.segments[i]
        x = [segment.origin.coordinate_x, segment.destination.coordinate_x]
        y = [segment.origin.coordinate_y, segment.destination.coordinate_y]  # Corrige el valor de y
        plt.plot(x, y, 'bo-', linewidth=2)
        mid_x = (segment.origin.coordinate_x + segment.destination.coordinate_x) / 2
        mid_y = (segment.origin.coordinate_y + segment.destination.coordinate_y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}", color="red", fontsize=12, ha="center")
        i += 1
    j = 0
    while j < len(g.nodes):  # Usa g en lugar de graph
        node = g.nodes[j]  # Corrige el acceso a los nodos
        plt.scatter(node.coordinate_x, node.coordinate_y, color="red", s=100)
        plt.text(node.coordinate_x, node.coordinate_y, node.name, fontsize=12, ha="right", color="black")
        j += 1
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Graph Representation")  # Corrige el error tipográfico
    plt.grid(True)
    plt.show()


def PlotNode(graph, nameOrigin):
    origin_node = None
    i = 0
    while i < len(graph.nodes):
        if graph.nodes[i].name == nameOrigin:
            origin_node = graph.nodes[i]
            break
        i += 1
    if origin_node is None:
        return False
    plt.figure(figsize=(8, 6))
    j = 0
    while j < len(graph.segments):
        segment = graph.segments[j]
        x = [segment.origin.coordinate_x, segment.destination.coordinate_x]
        y = [segment.origin.coordinate_y, segment.destination.coordinate_y]
        if segment.origin == origin_node or segment.destination == origin_node:
            plt.plot(x, y, 'r-', linewidth=2)
            mid_x = (segment.origin.coordinate_x + segment.destination.coordinate_x) / 2
            mid_y = (segment.origin.coordinate_y + segment.destination.coordinate_y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.2f}", color="red", fontsize=12, ha="center")
        else:
            plt.plot(x, y, 'black', linewidth=1, linestyle="dotted")
        j += 1
    k = 0
    while k < len(graph.nodes):
        node = graph.nodes[k]
        color = "blue"
        if node == origin_node:
            color = "gray"
        else:
            is_neighbor = False
            for segment in graph.segments:
                if (segment.origin == origin_node and segment.destination == node) or \
                        (segment.destination == origin_node and segment.origin == node):
                    is_neighbor = True
                    break
            if is_neighbor:
                color = "black"
        plt.scatter(node.coordinate_x, node.coordinate_y, color=color, s=100)
        plt.text(node.coordinate_x, node.coordinate_y, node.name, fontsize=12, ha="right", color="black")
        k += 1
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Graph Representation - Highlighting {nameOrigin}")
    plt.grid(True)
    plt.show()
    return True