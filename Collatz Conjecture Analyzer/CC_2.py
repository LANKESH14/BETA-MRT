import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from statistics import mode, median, mean
import seaborn as sns


def collatz_sequence(n):
    """Generate the Collatz sequence for a given number n."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


def get_statistics(sequence):
    """Calculate statistical measures for a sequence."""
    return {
        'mean': mean(sequence),
        'median': median(sequence),
        'mode': mode(sequence),
        'std_dev': np.std(sequence),
        'variance': np.var(sequence),
        'total_odd': sum(1 for x in sequence if x % 2 != 0),
        'total_even': sum(1 for x in sequence if x % 2 == 0)
    }


def analyze_collatz(n):
    """Enhanced analysis of the Collatz sequence."""
    sequence = collatz_sequence(n)
    stats = get_statistics(sequence)
    steps = len(sequence) - 1
    max_value = max(sequence)
    return sequence, steps, max_value, stats


def visualize_collatz(sequence, num):
    """Enhanced visualization with multiple plots."""
    fig = plt.figure(figsize=(12, 8))
    
    # Main sequence plot
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(sequence, marker="o", color="#8BC6EC", linestyle="-", markerfacecolor="#8BC6EC")
    ax1.set_title(f"Collatz Sequence for {num}", fontsize=12)
    ax1.set_xlabel("Steps")
    ax1.set_ylabel("Values")
    ax1.grid(True)

    # Distribution plot
    ax2 = plt.subplot(2, 1, 2)
    sns.histplot(sequence, ax=ax2, kde=True)
    ax2.set_title("Value Distribution", fontsize=12)
    
    plt.tight_layout()
    return fig


def generate_pattern_analysis(start, end):
    """Generate a comparison table for a range of numbers."""
    data = []
    for i in range(start, end + 1):
        sequence, steps, max_val, stats = analyze_collatz(i)  # Now correctly unpacking 4 values
        data.append((i, steps, max_val))
    return pd.DataFrame(data, columns=["Number", "Steps", "Max Value"])


# GUI Implementation
class CollatzApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Collatz Conjecture Analysis")
        self.root.geometry("1200x800")
        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Analysis Input", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Single Number:").grid(row=0, column=0, padx=5)
        self.number_input = ttk.Entry(input_frame, width=15)
        self.number_input.grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Analyze", command=self.analyze_number).grid(row=0, column=2, padx=5)

        ttk.Label(input_frame, text="Range Analysis:").grid(row=1, column=0, padx=5, pady=5)
        self.start_input = ttk.Entry(input_frame, width=10)
        self.start_input.grid(row=1, column=1, padx=2)
        ttk.Label(input_frame, text="to").grid(row=1, column=2)
        self.end_input = ttk.Entry(input_frame, width=10)
        self.end_input.grid(row=1, column=3, padx=2)
        ttk.Button(input_frame, text="Compare Range", command=self.compare_range).grid(row=1, column=4, padx=5)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="5")
        results_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        # Statistics display
        self.stats_text = tk.Text(results_frame, height=8, width=70, font=('Consolas', 10))
        self.stats_text.grid(row=0, column=0, pady=5, padx=5)

        # Graph area
        self.graph_frame = ttk.Frame(main_frame)
        self.graph_frame.grid(row=2, column=0, columnspan=2, pady=5)

    def analyze_number(self):
        try:
            num = int(self.number_input.get())
            if num <= 0:
                raise ValueError("Please enter a positive integer.")

            sequence, steps, max_val, stats = analyze_collatz(num)

            # Update statistics display
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert(tk.END, f"Analysis for number: {num}\n")
            self.stats_text.insert(tk.END, f"Steps to reach 1: {steps}\n")
            self.stats_text.insert(tk.END, f"Maximum Value: {max_val:,}\n")
            self.stats_text.insert(tk.END, f"Mean: {stats['mean']:.2f}\n")
            self.stats_text.insert(tk.END, f"Median: {stats['median']}\n")
            self.stats_text.insert(tk.END, f"Mode: {stats['mode']}\n")
            self.stats_text.insert(tk.END, f"Standard Deviation: {stats['std_dev']:.2f}\n")
            self.stats_text.insert(tk.END, f"Odd Numbers: {stats['total_odd']}, Even Numbers: {stats['total_even']}\n")

            # Plot the sequence
            fig = visualize_collatz(sequence, num)
            self.show_graph(fig)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def compare_range(self):
        """Compare Collatz behavior across a range of numbers."""
        try:
            start = int(self.start_input.get())
            end = int(self.end_input.get())
            if start <= 0 or end <= 0 or start > end:
                raise ValueError("Enter a valid positive range (start <= end).")

            df = generate_pattern_analysis(start, end)

            # Display the data in a new window
            compare_window = tk.Toplevel(self.root)
            compare_window.title("Collatz Range Comparison")

            tree = ttk.Treeview(compare_window, columns=["Number", "Steps", "Max Value"], show="headings", height=15)
            tree.pack(fill="both", expand=True)

            for col in ["Number", "Steps", "Max Value"]:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")

            for _, row in df.iterrows():
                tree.insert("", tk.END, values=row.tolist())

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_graph(self, fig):
        """Display the graph in the GUI."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CollatzApp(root)
    root.mainloop()
