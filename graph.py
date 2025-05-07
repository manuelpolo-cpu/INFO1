import math
from node import *
from segment import *
import matplotlib.pyplot as plt

class Graph:
    def __init__(graph):
        graph.nodes = []
        graph.segments = []

def AddNode(g, n):
    i  = 0
    while i < len(g.nodes):
        if n.name == g.nodes[i].name:
            return False
        i += 1
    g.nodes.append(n)
    return True

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

def Plot(g):
    plt.figure(figsize=(10, 8))
    x_nodes = []
    y_nodes = []
    for node in g.nodes:
        x_nodes.append(node.coordinate_x)
        y_nodes.append(node.coordinate_y)
        plt.text(node.coordinate_x+0.5,node.coordinate_y+0.5,node.name, fontsize=10, color = 'lightgreen',fontweight = 'bold')
    plt.scatter(x_nodes,y_nodes, color = 'lightgrey',s = 100)

    for segment in g.segments:
        origen_x = segment.origin.coordinate_x
        origen_y = segment.origin.coordinate_y
        destino_x = segment.destination.coordinate_x
        destino_y = segment.destination.coordinate_y
        coste = segment.cost
        plt.annotate("", xy=(destino_x, destino_y), xytext=(origen_x, origen_y),
                     arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))
        mid_x = (origen_x + destino_x) / 2
        mid_y = (origen_y + destino_y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}", color="black", fontsize=10, fontweight = 'bold')
    plt.xticks(range(-5, 26, 5))
    plt.yticks(range(-5, 26, 5))
    plt.grid(color = 'lightpink')
    plt.show()

def PlotNode(g, nameOrigin):
    plt.figure(figsize=(10, 8))
    node_origin = None
    encontrado = False
    for node in g.nodes:
        if node.name == nameOrigin:
            node_origin = node
            encontrado = True
            plt.text(node.coordinate_x + 0.5, node.coordinate_y + 0.5, node.name, fontsize=10, color='lightgreen',fontweight = 'bold')
            plt.scatter(node.coordinate_x,node.coordinate_y, color = 'grey', s = 100)
    if not encontrado:
        return False
    x_nodes = []
    y_nodes = []
    for node in g.nodes:
        if node.name != nameOrigin:
            x_nodes.append(node.coordinate_x)
            y_nodes.append(node.coordinate_y)
            plt.text(node.coordinate_x+0.5,node.coordinate_y+0.5,node.name, fontsize=10, color = 'lightgreen',fontweight = 'bold')
    plt.scatter(x_nodes,y_nodes, color = 'lightgrey', s = 100)


    for node in node_origin.neighbors:
        origen_x = node_origin.coordinate_x
        origen_y = node_origin.coordinate_y
        destino_x = node.coordinate_x
        destino_y = node.coordinate_y
        coste = Distance(node_origin,node)
        plt.annotate("", xy=(destino_x, destino_y), xytext=(origen_x, origen_y),
                     arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))
        mid_x = (origen_x + destino_x) / 2
        mid_y = (origen_y + destino_y) / 2
        plt.text(mid_x, mid_y, f"{coste:.2f}", color="black", fontsize=10, fontweight='bold')

    plt.xticks(range(-5, 26, 5))
    plt.yticks(range(-5, 26, 5))
    plt.grid(color = 'lightpink')
    plt.show()

def FromFile(filename):
    plt.figure(figsize=(10, 8))
    F = open('datos.txt','r')
    linea = F.readline()
    x = []
    y = []
    names = []
    while linea.strip() != "":
        elementos = linea.split(" ")
        names.append(elementos[0])
        x.append(float(elementos[1]))
        y.append(float(elementos[2]))
        linea = F.readline()
    F.close()
    plt.scatter(x, y, color = 'lightgrey', s = 100)

    F = open('datos.txt','r')
    linea = F.readline()
    while linea.strip() != "":
        linea = F.readline()
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        x1 = float(elementos[1])
        y1 = float(elementos[2])
        x2 = float(elementos[4])
        y2 = float(elementos[5])
        distancia = ((x2-x1)**2+(y2-y1)**2)**0.5
        mid_x = (x1+x2)/2
        mid_y = (y1+y2)/2
        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))
        plt.text(mid_x, mid_y, f"{distancia:.2f}", color="black", fontsize=10, fontweight='bold')
        linea = F.readline()
    F.close()

    i = 0
    while i < len(names):
        plt.text(x[i] + 0.5, y[i] + 0.5, names[i], fontsize=10, color='lightgreen', fontweight='bold')
        i += 1
    plt.xticks(range(-5, 26, 5))
    plt.yticks(range(-5, 26, 5))
    plt.grid(color='lightpink')
    plt.show()

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

    # Eliminar el nodo de la lista de nodos
    g.nodes.remove(node_to_remove)

    print(f"El nodo {node_name} y sus segmentos han sido eliminados.")
    return True


def ToFile(grafo, filename):
    with open(filename, 'w') as f:
        for node in grafo.nodes:
            f.write(f"{node.name} {int(node.coordinate_x)} {int(node.coordinate_y)}\n")
        f.write("\n")
        for segment in grafo.segments:
            o = segment.origin
            d = segment.destination
            f.write(f"{o.name} {int(o.coordinate_x)} {int(o.coordinate_y)} {d.name} {int(d.coordinate_x)} {int(d.coordinate_y)}\n")