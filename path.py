from node import Distance as distance

class Path:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def contains_node(self, node):
        return node in self.nodes

    def total_cost(self):
        cost = 0
        for i in range(len(self.nodes) - 1):
            cost += distance(self.nodes[i], self.nodes[i + 1])
        return cost

def AddNodeToPath(path, node):
    new_path = Path()
    new_path.nodes = path.nodes.copy()
    new_path.add_node(node)
    return new_path

def ContainsNode(path, node):
    return path.contains_node(node)

def CostToNode(path, node):
    if node not in path.nodes:
        return -1
    index = path.nodes.index(node)
    cost = 0
    for i in range(index):
        cost += distance(path.nodes[i], path.nodes[i + 1])
    return cost