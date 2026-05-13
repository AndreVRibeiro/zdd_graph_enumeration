# ===== ZDD Node =====

class ZDDNode:
    def __init__(self, edge_index, low, high) :
        self.low = low                  # 0-edge
        self.high = high                # 1-edge
        self.edge_index = edge_index    # index of the edge this node represents
