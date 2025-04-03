import matplotlib.pyplot as plt
class Node:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

class Segment:
    def __init__(self, orig, dest):
        self.origin = orig
        self.destination = dest
        self.cost = ((orig.x - dest.x) ** 2 + (orig.y - dest.y) ** 2) ** 0.5

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []
    
    def AddNode(self, n):
        if any(node.name == n.name for node in self.nodes):
            return False
        self.nodes.append(n)
        return True
    
    def AddSegment(self, OriginNode, DestinationNode):
        origin = next((node for node in self.nodes if node.name == OriginNode), None)
        destination = next((node for node in self.nodes if node.name == DestinationNode), None)
        
        if not origin or not destination:
            return False
        
        segment = Segment(origin, destination)
        self.segments.append(segment)
        origin.neighbors.append(destination)
        destination.neighbors.append(origin)
        return True
    
    def GetClosest(self, x, y):
        return min(self.nodes, key=lambda node: (node.x - x) ** 2 + (node.y - y) ** 2)
    
    def Plot(self):
        import matplotlib.pyplot as plt
        
        plt.figure()
        for segment in self.segments:
            plt.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], 'bo-')
            plt.text((segment.origin.x + segment.destination.x) / 2,
                     (segment.origin.y + segment.destination.y) / 2,
                     f'{segment.cost:.2f}', color='red')
        
        for node in self.nodes:
            plt.text(node.x, node.y, node.name, fontsize=12, color='black')
        plt.show()
    
    def PlotNode(self, nameOrigin):
        import matplotlib.pyplot as plt
        
        origin = next((node for node in self.nodes if node.name == nameOrigin), None)
        if not origin:
            return False
        
        plt.figure()
        for segment in self.segments:
            color = 'gray'
            if segment.origin == origin or segment.destination == origin:
                color = 'red'
            plt.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], color+'-')
            plt.text((segment.origin.x + segment.destination.x) / 2,
                     (segment.origin.y + segment.destination.y) / 2,
                     f'{segment.cost:.2f}', color='red')
        
        for node in self.nodes:
            if node == origin:
                plt.plot(node.x, node.y, 'bo')
            elif node in origin.neighbors:
                plt.plot(node.x, node.y, 'go')
            else:
                plt.plot(node.x, node.y, 'ko')
            plt.text(node.x, node.y, node.name, fontsize=12, color='black')
        
        plt.show()
        return True
