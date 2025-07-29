import tkinter as tk
from tkinter import ttk, messagebox
import time

class Node:
    """A node in a binary search tree."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

class TreeVisualizer:
    """
    A class to visualize a Binary Search Tree using tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.tree_root = None
        self.node_radius = 20
        self.h_spacing = 40
        self.v_spacing = 70

        # --- UI Setup ---
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(side="top", fill="x")
        
        self.canvas = tk.Canvas(self.root, bg="#ECF0F1", width=980, height=600)
        self.canvas.pack(expand=True, fill="both")

        # --- Controls ---
        ttk.Label(self.control_frame, text="Value:").pack(side="left", padx=5)
        self.entry = ttk.Entry(self.control_frame, width=10)
        self.entry.pack(side="left", padx=5)

        self.insert_button = ttk.Button(self.control_frame, text="Insert", command=self.insert_node)
        self.insert_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(self.control_frame, text="Clear Tree", command=self.clear_tree)
        self.clear_button.pack(side="left", padx=5)

        self.draw_tree()

    def _set_node_positions(self, node, x, y, level_width):
        """Recursively set the (x, y) coordinates for each node."""
        if node is not None:
            node.x = x
            node.y = y
            if node.left:
                self._set_node_positions(node.left, x - level_width / 2, y + self.v_spacing, level_width / 2)
            if node.right:
                self._set_node_positions(node.right, x + level_width / 2, y + self.v_spacing, level_width / 2)

    def draw_tree(self):
        """Draws the entire tree on the canvas."""
        self.canvas.delete("all")
        if self.tree_root:
            canvas_width = self.canvas.winfo_width()
            self._set_node_positions(self.tree_root, canvas_width / 2, 50, canvas_width / 2)
            self._draw_node_recursive(self.tree_root)

    def _draw_node_recursive(self, node):
        """Recursively draws nodes and the edges connecting them."""
        if node:
            # Draw edge to left child
            if node.left:
                self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill="gray", width=2)
                self._draw_node_recursive(node.left)
            # Draw edge to right child
            if node.right:
                self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="gray", width=2)
                self._draw_node_recursive(node.right)
            
            # Draw the node itself (oval and text)
            x1, y1 = node.x - self.node_radius, node.y - self.node_radius
            x2, y2 = node.x + self.node_radius, node.y + self.node_radius
            self.canvas.create_oval(x1, y1, x2, y2, fill="#9B59B6", outline="#8E44AD", width=2)
            self.canvas.create_text(node.x, node.y, text=str(node.key), font=("Helvetica", 12, "bold"), fill="white")

    def insert_node(self):
        """Handles the insert button click."""
        try:
            value = int(self.entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid integer.")
            return

        if self.tree_root is None:
            self.tree_root = Node(value)
        else:
            self._insert_recursive(self.tree_root, value)
        
        self.entry.delete(0, tk.END)
        self.draw_tree()
        self.root.update_idletasks()

    def _insert_recursive(self, current_node, value):
        """Recursively finds the correct position and inserts a new node."""
        if value < current_node.key:
            if current_node.left is None:
                current_node.left = Node(value)
            else:
                self._insert_recursive(current_node.left, value)
        elif value > current_node.key:
            if current_node.right is None:
                current_node.right = Node(value)
            else:
                self._insert_recursive(current_node.right, value)
        else:
            # Value already exists in the tree
            messagebox.showinfo("Duplicate", f"Value {value} already exists in the tree.")

    def clear_tree(self):
        """Clears the tree."""
        self.tree_root = None
        self.draw_tree()
        messagebox.showinfo("Tree Cleared", "The binary search tree has been cleared.")

