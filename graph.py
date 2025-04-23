from segment import Segment
from node import *
import math
import matplotlib.pyplot as plt
from path import *
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


def Plot(graph):
    plt.figure(figsize=(8, 6))
    i = 0
    while i < len(graph.segments):
        segment = graph.segments[i]
        x = [segment.origin.coordinate_x, segment.destination.coordinate_x]
        y = [segment.origin.coordinate_y, segment.destination.coordinate_y]
        mid_x = (segment.origin.coordinate_x + segment.destination.coordinate_x) / 2
        mid_y = (segment.origin.coordinate_y + segment.destination.coordinate_y) / 2
        plt.text(mid_x+0.4, mid_y+0.4, f"{segment.cost:.2f}", color="black", fontsize=12, ha="center")
        plt.annotate("",
                     xy=(segment.destination.coordinate_x, segment.destination.coordinate_y),  # destino
                     xycoords='data',
                     xytext=(segment.origin.coordinate_x, segment.origin.coordinate_y),  # origen
                     textcoords='data',
                     arrowprops=dict(arrowstyle="->", color="lightblue", lw=2))
        i += 1
    j = 0
    while j < len(graph.nodes):
        node = graph.nodes[j]
        plt.scatter(node.coordinate_x, node.coordinate_y, color="red", s=100)
        plt.text(node.coordinate_x + 0.5, node.coordinate_y + 0.5, node.name, fontsize=12, ha="left",va="bottom", color="green")
        j += 1
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Gráfico de nodos y segmentos")
    plt.grid(True)
    plt.show()


def PlotNode(graph, nameOrigin):
    origin_node = Node
    for node in graph.nodes:
        if node.name == nameOrigin:
            origin_node = node
            break
    if not origin_node:
        return False
    plt.figure(figsize=(8, 6))
    # Graficar segmentos que tienen el nodo de origen
    for segment in graph.segments:
        if origin_node in [segment.origin, segment.destination]:
            start, end = (segment.origin, segment.destination) if segment.origin == origin_node else (
            segment.destination, segment.origin)
            plt.annotate("", xy=(end.coordinate_x, end.coordinate_y), xytext=(start.coordinate_x, start.coordinate_y),
                         arrowprops=dict(arrowstyle="->", color="red", lw=2))
            # Mostrar el costo en el centro del segmento
            mid_x = (start.coordinate_x + end.coordinate_x) / 2
            mid_y = (start.coordinate_y + end.coordinate_y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.2f}", color="black", fontsize=12, ha="right")
    # Graficar nodos
    for node in graph.nodes:
        color = "gray" if node == origin_node else "blue"
        plt.scatter(node.coordinate_x, node.coordinate_y, color=color, s=100)
        plt.text(node.coordinate_x+0.5, node.coordinate_y+0.5, node.name, fontsize=12, ha="left",va="bottom", color="black")
    # Configuración de la gráfica
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Gráfico de nodos y segmentos")
    plt.grid(True)
    plt.show()
    return True


def CreateGraph_2():
    G = Graph()  # Crear un objeto Graph vacío
    AddNode(G, Node("X", 2, 3))
    AddNode(G, Node("Y", 6, 7))
    AddNode(G, Node("Z", 10, 3))
    AddNode(G, Node("W", 4, 9))
    # Añadir segmentos
    AddSegment(G, "XY", "X", "Y")
    AddSegment(G, "YZ", "Y", "Z")
    AddSegment(G, "ZW", "Z", "W")
    AddSegment(G, "WX", "W", "X")
    return G  # Asegúrate de que devuelves el grafo correctamente


def graph_from_file(filename):
    g = Graph()  # Asegúrate de que esta línea cree un objeto de tipo Graph
    F = open(filename, 'r')
    linea = F.readline().strip()
    while linea != "":
        if linea.startswith("#") or not linea:  # Ignorar comentarios y líneas vacías
            linea = F.readline().strip()
            continue
        elementos = linea.split()
        if len(elementos) == 3:
            name = elementos[0]
            x = float(elementos[1])
            y = float(elementos[2])
            node = Node(name, x, y)  # Crea el nodo
            AddNode(g, node)  # Añadir el nodo al grafo
        linea = F.readline().strip()
    linea = F.readline().strip()  # Leer la siguiente línea que debe ser de segmentos
    while linea != "":
        if linea.startswith("#") or not linea:  # Ignorar comentarios y líneas vacías
            linea = F.readline().strip()
            continue
        elementos = linea.split()
        if len(elementos) == 2:
            node1_name = elementos[0]
            node2_name = elementos[1]
            AddSegment(g, f"{node1_name}{node2_name}", node1_name, node2_name)  # Añadir segmento
        linea = F.readline().strip()
    F.close()
    return g




def FindShortestPath(G, origin, destination):
    paths = [Path([origin])]

    while paths:
        current = min(paths, key=lambda p: p.total_cost() + distance(p.last_node(), destination))
        paths.remove(current)
        last = current.last_node()

        for neighbor in G.neighbors(last):
            if neighbor == destination:
                final_path = AddNodeToPath(current, neighbor)
                return final_path
            if ContainsNode(current, neighbor):
                continue
            extended = AddNodeToPath(current, neighbor)
            paths.append(extended)
    return None

def ReachableNodes(graph, start_node):
    visited = set()
    to_visit = [start_node]
    while to_visit:
        current = to_visit.pop()
        if current not in visited:
            visited.add(current)
            to_visit.extend([n for n in graph.neighbors(current) if n not in visited])
    return list(visited)