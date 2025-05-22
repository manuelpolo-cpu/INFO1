#importar las clases y funciones necesarias
from node import *
from segment import *
#importar las librerías numéricas y gráficas
import matplotlib.pyplot as plt


#clase grafo
class Path:
    def __init__(path, origen, destination):
        path.nodes = []
        path.total_cost = 0.0
        path.origen = origen
        path.destination = destination


#añadir un nodo al camino
def AddNodeToPath(P, n):
    for node in P.nodes:
        if n.name == node.name:
            return False
    P.nodes.append(n)
    return True

#calcualr el coste
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

#buscar si el camino contiene un nodo
def ContainsNode(p, n):
    i = 0
    while i < len(p.nodes):
        if p.nodes[i].name == n.name:
            return True
        i += 1
    return False

#plotear el camino
def PlotPath(G, P, figsize, xticks, yticks):
    total_cost = 0
    camino_parcial = Path(P.origen, P.destination)
    AddNodeToPath(camino_parcial, P.nodes[0])  # Añadir solo el primer nodo una vez
    flechas_hechas = []       # [(origen, destino)]
    costes_hechos = []        # [(x_medio, y_medio, coste)]

    # Acumulamos los datos del camino, sin plotear cada paso
    for i in range(len(P.nodes) - 1):
        current_node = P.nodes[i]
        next_node = P.nodes[i + 1]
        AddNodeToPath(camino_parcial, next_node)

        # Buscar el segmento entre los dos nodos
        segmento = next((s for s in G.segments if
                         (s.origin == current_node and s.destination == next_node) or
                         (s.origin == next_node and s.destination == current_node)), None)

        if segmento:
            coste = segmento.cost
        else:
            coste = 0  # Si no se encuentra el segmento, asumimos coste 0

        total_cost += coste
        mid_x = (current_node.coordinate_x + next_node.coordinate_x) / 2
        mid_y = (current_node.coordinate_y + next_node.coordinate_y) / 2
        costes_hechos.append((mid_x, mid_y, coste))
        flechas_hechas.append((current_node, next_node))

    # Ahora plot final solo
    plt.figure(figsize=figsize)

    for node in G.nodes:
        plt.scatter(node.coordinate_x, node.coordinate_y, color='lightgrey', s=100)
        plt.text(node.coordinate_x, node.coordinate_y, node.name,
                 fontsize=10, color='lightgray', fontweight='bold')

    for (origen, destino) in flechas_hechas:
        plt.annotate("",
                     xy=(destino.coordinate_x, destino.coordinate_y),
                     xytext=(origen.coordinate_x, origen.coordinate_y),
                     arrowprops=dict(facecolor="skyblue", edgecolor="skyblue", arrowstyle="->", lw=2))

    for (x, y, c) in costes_hechos:
        plt.text(x, y, f"{c:.2f}", color="black", fontsize=10, fontweight='bold', va='center', ha='center')

    for node in camino_parcial.nodes:
        plt.scatter(node.coordinate_x, node.coordinate_y, color='grey', s=120)
        plt.text(node.coordinate_x, node.coordinate_y, node.name,
                 fontsize=10, color='lightgreen', fontweight='bold')

    plt.title(f"Camino completo de {P.origen.name} → {P.destination.name} | Coste total: {total_cost:.2f}")
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.grid(color='lightpink')

#alcanzabilidad de un nodo sobre otro
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

#encontrar el camino mas corto
def FindShortestPath(grafo, origen, destino):
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