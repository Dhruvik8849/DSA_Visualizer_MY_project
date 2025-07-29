import tkinter as tk
from tkinter import ttk, messagebox
import time

class QueueVisualizer:
    """
    A class to visualize the Queue data structure using tkinter.
    """
    def __init__(self, root):
        """
        Initializes the Queue Visualizer GUI.
        Args:
            root (tk.Toplevel): The parent window for this visualizer.
        """
        self.root = root
        self.queue = []
        self.max_size = 10

        # --- UI Setup ---
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(side="top", fill="x")
        
        self.canvas_frame = ttk.Frame(self.root, padding="10")
        self.canvas_frame.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self.canvas_frame, bg="#ECF0F1", width=800, height=300)
        self.canvas.pack(expand=True, fill="both")

        # --- Controls ---
        ttk.Label(self.control_frame, text="Value:").pack(side="left", padx=5)
        self.entry = ttk.Entry(self.control_frame, width=10)
        self.entry.pack(side="left", padx=5)

        self.enqueue_button = ttk.Button(self.control_frame, text="Enqueue", command=self.enqueue)
        self.enqueue_button.pack(side="left", padx=5)

        self.dequeue_button = ttk.Button(self.control_frame, text="Dequeue", command=self.dequeue)
        self.dequeue_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(self.control_frame, text="Clear", command=self.clear_queue)
        self.clear_button.pack(side="left", padx=5)

        self.draw_queue()

    def draw_queue(self):
        """
        Draws the current state of the queue on the canvas.
        """
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        box_width = 70
        box_height = 50
        y_center = canvas_height / 2
        start_x = 50

        if not self.queue:
            self.canvas.create_text(canvas_width / 2, y_center, text="Queue is empty", font=("Helvetica", 14), fill="gray")
        else:
            for i, value in enumerate(self.queue):
                x = start_x + i * (box_width + 10)
                x1 = x
                y1 = y_center - box_height / 2
                x2 = x + box_width
                y2 = y_center + box_height / 2
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#1ABC9C", outline="#16A085", width=2)
                self.canvas.create_text(x + box_width / 2, y_center, text=str(value), font=("Helvetica", 14, "bold"), fill="white")

        # Draw Front and Rear pointers
        if self.queue:
            # Front pointer
            front_x = start_x + box_width / 2
            self.canvas.create_text(front_x, y_center - 50, text="Front", font=("Helvetica", 12, "bold"), fill="#2980B9")
            self.canvas.create_line(front_x, y_center - 40, front_x, y_center - box_height/2, arrow=tk.LAST, width=2, fill="#2980B9")
            
            # Rear pointer
            rear_x = start_x + (len(self.queue) - 1) * (box_width + 10) + box_width / 2
            self.canvas.create_text(rear_x, y_center + 50, text="Rear", font=("Helvetica", 12, "bold"), fill="#E74C3C")
            self.canvas.create_line(rear_x, y_center + 40, rear_x, y_center + box_height/2, arrow=tk.FIRST, width=2, fill="#E74C3C")


    def enqueue(self):
        """
        Handles the enqueue operation.
        """
        value = self.entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value to enqueue.")
            return
        
        if len(self.queue) >= self.max_size:
            messagebox.showwarning("Queue Full", f"Queue is full (max size: {self.max_size}).")
            return

        self.queue.append(value)
        self.entry.delete(0, tk.END)
        self.animate_enqueue()

    def animate_enqueue(self):
        """
        Animates the enqueue operation.
        """
        self.draw_queue()
        self.root.update_idletasks()

    def dequeue(self):
        """
        Handles the dequeue operation.
        """
        if not self.queue:
            messagebox.showinfo("Queue Empty", "Queue is empty, cannot dequeue.")
            return
        
        self.animate_dequeue()

    def animate_dequeue(self):
        """
        Animates the dequeue operation.
        """
        canvas_height = self.canvas.winfo_height()
        box_width = 70
        box_height = 50
        y_center = canvas_height / 2
        start_x = 50
        
        x1 = start_x
        y1 = y_center - box_height / 2
        x2 = start_x + box_width
        y2 = y_center + box_height / 2
        
        # Highlight the front element
        highlight_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F1C40F", outline="#F39C12", width=2)
        self.root.update()
        time.sleep(0.5)

        self.queue.pop(0)
        self.canvas.delete(highlight_rect)
        self.draw_queue()
        self.root.update_idletasks()
        
    def clear_queue(self):
        """Clears the queue and redraws the canvas."""
        self.queue.clear()
        self.draw_queue()
        messagebox.showinfo("Queue Cleared", "The queue has been cleared.")
