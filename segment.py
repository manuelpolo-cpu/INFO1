import math
class Segment:
    def __init__ (segment,name,origin,destination):
        segment.name = name
        segment.origin = origin
        segment.destination = destination
        segment.cost = segment.calculate_cost()
    def calculate_cost(segment):
        return math.sqrt((segment.destination.coordinate_x-segment.origin.coordinate_x)**2+(segment.destination.coordinate_y-segment.origin.coordinate_y)**2)