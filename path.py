from node import *
import matplotlib.pyplot as plt
from segment import *

class Path:
    def __init__(path, origen, destination):
        path.nodes = []
        path.total_cost = 0.0
        path.origen = origen
        path.destination = destination


def AddNodeToPath(P, n):
    for node in P.nodes:
        if n.name == node.name:
            return False
    P.nodes.append(n)
    return True


def CostToNode(P, n):
    coste = 0.0
    i = 0
    while i < len(P.nodes)-1:
        actual = P.nodes[i]
        siguiente = P.nodes[i+1]
        coste += Distance(actual, siguiente)
        if siguiente.name == n.name:
            return coste
        i += 1
    return -1


def ContainsNode(p, n):
    i = 0
    while i < len(p.nodes):
        if p.nodes[i].name == n.name:
            return True
        i += 1
    return False


def PlotPath(G, P):
    total_cost = 0
    camino_parcial = Path(P.origen, P.destination)
    AddNodeToPath(camino_parcial, P.nodes[0])  # Añadir solo el primer nodo una vez
    flechas_hechas = []       # [(origen, destino)]
    costes_hechos = []        # [(x_medio, y_medio, coste)]

    for i in range(len(P.nodes) - 1):
        plt.figure(figsize=(10, 8))

        for node in G.nodes:
            plt.scatter(node.coordinate_x, node.coordinate_y, color='lightgrey', s=100)
            plt.text(node.coordinate_x + 0.5, node.coordinate_y + 0.5, node.name,
                     fontsize=10, color='gray', fontweight='bold')

        current_node = P.nodes[i]
        next_node = P.nodes[i + 1]
        AddNodeToPath(camino_parcial, next_node)

        for neighbor in current_node.neighbors:
            plt.annotate("",
                         xy=(neighbor.coordinate_x, neighbor.coordinate_y),
                         xytext=(current_node.coordinate_x, current_node.coordinate_y),
                         arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))

        for (origen, destino) in flechas_hechas:
            plt.annotate("",
                         xy=(destino.coordinate_x, destino.coordinate_y),
                         xytext=(origen.coordinate_x, origen.coordinate_y),
                         arrowprops=dict(facecolor="skyblue", edgecolor="skyblue", arrowstyle="->", lw=2))

        for (x, y, c) in costes_hechos:
            plt.text(x, y, f"{c:.2f}", color="black", fontsize=9, fontweight='bold', va='center', ha='center')
        plt.annotate("",
                     xy=(next_node.coordinate_x, next_node.coordinate_y),
                     xytext=(current_node.coordinate_x, current_node.coordinate_y),
                     arrowprops=dict(facecolor="skyblue", edgecolor="skyblue", arrowstyle="->", lw=2))
        coste = Distance(current_node, next_node)
        total_cost += coste
        mid_x = (current_node.coordinate_x + next_node.coordinate_x)/2
        mid_y = (current_node.coordinate_y + next_node.coordinate_y)/2
        costes_hechos.append((mid_x, mid_y, coste))
        flechas_hechas.append((current_node, next_node))

        for node in camino_parcial.nodes:
            plt.scatter(node.coordinate_x, node.coordinate_y, color='grey', s=120)
            plt.text(node.coordinate_x + 0.5, node.coordinate_y + 0.5, node.name,
                     fontsize=10, color='lightgreen', fontweight='bold')

        plt.title(f"Paso {i + 1}: desde {current_node.name} → {next_node.name} | Coste acumulado: {total_cost:.2f}")
        plt.xticks(range(-5, 26, 5))
        plt.yticks(range(-5, 26, 5))
        plt.grid(color='lightpink')
        plt.show()

    plt.figure(figsize=(10, 8))

    for node in G.nodes:
        plt.scatter(node.coordinate_x, node.coordinate_y, color='lightgrey', s=100)
        plt.text(node.coordinate_x + 0.5, node.coordinate_y + 0.5, node.name,
                 fontsize=10, color='gray', fontweight='bold')

    for (origen, destino) in flechas_hechas:
        plt.annotate("",
                     xy=(destino.coordinate_x, destino.coordinate_y),
                     xytext=(origen.coordinate_x, origen.coordinate_y),
                     arrowprops=dict(facecolor="skyblue", edgecolor="skyblue", arrowstyle="->", lw=2))

    for (x, y, c) in costes_hechos:
        plt.text(x, y, f"{c:.2f}", color="black", fontsize=10, fontweight='bold')

    for node in camino_parcial.nodes:
        plt.scatter(node.coordinate_x, node.coordinate_y, color='grey', s=120)
        plt.text(node.coordinate_x + 0.5, node.coordinate_y + 0.5, node.name,
                 fontsize=10, color='lightgreen', fontweight='bold')

    plt.title(f"Camino completo de {P.origen.name} → {P.destination.name} | Coste total: {total_cost:.2f}")
    plt.xticks(range(-5, 26, 5))
    plt.yticks(range(-5, 26, 5))
    plt.grid(color='lightpink')
    plt.show()


def Reachability(g, n1, n2, visited=None):
    if visited is None:
        visited = set()  # Iniciar el conjunto de nodos visitados
    visited.add(n1)
    if n1 == n2:
        return True
    for neighbor in n1.neighbors:
        if neighbor not in visited:  # Si el vecino no ha sido visitado
            # Llamar recursivamente con el vecino
            if Reachability(g, neighbor, n2, visited):
                return True
    return False


def FindShortestPath(G, origen, destino):
    initial_path = Path(origen, destino)
    AddNodeToPath(initial_path, origen)
    current_paths = [initial_path]

    while current_paths:
        current_paths.sort(key=lambda path: path.total_cost + Distance(path.nodes[-1], destino))
        current_path = current_paths.pop(0)
        if current_path.nodes[-1] == destino:
            return current_path
        last_node = current_path.nodes[-1]

        for neighbor in last_node.neighbors:
            if ContainsNode(current_path, neighbor):
                continue
            new_path = Path(current_path.origen, current_path.destination)

            for node in current_path.nodes:
                AddNodeToPath(new_path, node)
            AddNodeToPath(new_path, neighbor)
            new_path.total_cost = current_path.total_cost + Distance(last_node, neighbor)
            current_paths.append(new_path)
    return None