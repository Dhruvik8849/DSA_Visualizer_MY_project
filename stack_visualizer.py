import tkinter as tk
from tkinter import ttk, messagebox
import time

class StackVisualizer:
    """
    A class to visualize the Stack data structure using tkinter.
    """
    def __init__(self, root):
        """
        Initializes the Stack Visualizer GUI.
        Args:
            root (tk.Toplevel): The parent window for this visualizer.
        """
        self.root = root
        self.stack = []
        self.max_size = 8  # Max elements in the stack for visualization purposes

        # --- UI Setup ---
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(side="top", fill="x")
        
        self.canvas_frame = ttk.Frame(self.root, padding="10")
        self.canvas_frame.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self.canvas_frame, bg="#ECF0F1", width=800, height=500)
        self.canvas.pack(expand=True, fill="both")

        # --- Controls ---
        ttk.Label(self.control_frame, text="Value:").pack(side="left", padx=5)
        self.entry = ttk.Entry(self.control_frame, width=10)
        self.entry.pack(side="left", padx=5)

        self.push_button = ttk.Button(self.control_frame, text="Push", command=self.push)
        self.push_button.pack(side="left", padx=5)

        self.pop_button = ttk.Button(self.control_frame, text="Pop", command=self.pop)
        self.pop_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(self.control_frame, text="Clear", command=self.clear_stack)
        self.clear_button.pack(side="left", padx=5)

        self.draw_stack()

    def draw_stack(self):
        """
        Draws the current state of the stack on the canvas.
        """
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        box_width = 80
        box_height = 40
        x_center = canvas_width / 2
        
        # Draw stack base
        self.canvas.create_line(x_center - box_width, canvas_height - 50, x_center + box_width, canvas_height - 50, width=3, fill="#34495E")

        if not self.stack:
            self.canvas.create_text(x_center, canvas_height - 80, text="Stack is empty", font=("Helvetica", 14), fill="gray")
        else:
            for i, value in enumerate(self.stack):
                y = canvas_height - 50 - (i + 1) * box_height
                x1 = x_center - box_width / 2
                y1 = y
                x2 = x_center + box_width / 2
                y2 = y + box_height
                
                # Draw the stack element box
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#3498DB", outline="#2980B9", width=2)
                # Draw the value inside the box
                self.canvas.create_text(x_center, y + box_height / 2, text=str(value), font=("Helvetica", 14, "bold"), fill="white")
        
        # Draw "Top" pointer
        if self.stack:
             top_y = canvas_height - 50 - len(self.stack) * box_height
             self.canvas.create_text(x_center + box_width, top_y + box_height / 2, text="<-- Top", font=("Helvetica", 12, "bold"), fill="#E74C3C")


    def push(self):
        """
        Handles the push operation.
        """
        value = self.entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value to push.")
            return
        
        if len(self.stack) >= self.max_size:
            messagebox.showwarning("Stack Overflow", f"Stack is full (max size: {self.max_size}).")
            return

        self.stack.append(value)
        self.entry.delete(0, tk.END)
        self.animate_push()

    def animate_push(self):
        """
        Animates the push operation.
        """
        self.draw_stack() # Redraw to show the new element
        self.root.update_idletasks()

    def pop(self):
        """
        Handles the pop operation.
        """
        if not self.stack:
            messagebox.showinfo("Stack Underflow", "Stack is empty, cannot pop.")
            return
        
        self.animate_pop()

    def animate_pop(self):
        """
        Animates the pop operation.
        """
        # Highlight the top element before removing
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        box_width = 80
        box_height = 40
        x_center = canvas_width / 2
        
        top_y = canvas_height - 50 - len(self.stack) * box_height
        x1 = x_center - box_width / 2
        y1 = top_y
        x2 = x_center + box_width / 2
        y2 = top_y + box_height
        
        # Highlight rectangle
        highlight_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#E74C3C", outline="#C0392B", width=2)
        self.root.update()
        time.sleep(0.5)

        self.stack.pop()
        self.canvas.delete(highlight_rect)
        self.draw_stack()
        self.root.update_idletasks()
        
    def clear_stack(self):
        """Clears the stack and redraws the canvas."""
        self.stack.clear()
        self.draw_stack()
        messagebox.showinfo("Stack Cleared", "The stack has been cleared.")

