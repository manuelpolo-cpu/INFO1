from segment import *
from node import *
n1 = Node('manuel',3,4)
n2 = Node('alex',0,0)
n3 = Node('javier',2,2)
A = Segment('prueba',n1,n2,Distance(n1,n2))
B = Segment('prueba_0',n2,n3,Distance(n2,n3))
print(A.__dict__)
print(B.__dict__)