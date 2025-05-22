#importar las librerías numéricas y graficas
import matplotlib.pyplot as plt
import numpy as np
import math
#importar todas las clases y funciones necesarias
from node import *
from segment import *


#clase grafo
class Graph:
    def __init__(graph):
        graph.nodes = []
        graph.segments = []


#función para añadir nodos
def AddNode(g, n):
    i = 0
    while i < len(g.nodes):
        if n.name == g.nodes[i].name:
            return False
        i += 1
    g.nodes.append(n)
    return True


#función para añadir segmentos
def AddSegment(g, name, nameOriginNode, nameDestinationNode):
    encontrados = 0
    node_origin = None
    node_destination = None
    for node in g.nodes:
        if node.name == nameOriginNode:
            node_origin = node
            encontrados += 1
        elif node.name == nameDestinationNode:
            node_destination = node
            encontrados += 1
    if encontrados == 2:
        cost = Distance(node_origin,node_destination)
        segment = Segment(name = name,origin = node_origin, destination = node_destination, cost = cost)
        g.segments.append(segment)
        node_origin.neighbors.append(node_destination)
        node_destination.neighbors.append(node_origin)
        return True
    else:
        return False


#función para encontrar el nodo mas cercano a un punto
def GetClosest(g, x, y):
    closest = None
    min_distance = 1000000
    for node in g.nodes:
        coordx = node.coordinate_x - x
        coordy = node.coordinate_y - y
        distance = math.sqrt(coordx**2+coordy**2)
        if distance < min_distance:
            min_distance = distance
            closest = node
    return closest


#función para plotear un grafo
def Plot(g, figsize, xticks, yticks):
    plt.figure(figsize=figsize)
    x_nodes = []
    y_nodes = []
    for node in g.nodes:
        x_nodes.append(node.coordinate_x)
        y_nodes.append(node.coordinate_y)
        plt.text(node.coordinate_x,node.coordinate_y,node.name, fontsize=10, color = 'lightgreen',fontweight = 'bold')
    plt.scatter(x_nodes,y_nodes, color = 'lightgrey',s = 100)

    for segment in g.segments:
        origen_x = segment.origin.coordinate_x
        origen_y = segment.origin.coordinate_y
        destino_x = segment.destination.coordinate_x
        destino_y = segment.destination.coordinate_y
        segment.cost
        plt.annotate("", xy=(destino_x, destino_y), xytext=(origen_x, origen_y),
                     arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))
        mid_x = (origen_x + destino_x) / 2
        mid_y = (origen_y + destino_y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}", color="black", fontsize=10, fontweight = 'bold', ha= 'center', va = 'center')
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.grid(color = 'lightpink')


#función para plotear los vecinos de un nodo
def PlotNode(g, nameOrigin, figsize, xticks, yticks):
    plt.figure(figsize=figsize)
    node_origin = None
    encontrado = False
    for node in g.nodes:
        if node.name == nameOrigin:
            node_origin = node
            encontrado = True
            plt.text(node.coordinate_x, node.coordinate_y, node.name, fontsize=10, color='lightgreen',fontweight = 'bold')
            plt.scatter(node.coordinate_x,node.coordinate_y, color = 'grey', s = 100)
    if not encontrado:
        return False
    x_nodes = []
    y_nodes = []
    for node in g.nodes:
        if node.name != nameOrigin:
            x_nodes.append(node.coordinate_x)
            y_nodes.append(node.coordinate_y)
            plt.text(node.coordinate_x,node.coordinate_y,node.name, fontsize=10, color = 'lightgreen',fontweight = 'bold')
    plt.scatter(x_nodes,y_nodes, color = 'lightgrey', s = 100)

    def get_segment_cost(g, node_a, node_b):
        for segment in g.segments:
            if (segment.origin == node_a and segment.destination == node_b) or \
               (segment.origin == node_b and segment.destination == node_a):
                return segment.cost
        return None

    for node in node_origin.neighbors:
        origen_x = node_origin.coordinate_x
        origen_y = node_origin.coordinate_y
        destino_x = node.coordinate_x
        destino_y = node.coordinate_y
        coste = get_segment_cost(g, node_origin, node)
        plt.annotate("", xy=(destino_x, destino_y), xytext=(origen_x, origen_y),
                     arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))
        mid_x = (origen_x + destino_x) / 2
        mid_y = (origen_y + destino_y) / 2
        plt.text(mid_x, mid_y, f"{coste:.2f}", color="black", fontsize=10, fontweight='bold', ha= 'center', va = 'center')

    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.grid(color = 'lightpink')


#función para plotear un grafo que viene de un archivo
def FromFile(filename, grafo_existente=None):
    FF = Graph()
    with open(filename, 'r') as F:
        linea = F.readline()
        while linea.strip() != "":
            elementos = linea.strip().split()
            if len(elementos) >= 3:
                name = elementos[0]
                x_coord = float(elementos[1])
                y_coord = float(elementos[2])
                n = Node(name, x_coord, y_coord)
                AddNode(FF, n)
            linea = F.readline()
    with open(filename, 'r') as F:
        for linea in F:
            if linea.strip() == "":
                break
        for linea in F:
            elementos = linea.strip().split()
            if len(elementos) >= 6:
                name_segment = f"{elementos[0]}-{elementos[3]}"
                name_origin = elementos[0]
                name_dest = elementos[3]
                AddSegment(FF, name_segment, name_origin, name_dest)
    return FF


#función para eliminar un nodo de un grafo
def DeleteNode(g, node_name):
    # Buscar el nodo a eliminar en la lista de nodos
    node_to_remove = None
    for node in g.nodes:
        if node.name == node_name:
            node_to_remove = node
            break
    # Si no se encuentra el nodo, retornar False (indicando que no se eliminó nada)
    if not node_to_remove:
        print(f"No se encontró el nodo {node_name}.")
        return False
    # Eliminar todos los segmentos que tengan como origen o destino este nodo
    g.segments = [seg for seg in g.segments if seg.origin != node_to_remove and seg.destination != node_to_remove]
    g.nodes.remove(node_to_remove)
    print(f"El nodo {node_name} y sus segmentos han sido eliminados.")
    return True


#función para llevar un grafo a un archivo
def ToFile(grafo, filename):
    with open(filename, 'w') as f:
        for node in grafo.nodes:
            f.write(f"{node.name} {int(node.coordinate_x)} {int(node.coordinate_y)}\n")
        f.write("\n")
        for segment in grafo.segments:
            o = segment.origin
            d = segment.destination
            f.write(f"{o.name} {int(o.coordinate_x)} {int(o.coordinate_y)} {d.name} {int(d.coordinate_x)} {int(d.coordinate_y)}\n")