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

#encontrar el camino mas corto
def FindShortestPath(grafo, origen, destino):
    initial_path = Path(origen, destino)
    AddNodeToPath(initial_path, origen)
    current_paths = [initial_path]
    visited = set()  # nodos ya visitados

    while current_paths:
        current_paths.sort(key=lambda path: path.total_cost + Distance(path.nodes[-1], destino))
        current_path = current_paths.pop(0)
        last_node = current_path.nodes[-1]

        if last_node == destino:
            return current_path

        if last_node in visited:
            continue  # ya expandido, evitar redundancia
        visited.add(last_node)

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

#función que pinta los nodos alcanzables desde uno seleccionado
def Reachability(grafo, figsize=None, xticks=None, yticks=None, start_node=None):
    alcanzables = set()
    if start_node is not None:
        visitados = set()
        cola = [start_node]
        while cola:
            nodo = cola.pop(0)
            if nodo not in visitados:
                visitados.add(nodo)
                for vecino in nodo.neighbors:
                    if vecino not in visitados:
                        cola.append(vecino)
        alcanzables = visitados
    plt.figure(figsize=figsize)
    for nodo in grafo.nodes:
        if nodo == start_node:
            color = 'lightgreen'
            size = 140
            text_color = 'grey'
            font_weight = 'bold'
        elif nodo in alcanzables:
            color = 'grey'
            size = 120
            text_color = 'lightgreen'
            font_weight = 'bold'
        else:
            color = 'lightgrey'
            size = 100
            text_color = 'lightgrey'
            font_weight = 'bold'
        plt.scatter(nodo.coordinate_x, nodo.coordinate_y, color=color, s=size)
        plt.text(nodo.coordinate_x, nodo.coordinate_y, nodo.name, fontsize=10, color=text_color, fontweight=font_weight)
    plt.grid(color='lightpink')
    if xticks is not None:
        plt.xticks(xticks)
    if yticks is not None:
        plt.yticks(yticks)

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

#exportar una ruta a un archivo .kml
def export_to_kml(path, filename):
    kml_header = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<kml xmlns="http://www.opengis.net/kml/2.2">'
        '<Document>'
        f'<name>Shortest Path</name>'
        f'<description>Path from {path.origen.name} to {path.destination.name}</description>'
    )
    kml_footer = '</Document></kml>'
    coordinates = " ".join(f"{node.coordinate_x},{node.coordinate_y},0" for node in path.nodes)
    kml_linestring = (
        '<Placemark>'
        '<name>Ruta mas corta</name>'
        '<Style>'
        '<LineStyle>'
        '<color>ff0000ff</color>'
        '<width>4</width>'
        '</LineStyle>'
        '</Style>'
        '<LineString>'
        '<tessellate>1</tessellate>'
        f'<coordinates>{coordinates}</coordinates>'
        '</LineString>'
        '</Placemark>')
    kml_content = kml_header + kml_linestring + kml_footer
    with open(filename, "w", encoding="utf-8") as f:
        f.write(kml_content)

#alcanzabilidad de un nodo sobre otro (función extra 1)
def Alcanzabilidad(g, n1, n2, visited=None):
    if visited is None:
        visited = set()
    visited.add(n1)
    if n1 == n2:
        return True
    for neighbor in n1.neighbors:
        if neighbor not in visited:
            if Alcanzabilidad(g, neighbor, n2, visited):
                return True
    return False