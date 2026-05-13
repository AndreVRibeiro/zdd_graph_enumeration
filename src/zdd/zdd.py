from zdd.zddNode import ZDDNode
# ===== ZDD  =====

class ZDD:
    def __init__(self):
        # Terminal nodes
        self.ZERO = ZDDNode(None, None, None)
        self.ONE = ZDDNode(None, None, None)

        self.isomorphism_table = {}

    def make_node_and_children(self, edge_index, low, high):
        # Zero-suppression reduction rule
        if high is self.ZERO:
            return low
        
        key = (edge_index, id(low), id(high))

        # Isomorphism reduction rule
        if key in self.isomorphism_table:
            return self.isomorphism_table[key]
        
        node = ZDDNode(edge_index, low, high)
        self.isomorphism_table[key] = node
        return node