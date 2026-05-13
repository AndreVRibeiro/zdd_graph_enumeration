import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from asyncio import graph
from graph.graph import Graph
from frontier.frontier_state import FrontierState
from constructor.constructor import construct_zdd_for_st_paths, enumerate_paths_from_zdd
from zdd.zdd import ZDD, ZDDNode


class Gui(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("ZDD s-t Path Visualizer")
        self.geometry("1400x800")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1, uniform="panels")
        self.grid_columnconfigure(1, weight=1, uniform="panels")
        self.grid_rowconfigure(0, weight=1)

        #self.grid_columnconfigure(0, uniform="a")
        #self.grid_columnconfigure(1, uniform="a")

        self.selected_path = ctk.StringVar(value="")

        self.G = nx.Graph()
        self.edge_list = []

        self.create_graph_panel()
        self.create_zdd_panel()

        
    def create_graph_panel(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        #frame.grid_propagate(False)

        frame.grid_rowconfigure(0, weight=3)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Graph area
        graph_frame = ctk.CTkFrame(frame)
        graph_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        graph_frame.grid_columnconfigure(0, weight=1)
        graph_frame.grid_rowconfigure(0, weight=1)

        self.fig_graph, self.ax_graph = plt.subplots(figsize=(5, 5))
        self.ax_graph.axis("off")
        self.ax_graph.set_title("Graph")
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=graph_frame)
        self.canvas_graph.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        #self.canvas_graph.get_tk_widget().pack(fill="both", expand=True)

        # Control area
        control_frame = ctk.CTkFrame(frame)
        control_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_rowconfigure(0, weight=1)
        control_frame.grid_rowconfigure(1, weight=0)

        # Vertices
        vertices_frame = ctk.CTkFrame(control_frame)
        vertices_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        vertices_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            vertices_frame,
            text="Vertices (example: A B C D)",
            anchor="w"
        ).grid(row=0, column=0, sticky="ew")

        self.vertices_box = ctk.CTkTextbox(vertices_frame, height=60)
        self.vertices_box.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        self.vertices_box.bind("<KeyRelease>", self.update_graph)
        
        # Edges
        edges_frame = ctk.CTkFrame(control_frame)
        edges_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        edges_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            edges_frame,
            text="Edges (one per line, example: A B)",
            anchor="w"
        ).grid(row=0, column=0, sticky="ew")

        self.edges_box = ctk.CTkTextbox(edges_frame, height=60)
        self.edges_box.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        self.edges_box.bind("<KeyRelease>", self.update_graph)

        # s and t dropdowns
        st_frame = ctk.CTkFrame(control_frame)
        st_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        st_frame.grid_columnconfigure(0, weight=1)
        st_frame.grid_columnconfigure(1, weight=1)

        self.s_vertex = ctk.StringVar(value="s")
        self.t_vertex = ctk.StringVar(value="t")

        self.s_menu = ctk.CTkOptionMenu(st_frame, variable=self.s_vertex, values=[], command=self.update_graph)
        self.s_menu.grid(row=0, column=0, sticky="ew", padx=2)

        self.t_menu = ctk.CTkOptionMenu(st_frame, variable=self.t_vertex, values=[], command=self.update_graph)
        self.t_menu.grid(row=0, column=1, sticky="ew", padx=2)

        # Build button
        self.build_button = ctk.CTkButton(control_frame, text="Build ZDD", command=self.build_zdd)
        self.build_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        

    def create_zdd_panel(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        #frame.grid_propagate(False)

        frame.grid_rowconfigure(0, weight=3)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # ZDD area
        zdd_frame = ctk.CTkFrame(frame)
        zdd_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        zdd_frame.grid_columnconfigure(0, weight=1)
        zdd_frame.grid_rowconfigure(0, weight=1)

        self.fig_zdd, self.ax_zdd = plt.subplots(figsize=(5, 5))
        self.ax_zdd.axis("off")
        self.ax_zdd.set_title("ZDD")
        self.canvas_zdd = FigureCanvasTkAgg(self.fig_zdd, master=zdd_frame)
        self.canvas_zdd.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        #self.canvas_zdd.get_tk_widget().pack(fill="both", expand=True)

        # Path buttons frame
        self.paths_frame = ctk.CTkFrame(frame, height=145)
        self.paths_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.paths_frame.grid_propagate(False)

        self.paths_frame.grid_columnconfigure(0, weight=1)
        self.paths_frame.grid_rowconfigure(0, weight=0)
        self.paths_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.paths_frame,
            text="All s → t paths",
            anchor="w"
        ).grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 2))

        self.paths_container = ctk.CTkScrollableFrame(self.paths_frame)
        self.paths_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        #self.paths_container.pack(fill="both", expand=True)


    #########################################################################################################
    ##### ZDD Construction and Visualization ################################################################
    #########################################################################################################

    def build_zdd(self):
        graph = self.make_graph_object()
        s = self.s_vertex.get()
        t = self.t_vertex.get()

        edge_order = self.edge_list

        zdd = ZDD()
        initial_frontier = FrontierState(graph, s, t)

        memo = {}
        root = construct_zdd_for_st_paths(0, initial_frontier, graph, zdd, memo, edge_order)
        paths = enumerate_paths_from_zdd(root, zdd, edge_order)

        print("Paths found in ZDD:")
        for p in paths:
            print(p)

        self.graph_obj = graph
        self.zdd_obj = zdd
        self.zdd_root = root
        self.paths = paths

        self.populate_paths()
        self.draw_zdd(zdd, root)

    
    def draw_zdd(self, zdd, root):
        G = self.zdd_to_networkx(root, zdd)

        self.ax_zdd.clear()

        pos = self.layered_layout(root)

        labels = nx.get_node_attributes(G, "label")

        node_shapes = {"zero": "s", "one": "s", "decision": "o"}
        node_color_map = {"zero": "red", "one": "green", "decision": "lightblue"}
        root_id = id(self.zdd_root)

        for ntype in ["decision", "zero", "one"]:
            nodes = [n for n, d in G.nodes(data=True) if d.get("type") == ntype]
            colors = []
            for n in nodes:
                if n == root_id:
                    colors.append("gray")  
                else:
                    colors.append(node_color_map[ntype])
            nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=colors, node_shape=node_shapes[ntype], node_size=500, ax=self.ax_zdd)
        

        nx.draw_networkx_edges(G, pos, ax=self.ax_zdd, arrows=True, arrowstyle='-|>', arrowsize=15, min_source_margin=15, min_target_margin=15)
        #nx.draw(G, pos, ax=self.ax_zdd, with_labels=False, node_size=1200, node_color="lightblue", arrows=True)
        labels = nx.get_node_attributes(G, "label")
        nx.draw_networkx_labels(G, pos, labels, ax=self.ax_zdd)

        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax_zdd, label_pos=0.25)

        self.ax_zdd.set_title("ZDD")
        self.ax_zdd.axis("off")
        self.canvas_zdd.draw()


    def zdd_to_networkx(self, root, zdd):

        G = nx.DiGraph()
        visited = set()

        def dfs(node):
            if node is None or node in visited:
                return

            visited.add(node)

            node_id = id(node)

            # Terminal nodes
            if node is zdd.ZERO:
                G.add_node(node_id, label="0", type="zero")
                return

            if node is zdd.ONE:
                G.add_node(node_id, label="1", type="one")
                return

            # Normal ZDD node
            label = f"e{node.edge_index}"
            G.add_node(node_id, label=label, type="decision")

            # low edge (0-branch)
            if node.low:
                G.add_edge(node_id, id(node.low), label="0")
                dfs(node.low)

            # high edge (1-branch)
            if node.high:
                G.add_edge(node_id, id(node.high), label="1")
                dfs(node.high)

        dfs(root)
        return G
    

    def compute_levels(self, root):
        from collections import deque

        levels = {}
        visited = set()

        queue = deque()
        queue.append((root, 0))

        while queue:
            node, depth = queue.popleft()

            if node is None or node in visited:
                continue

            visited.add(node)
            nid = id(node)

            if node is self.zdd_obj.ZERO or node is self.zdd_obj.ONE:
                levels[nid] = depth
                continue

            levels[nid] = depth

            if node.low:
                queue.append((node.low, depth))

            if node.high:
                queue.append((node.high, depth + 1))

        return levels
    

    # This is not otimized at all. I don't know how to structure it just like a ZDD. Its the best i can do for now :(
    def layered_layout(self, root):
        levels = self.compute_levels(root)

        from collections import defaultdict

        layers = defaultdict(list)

        for nid, lvl in levels.items():
            layers[lvl].append(nid)

        pos = {}

        max_level = max(layers.keys()) if layers else 0
        terminal_y = -(max_level + 2)

        for lvl in sorted(layers.keys()):
            nodes = layers[lvl]

            nodes = sorted(nodes)

            n = len(nodes)

            x_spacing = 2.5
            y = -lvl * 2.5

            for i, nid in enumerate(nodes):
                x = (i - (n - 1) / 2) * x_spacing
                pos[nid] = (x, y)

        for node in self.zdd_to_networkx(self.zdd_root, self.zdd_obj).nodes():
            if node not in pos:
                # fallback placement
                pos[node] = (0, terminal_y)


        return pos
    
    #########################################################################################################
    #### Graph Contruction from GUI Inuput ##################################################################
    #########################################################################################################

    def make_graph_object(self):
        graph = Graph()

        for v in self.G.nodes:
            graph.add_vertex(v)

        for u, v in self.edge_list:
            graph.add_edge(u, v)

        return graph
    

    def draw_graph(self, highlight_edges=None):
        self.ax_graph.clear()
        if len(self.G.nodes) == 0:
            return
        
        pos = nx.spring_layout(self.G)
        self.pos = pos

        colors = []
        for node in self.G.nodes:
            if node == self.s_vertex.get():
                colors.append("green")
            elif node == self.t_vertex.get():
                colors.append("red")
            else:
                colors.append("lightblue")
        
        nx.draw(self.G, pos, ax=self.ax_graph, with_labels=True, node_color=colors)

        edge_labels = {edge: f"e{i}" for i, edge in enumerate(self.edge_list)}

        nx.draw_networkx_edges(self.G, pos, edgelist=self.edge_list, ax=self.ax_graph)

        if highlight_edges:
            nx.draw_networkx_edges(self.G, pos, edgelist=highlight_edges, width=4, edge_color="orange", ax=self.ax_graph)
            
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax_graph, label_pos=0.5, font_size=10)

        self.ax_graph.set_title("Graph")
        self.canvas_graph.draw()
    
    
    def update_graph(self, event=None):
        vertices = self.vertices_box.get("1.0", "end").split()
        lines = self.edges_box.get("1.0", "end").splitlines()

        self.G.clear()
        self.G.add_nodes_from(vertices)

        self.edge_list = []

        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) == 2:
                u, v = sorted(parts)

                self.G.add_edge(u, v)

                self.edge_list.append((u, v))

        self.update_st_menus(vertices)
        self.draw_graph() 


    def update_st_menus(self, vertices):
        self.s_menu.configure(values=vertices)
        self.t_menu.configure(values=vertices)

        if self.s_vertex.get() not in vertices:
            self.s_vertex.set("s")

        if self.t_vertex.get() not in vertices:
            self.t_vertex.set("t")


    #########################################################################################################
    #### Path Buttons #######################################################################################
    #########################################################################################################

    def on_path_selected(self):
        idx = int(self.selected_path.get())
        path = self.paths[idx]
        self.highlight_path(path)


    def populate_paths(self):

        # clear old widgets
        for widget in self.paths_container.winfo_children():
            widget.destroy()

        for i, path in enumerate(self.paths):
            # convert path edges to e-indices
            labels = [
                f"e{self.edge_list.index(tuple(sorted(edge)))}"
                for edge in path
            ]
            path_str = ", ".join(labels)

            rb = ctk.CTkRadioButton(self.paths_container, text=path_str, variable=self.selected_path, value=str(i), command=self.on_path_selected)
            rb.pack(anchor="w", padx=5, pady=2)


    def highlight_path(self, path):
        self.draw_graph(highlight_edges=path)

    #########################################################################################################
    #### Necessary otherwise it doesn't close properly ######################################################
    #########################################################################################################

    def on_close(self):
        try:
            plt.close("all")  
        except:
            pass

        self.destroy()        
        self.quit()

