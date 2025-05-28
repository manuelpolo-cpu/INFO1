# path.py
import matplotlib.pyplot as plt
import math

# Clase Path
class Path:
    def __init__(self, origen, destination):
        self.nodes = []
        self.cost = 0.0
        self.origen = origen
        self.destination = destination

# Añadir nodo al camino
def AddNodeToPath(P, n):
    for node in P.nodes:
        if n.name == node.name:
            return False
    P.nodes.append(n)
    return True

# Calcular distancia entre dos nodos
def Distance(node1, node2):
    dx = node1.coordinate_x - node2.coordinate_x
    dy = node1.coordinate_y - node2.coordinate_y
    return math.sqrt(dx*dx + dy*dy)

# Buscar si el camino contiene un nodo
def ContainsNode(p, n):
    for node in p.nodes:
        if node.name == n.name:
            return True
    return False

# Encontrar el camino más corto (Dijkstra o similar)
def FindShortestPath(grafo, origen, destino):
    initial_path = Path(origen, destino)
    AddNodeToPath(initial_path, origen)
    current_paths = [initial_path]
    while current_paths:
        current_paths.sort(key=lambda path: path.cost + Distance(path.nodes[-1], destino))
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
            new_path.cost = current_path.cost + Distance(last_node, neighbor)
            current_paths.append(new_path)
    return None

# Plotear el camino
def PlotPath(G, P, figsize, xticks, yticks):
    total_cost = 0
    camino_parcial = Path(P.origen, P.destination)
    AddNodeToPath(camino_parcial, P.nodes[0])
    flechas_hechas = []  # [(origen, destino)]
    costes_hechos = []   # [(x_medio, y_medio, coste)]

    for i in range(len(P.nodes) - 1):
        current_node = P.nodes[i]
        next_node = P.nodes[i + 1]
        AddNodeToPath(camino_parcial, next_node)

        segmento = next((s for s in G.segments if
                         (s.origin == current_node and s.destination == next_node) or
                         (s.origin == next_node and s.destination == current_node)), None)
        coste = segmento.cost if segmento else 0
        total_cost += coste
        mid_x = (current_node.coordinate_x + next_node.coordinate_x)/2
        mid_y = (current_node.coordinate_y + next_node.coordinate_y)/2
        costes_hechos.append((mid_x, mid_y, coste))
        flechas_hechas.append((current_node, next_node))

    plt.figure(figsize=figsize)
    for node in G.nodes:
        plt.scatter(node.coordinate_x, node.coordinate_y, color='lightgrey', s=100)
        plt.text(node.coordinate_x, node.coordinate_y, node.name, fontsize=10, color='lightgrey', fontweight='bold')
    for (origen, destino) in flechas_hechas:
        plt.annotate("",
                     xy=(destino.coordinate_x, destino.coordinate_y),
                     xytext=(origen.coordinate_x, origen.coordinate_y),
                     arrowprops=dict(facecolor="skyblue", edgecolor="skyblue", arrowstyle="->", lw=2))
    for (x, y, c) in costes_hechos:
        plt.text(x, y, f"{c:.2f}", color="black", fontsize=10, fontweight='bold', va='center', ha='center')
    for node in camino_parcial.nodes:
        plt.scatter(node.coordinate_x, node.coordinate_y, color='grey', s=120)
        plt.text(node.coordinate_x, node.coordinate_y, node.name, fontsize=10, color='lightgreen', fontweight='bold')
    plt.title(f"Camino completo de {P.origen.name} → {P.destination.name} | Coste total: {total_cost:.2f}")
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.grid(color='lightpink')

# Función para exportar a KML
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