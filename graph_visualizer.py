import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class GraphVisualizer:
    """
    A class to visualize Graph algorithms (BFS, DFS) using networkx and matplotlib.
    """
    def __init__(self, root):
        self.root = root
        self.graph = nx.Graph()
        self.node_positions = None

        # --- UI Setup ---
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(side="top", fill="x")

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(expand=True, fill="both")

        # --- Matplotlib Figure and Canvas ---
        self.fig, self.ax = plt.subplots(facecolor='#ECF0F1')
        self.tk_canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.tk_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # --- Controls ---
        # Add Node
        ttk.Label(self.control_frame, text="Node:").pack(side="left", padx=5)
        self.node_entry = ttk.Entry(self.control_frame, width=8)
        self.node_entry.pack(side="left", padx=5)
        self.add_node_button = ttk.Button(self.control_frame, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side="left", padx=5)

        # Add Edge
        ttk.Label(self.control_frame, text="Edge (u, v):").pack(side="left", padx=10)
        self.edge_u_entry = ttk.Entry(self.control_frame, width=5)
        self.edge_u_entry.pack(side="left")
        self.edge_v_entry = ttk.Entry(self.control_frame, width=5)
        self.edge_v_entry.pack(side="left", padx=5)
        self.add_edge_button = ttk.Button(self.control_frame, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack(side="left", padx=5)

        # Traversal
        ttk.Label(self.control_frame, text="Start Node:").pack(side="left", padx=10)
        self.start_node_entry = ttk.Entry(self.control_frame, width=8)
        self.start_node_entry.pack(side="left")
        self.bfs_button = ttk.Button(self.control_frame, text="Run BFS", command=self.run_bfs)
        self.bfs_button.pack(side="left", padx=5)
        self.dfs_button = ttk.Button(self.control_frame, text="Run DFS", command=self.run_dfs)
        self.dfs_button.pack(side="left", padx=5)
        
        # Clear
        self.clear_button = ttk.Button(self.control_frame, text="Clear Graph", command=self.clear_graph)
        self.clear_button.pack(side="right", padx=10)

        self.draw_graph()

    def draw_graph(self, highlight_nodes=None, highlight_color='yellow'):
        """Draws the graph on the matplotlib canvas."""
        self.ax.clear()
        if not self.graph.nodes():
            self.ax.text(0.5, 0.5, "Graph is empty. Add nodes and edges.", ha='center', va='center', transform=self.ax.transAxes)
            self.tk_canvas.draw()
            return

        # Recalculate positions only if nodes have been added/removed
        if self.node_positions is None or set(self.node_positions.keys()) != set(self.graph.nodes()):
            self.node_positions = nx.spring_layout(self.graph, seed=42)

        # Set node colors
        node_colors = []
        for node in self.graph.nodes():
            if highlight_nodes and node in highlight_nodes:
                node_colors.append(highlight_color)
            else:
                node_colors.append('#3498DB')

        nx.draw(self.graph, self.node_positions, ax=self.ax, with_labels=True,
                node_color=node_colors, node_size=700,
                font_color='white', font_size=12, font_weight='bold',
                edge_color='gray', width=2.0)
        
        self.ax.set_title("Graph Visualization")
        self.tk_canvas.draw()
        self.root.update_idletasks()

    def add_node(self):
        """Adds a node to the graph."""
        node = self.node_entry.get()
        if node:
            self.graph.add_node(node)
            self.node_entry.delete(0, tk.END)
            self.draw_graph()
        else:
            messagebox.showwarning("Input Error", "Please enter a node name.")

    def add_edge(self):
        """Adds an edge to the graph."""
        u, v = self.edge_u_entry.get(), self.edge_v_entry.get()
        if u and v:
            if u not in self.graph.nodes() or v not in self.graph.nodes():
                messagebox.showerror("Error", "Both nodes must exist in the graph before adding an edge.")
                return
            self.graph.add_edge(u, v)
            self.edge_u_entry.delete(0, tk.END)
            self.edge_v_entry.delete(0, tk.END)
            self.draw_graph()
        else:
            messagebox.showwarning("Input Error", "Please enter both nodes for the edge.")
            
    def _run_traversal(self, traversal_func):
        """Generic function to run and animate a graph traversal."""
        start_node = self.start_node_entry.get()
        if not start_node:
            messagebox.showwarning("Input Error", "Please enter a start node for the traversal.")
            return
        if start_node not in self.graph:
            messagebox.showerror("Error", f"Start node '{start_node}' not in graph.")
            return

        try:
            # Get the generator for the traversal
            traversal_iterator = traversal_func(self.graph, source=start_node)
            visited_nodes = []
            for node in traversal_iterator:
                visited_nodes.append(node)
                self.draw_graph(highlight_nodes=visited_nodes, highlight_color='#F1C40F')
                time.sleep(0.7)
            # Final highlight in green
            self.draw_graph(highlight_nodes=visited_nodes, highlight_color='#2ECC71')
        except Exception as e:
            messagebox.showerror("Traversal Error", f"An error occurred: {e}")


    def run_bfs(self):
        """Runs and animates the Breadth-First Search algorithm."""
        self._run_traversal(nx.bfs_tree)

    def run_dfs(self):
        """Runs and animates the Depth-First Search algorithm."""
        self._run_traversal(nx.dfs_tree)

    def clear_graph(self):
        """Clears the graph."""
        self.graph.clear()
        self.node_positions = None
        self.ax.clear()
        self.draw_graph()
        messagebox.showinfo("Graph Cleared", "The graph has been cleared.")
