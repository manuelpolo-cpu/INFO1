from graph import Graph, Node
def CreateGraph(): 
    G = Graph() 
    G.AddNode(Node("A", 1, 20)) 
    G.AddNode(Node("B", 8, 17)) 
    G.AddNode(Node("C", 15, 20)) 
    G.AddNode(Node("D", 18, 15)) 
    G.AddNode(Node("E", 2, 4)) 
    G.AddNode(Node("F", 6, 5)) 
    G.AddNode(Node("G", 12, 12)) 
    G.AddNode(Node("H", 10, 3)) 
    G.AddNode(Node("I", 19, 1)) 
    G.AddNode(Node("J", 13, 5)) 
    G.AddNode(Node("K", 3, 15)) 
    G.AddNode(Node("L", 4, 10)) 
    
    G.AddSegment("A", "B") 
    G.AddSegment("A", "E") 
    G.AddSegment("A", "K") 
    G.AddSegment("B", "C") 
    G.AddSegment("B", "F") 
    G.AddSegment("B", "K") 
    G.AddSegment("B", "G") 
    G.AddSegment("C", "D") 
    G.AddSegment("C", "G") 
    G.AddSegment("D", "G") 
    G.AddSegment("D", "H") 
    G.AddSegment("D", "I") 
    G.AddSegment("E", "F") 
    G.AddSegment("F", "L") 
    G.AddSegment("G", "B") 
    G.AddSegment("G", "F") 
    G.AddSegment("G", "H") 
    G.AddSegment("I", "D") 
    G.AddSegment("I", "J") 
    G.AddSegment("K", "L") 
    G.AddSegment("L", "F") 
    
    return G 

G = CreateGraph() 
G.Plot() 
G.PlotNode("C") 

n = G.GetClosest(15, 5) 
print(n.name)  # La respuesta debe ser J 

n = G.GetClosest(8, 19)  
print(n.name)  # La respuesta debe ser B 
