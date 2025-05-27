from path import *
class DummyNode:
    def __init__(self, name, lon, lat):
        self.name = name
        self.coordinate_x = lon  # longitud
        self.coordinate_y = lat  # latitud

# Simulamos 3 puntos en línea recta
nodo1 = DummyNode("A", -3.7038, 40.4168)  # Madrid
nodo2 = DummyNode("B", -0.1276, 51.5074)  # Londres
nodo3 = DummyNode("C", 2.3522, 48.8566)
class DummyPath:
    def __init__(self, nodes):
        self.nodes = nodes
        self.origen = nodes[0]
        self.destination = nodes[-1]

# Crear camino ficticio
camino_test = DummyPath([nodo1, nodo2, nodo3])
export_to_kml(camino_test, "flight_plan.kml")