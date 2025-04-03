import math

class Segment:
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = self.calculate_cost()  # Llamar al método para calcular el costo automáticamente

    def calculate_cost(self):
        # Suponiendo que 'origin' y 'destination' tienen 'coordinate_x' y 'coordinate_y'
        dx = self.destination.coordinate_x - self.origin.coordinate_x  # Diferencia en X
        dy = self.destination.coordinate_y - self.origin.coordinate_y  # Diferencia en Y
        return math.sqrt(dx**2 + dy**2)  # Distancia euclidiana entre los dos nodos
