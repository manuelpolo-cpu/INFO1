from segment import Segment
from node import Node
n1 = Node("aaa",0,0)
n2 = Node("bbb",3,4)
n3 = Node("ccc",10,8)
segment1 = Segment("Segement",n1,n2)
segment2 = Segment("Segment2",n2,n3)
print(f"{segment1.name}, Cost: {segment1.cost}")
print(f"{segment2.name}, Cost: {segment2.cost}")