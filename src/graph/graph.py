# ===== Graph representation =====

class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = []
        self.adjacency = {} 
    
    # Add a vertex to the graph
    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.add(v)
            self.adjacency[v] = []
    
    # Add an edge to the graph
    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)

        edge_index = len(self.edges)
        self.edges.append((u, v))

        self.adjacency[u].append(edge_index)
        self.adjacency[v].append(edge_index)

    def get_edge(self, index):
        return self.edges[index]
    
    def incident_edges(self, v):
        return self.adjacency[v]
    
    def number_of_edges(self):
        return len(self.edges)
    
    def number_of_vertices(self):
        return len(self.vertices)