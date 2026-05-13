# ZDD - Graph enumeration
This project implements a frontier-based construction of Zero-suppressed Decision Diagrams (ZDDs) to compactly represent and count all paths between two nodes s and t in an undirected graph.

Instead of enumerating paths explicitly, the algorithm explores edge decisions while maintaining frontier constraints (degree and connectivity) and builds the ZDD on the fly using zero-suppression and node merging. This demonstrates how ZDDs can efficiently represent large families of subgraphs arising in graph enumeration problems.

The implementation is written from scratch in Python for educational and demonstrational purposes.

# ▶️ How to Run the Program

This project provides two entry points:

- main.py → runs predefined example graphs in the terminal
- mainGUI.py → launches the graphical interface to build your own graphs and visualize the ZDD

## 🧪 Run the Examples (Terminal Only)

The file main.py contains several example graphs already defined as functions and also called inside the main() function.

Simply run: python main.py

This will:

- Construct the example graphs
- Build the ZDD for each graph
- Output all s → t paths in the terminal

This is the core functionality of the project and demonstrates the algorithm without any GUI.

## 🖥️ Run the GUI

To use the graphical interface, run: python mainGUI.py

The window is divided into two main parts.

### Left Side — Graph Input

You must provide:
- Vertices (space separated)
- Edges (one per line, format: u v)
- Select the start vertex (s) and target vertex (t)

Then press the button to build the ZDD.

### Right Side — ZDD and Paths

After building:
- The top panel shows the ZDD representing the sparse family of sets encoding all s → t paths
- The bottom panel lists all paths as edge IDs (e0, e1, …)

By selecting a path from the list:
- The corresponding path is highlighted in the graph on the left
## ⚠️ Visualization Disclaimer

The ZDD drawing uses a custom layout implemented with networkx and matplotlib.

Because of this, in some cases:
- Edges in the ZDD may overlap
- The diagram may look crowded or hard to read

If this happens, simply press the build button again.
Due to layout randomness, the ZDD may be drawn in a clearer way on the next attempt.

This does not affect the correctness of the algorithm — only the visualization.

## Use of AI Tools in This Project

This project was developed for the Seminar "Knowledge, Reasoning and Planning" at the University of Basel as part of my seminar work on Zero-suppressed Decision Diagrams (ZDDs). The core algorithmic implementation, which includes the graph modeling, frontier state handling, ZDD construction, memoization strategy, and path enumeration was designed, implemented, and tested by me.

AI tools (specifically ChatGPT) were used as a supporting resource during development in the following ways:

- Clarifying theoretical concepts related to ZDDs and frontier-based construction
- Answering questions when I was uncertain about specific implementation details
- Acting as a guide when reasoning about design decisions
- Assisting with debugging and general Python questions
- Providing guidance on GUI layout and grid management, as I had limited prior experience with Python GUI frameworks

The graphical user interface is a supplementary visualization tool intended to make the results of the algorithm easier to inspect. Since GUI development was not the focus of this project, AI assistance was used more actively in this part to understand layout structures and rendering approaches.

AI was not used to generate the core algorithm, data structures, or logic of the ZDD construction. Instead, it served as an interactive reference, similar to documentation, tutorials, or discussion forums, helping to resolve questions and validate understanding during the development process.

This disclosure is provided to ensure transparency regarding the role of AI in the project.
