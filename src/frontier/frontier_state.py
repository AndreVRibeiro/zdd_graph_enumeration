# ===== Frontier (mate + degree) =====

class FrontierState:
    def __init__(self, graph, s, t):
        self.graph = graph
        self.s = s
        self.t = t

        self.mate = {v: v for v in graph.vertices}      # dict: vertex -> vertex
        self.degree = {v: 0 for v in graph.vertices}    # dict: vertex -> 0/1/2
    

    def copy(self):
        f = FrontierState(self.graph, self.s, self.t)
        f.mate = self.mate.copy()
        f.degree = self.degree.copy()
        return f
    

    def get_root(self, v):
        while self.mate[v] != v:
            v = self.mate[v]
        return v
    

    def merge(self, u, v):
        ru = self.get_root(u)
        rv = self.get_root(v)

        if ru != rv:
            self.mate[rv] = ru


    def take_edge(self, u, v):
        # Increase degrees
        self.degree[u] += 1
        self.degree[v] += 1

        # Rule 1: No forks allowed
        if self.degree[u] > 2 or self.degree[v] > 2:
            return False
        
        # Rule 2: No cycles allowed
        if self.get_root(u) == self.get_root(v):
            return False
    
        self.merge(u, v)

        return True


    def is_valid_terminal(self):
        # s and t must have degree 1
        if self.degree[self.s] != 1 or self.degree[self.t] != 1:
            return False
        
        # all other vertices must have degree 0 or 2
        for v in self.graph.vertices:
            if v != self.s and v != self.t:
                if self.degree[v] not in (0,2):
                    return False
        
        return self.get_root(self.s) == self.get_root(self.t)


    def signature(self):
        comp = {}
        for v in self.graph.vertices:
            root = self.get_root(v)
            if root not in comp:
                comp[root] = []
            comp[root].append((v, self.degree[v]))
        
        normalized = []
        for group in comp.values():
            normalized.append(tuple(sorted(group)))
        normalized.sort()

        return tuple(normalized) 