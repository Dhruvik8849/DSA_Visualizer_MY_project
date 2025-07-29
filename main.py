import tkinter as tk
from tkinter import ttk
from stack_visualizer import StackVisualizer
from queue_visualizer import QueueVisualizer
from tree_visualizer import TreeVisualizer
from graph_visualizer import GraphVisualizer

class DSAVisualizerApp:
    
    def __init__(self, root):
       
        self.root = root
        self.root.title("DSA Visualizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")

        # Style for the widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton",
                        font=("Helvetica", 14),
                        padding=10,
                        background="#3498DB",
                        foreground="white",
                        borderwidth=0)
        style.map("TButton",
                  background=[('active', '#2980B9')])
        style.configure("TFrame", background="#2C3E50")
        style.configure("TLabel", background="#2C3E50", foreground="white", font=("Helvetica", 24, "bold"))

        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = ttk.Label(main_frame, text="Data Structures & Algorithms Visualizer")
        title_label.pack(pady=30)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # --- Buttons to launch visualizers ---
        stack_button = ttk.Button(button_frame, text="Stack", command=self.open_stack_visualizer)
        stack_button.grid(row=0, column=0, padx=15, pady=15)

        queue_button = ttk.Button(button_frame, text="Queue", command=self.open_queue_visualizer)
        queue_button.grid(row=0, column=1, padx=15, pady=15)

        tree_button = ttk.Button(button_frame, text="Binary Search Tree", command=self.open_tree_visualizer)
        tree_button.grid(row=1, column=0, padx=15, pady=15)

        graph_button = ttk.Button(button_frame, text="Graph", command=self.open_graph_visualizer)
        graph_button.grid(row=1, column=1, padx=15, pady=15)

    def _open_visualizer_window(self, visualizer_class, title):
        """
        Creates a new Toplevel window for a specific visualizer.
        Args:
            visualizer_class: The class of the visualizer to instantiate.
            title (str): The title for the new window.
        """
        # Create a new top-level window
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("1000x700")
        new_window.configure(bg="#34495E")
        
        # Instantiate the visualizer class within the new window
        app = visualizer_class(new_window)

    def open_stack_visualizer(self):
        """Opens the Stack Visualizer window."""
        self._open_visualizer_window(StackVisualizer, "Stack Visualizer")

    def open_queue_visualizer(self):
        """Opens the Queue Visualizer window."""
        self._open_visualizer_window(QueueVisualizer, "Queue Visualizer")

    def open_tree_visualizer(self):
        """Opens the Tree Visualizer window."""
        self._open_visualizer_window(TreeVisualizer, "Binary Search Tree Visualizer")

    def open_graph_visualizer(self):
        """Opens the Graph Visualizer window."""
        self._open_visualizer_window(GraphVisualizer, "Graph Traversal Visualizer")


if __name__ == "__main__":
    # Before running, make sure you have the required libraries:
    # pip install matplotlib networkx
    
    main_root = tk.Tk()
    app = DSAVisualizerApp(main_root)
    main_root.mainloop()