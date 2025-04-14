import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from collections import Counter


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


def analyze_collatz(n):
    """Analyze the Collatz sequence for a number n."""
    sequence = collatz_sequence(n)
    steps = len(sequence) - 1
    max_value = max(sequence)
    return sequence, steps, max_value


def visualize_collatz(sequence, num):
    """Visualize the Collatz sequence."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(sequence, marker="o", color="#8BC6EC", linestyle="-", markerfacecolor="#8BC6EC")
    ax.set_title(f"Collatz Conjecture for {num}", fontsize=14)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Values")
    ax.grid(color="gray", linestyle="--", linewidth=0.5)
    return fig


def generate_pattern_analysis(start, end):
    """Generate a comparison table for a range of numbers."""
    data = []
    for i in range(start, end + 1):
        _, steps, max_val = analyze_collatz(i)
        data.append((i, steps, max_val))
    return pd.DataFrame(data, columns=["Number", "Steps", "Max Value"])


def find_repeated_max_values(dataframe):
    """Find numbers that have repeated maximum values."""
    max_value_counts = Counter(dataframe["Max Value"])
    repeated_values = {value: count for value, count in max_value_counts.items() if count > 1}
    return repeated_values


# GUI Implementation
class CollatzApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Collatz Conjecture Analysis")
        self.create_widgets()

    def create_widgets(self):
        # Input frame
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Enter a number:").grid(row=0, column=0, padx=5, pady=5)
        self.number_input = tk.Entry(frame, width=10)
        self.number_input.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame, text="Analyze", command=self.analyze_number).grid(row=0, column=2, padx=5, pady=5)

        # Range input for pattern analysis
        tk.Label(frame, text="Range (Start - End):").grid(row=1, column=0, padx=5, pady=5)
        self.start_input = tk.Entry(frame, width=5)
        self.start_input.grid(row=1, column=1, padx=2, pady=5)
        self.end_input = tk.Entry(frame, width=5)
        self.end_input.grid(row=1, column=2, padx=2, pady=5)

        tk.Button(frame, text="Compare", command=self.compare_range).grid(row=1, column=3, padx=5, pady=5)

        # Results frame
        self.results_text = tk.Text(self.root, height=5, width=60, state="disabled")
        self.results_text.pack(pady=10)

        # Graph area
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack()

    def analyze_number(self):
        """Analyze the Collatz sequence for a single number."""
        try:
            num = int(self.number_input.get())
            if num <= 0:
                raise ValueError("Enter a positive integer.")

            sequence, steps, max_val = analyze_collatz(num)

            # Display results
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                tk.END, f"Number: {num}\nSteps to reach 1: {steps}\nMaximum Value: {max_val}\nSequence: {sequence}\n"
            )
            self.results_text.config(state="disabled")

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

            # Find repeated max values
            repeated_values = find_repeated_max_values(df)

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

            # Display repeated max values in a summary
            summary_text = tk.Text(compare_window, height=5, width=60, state="normal")
            summary_text.pack(pady=10)
            summary_text.insert(tk.END, "Repeated Max Values:\n")
            for value, count in repeated_values.items():
                summary_text.insert(tk.END, f"Value: {value}, Count: {count}\n")
            summary_text.config(state="disabled")

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
