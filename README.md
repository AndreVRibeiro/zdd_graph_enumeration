# ZDD - Graph enumeration
This project implements a frontier-based construction of Zero-suppressed Decision Diagrams (ZDDs) to compactly represent and count all paths between two nodes s and t in an undirected graph.

Instead of enumerating paths explicitly, the algorithm explores edge decisions while maintaining frontier constraints (degree and connectivity) and builds the ZDD on the fly using zero-suppression and node merging. This demonstrates how ZDDs can efficiently represent large families of subgraphs arising in graph enumeration problems.

The implementation is written from scratch in Python for educational and demonstrational purposes.
