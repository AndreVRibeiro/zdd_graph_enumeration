from graph.graph import Graph
from frontier.frontier_state import FrontierState
from constructor.constructor import construct_zdd_for_st_paths, enumerate_paths_from_zdd
from zdd.zdd import ZDD, ZDDNode



def example_single_path():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")

    edge_order = graph.edges

    zdd = ZDD()
    initial_frontier = FrontierState(graph, "A", "D")

    memo = {}
    root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)

    paths = enumerate_paths_from_zdd(root, zdd, edge_order)

    print_paths(paths, "Example — Single Path")
    

def example_diamond():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")

    edge_order = graph.edges

    zdd = ZDD()
    initial_frontier = FrontierState(graph, "A", "D")

    memo = {}
    root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)

    paths = enumerate_paths_from_zdd(root, zdd, edge_order)

    print_paths(paths, "Example — Diamond")


def example_diamond():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")

    edge_order = graph.edges

    zdd = ZDD()
    initial_frontier = FrontierState(graph, "A", "D")

    memo = {}
    root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)

    paths = enumerate_paths_from_zdd(root, zdd, edge_order)

    print_paths(paths, "Example — Diamond")


def example_cycle():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")  # cycle
    graph.add_edge("C", "E")
    graph.add_edge("E", "D")

    edge_order = graph.edges

    zdd = ZDD()
    initial_frontier = FrontierState(graph, "A", "D")

    memo = {}
    root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)

    paths = enumerate_paths_from_zdd(root, zdd, edge_order)

    print_paths(paths, "Example — Cycle Handling")


def example_layered():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    graph.add_edge("B", "E")
    graph.add_edge("E", "F")
    graph.add_edge("D", "F")

    edge_order = graph.edges

    zdd = ZDD()
    initial_frontier = FrontierState(graph, "A", "F")

    memo = {}
    root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)

    paths = enumerate_paths_from_zdd(root, zdd, edge_order)

    print_paths(paths, "Example — Layered Graph")


def example_dense():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")
    graph.add_edge("E", "F")
    graph.add_edge("F", "G")
    graph.add_edge("D", "G")

    edge_order = graph.edges

    zdd = ZDD()
    initial_frontier = FrontierState(graph, "A", "G")

    memo = {}
    root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)

    paths = enumerate_paths_from_zdd(root, zdd, edge_order)

    print_paths(paths, "Example — Dense Graph")



def print_paths(paths, example_name):
    print(f"Paths found in ZDD for {example_name}:")
    for p in paths:
        print(p)
    print(len(paths), " path(s) found!")


if __name__ == "__main__":
    example_single_path()
    example_diamond()
    example_cycle()
    example_layered()
    example_dense()