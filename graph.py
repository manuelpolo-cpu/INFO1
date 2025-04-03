class Graph:
    def __init__(graph,nodes,segments):
        graph.nodes = []
        graph.segments = []

    def AddNode(graph,n):
        i = 0
        while i < len(graph.segments):

    def from_file(self,filen_ame):
        with open(file_name,'r') as file:
            lines = file.readlines()

        for line in lines:
            partes = line.srip().split()
            if partes[0] == "Node":
                name = partes[1]
                x = float(partes[2])
                y = float(partes[3])
                self.nodes.append(Node(name,x,y))
            elif partes[0] == "Segment":
                name = partes[1]
                origin_name = partes[2]
                destination_name = partes[3]

                origin = None
                destination = None
                for node in self.nodes:
                    if node.name == origin_name:
                        origin = node
                    if node.name == destination_name:
                        destination = node
                    if origin and destination:
                        break
                if origin and destination:
                    self.segments.append(Segment(name, origin, destination))