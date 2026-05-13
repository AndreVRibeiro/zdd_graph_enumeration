# ===== Core algorithm =====

def construct_zdd_for_st_paths(k, state, graph, zdd, memo, edge_order):

    # Terminal node: All edges decided
    if k == graph.number_of_edges():
        if state.is_valid_terminal():
            return zdd.ONE
        else:
            return zdd.ZERO
        
    key = (k, state.signature())
    if key in memo:
        return memo[key]
    
    u, v = edge_order[k]

    # 0-branch: do not take the edge
    state0 = state.copy()
    low = construct_zdd_for_st_paths(k+1, state0, graph, zdd, memo, edge_order)

    # 1-branch: take the edge
    state1 = state.copy()
    if state1.take_edge(u, v):
        high = construct_zdd_for_st_paths(k+1, state1, graph, zdd, memo, edge_order)
    else:
        high = zdd.ZERO

    node = zdd.make_node_and_children(k, low, high)
    memo[key] = node
    return node


def enumerate_paths_from_zdd(node, zdd, edge_order):

    all_paths = []

    def dfs(current_node, chosen_edges):
        # If we hit ZERO → invalid branch
        if current_node is zdd.ZERO:
            return

        # If we hit ONE → valid s-t path found
        if current_node is zdd.ONE:
            all_paths.append(list(chosen_edges))
            return

        # Edge this node represents
        edge = edge_order[current_node.edge_index]

        # Follow 0-edge (edge NOT taken)
        dfs(current_node.low, chosen_edges)

        # Follow 1-edge (edge taken)
        chosen_edges.append(edge)
        dfs(current_node.high, chosen_edges)
        chosen_edges.pop()

    dfs(node, [])
    return all_paths