from path import Path, AddNodeToPath, ContainsNode, CostToNode
from node import Node

n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)

p = Path()
p = AddNodeToPath(p, n1)
p = AddNodeToPath(p, n2)

assert p.total_cost() == 5.0  #esta función la aprendí ayer y verifica igualdades
print("Todo bien.")