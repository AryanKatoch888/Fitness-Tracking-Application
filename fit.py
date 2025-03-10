import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class FitnessApp:
    def __init__(self, root):
        # self.root = root
        self.root = tk.Tk()
        self.root.title("Enhanced Fitness Data Tracker")
        self.root.geometry("900x700")  # Set a fixed window size

        # Initialize an empty DataFrame for fitness data
        self.data_file = 'fitness.csv'
        self.data = pd.DataFrame(columns=['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)'])

        # Setup GUI Layout
        self.setup_gui()

    # ---------------- Styling ---------------- #
    def setup_styles(self):
        """Set up styling for widgets."""
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
        style.configure("Success.TLabel", foreground="green", font=("Helvetica", 10, "bold"))
        style.configure("Error.TLabel", foreground="red", font=("Helvetica", 10, "bold"))

    # ---------------- GUI Layout ---------------- #
    def setup_gui(self):
        """Set up the main GUI layout."""
        self.setup_styles()

        # Frames for Layout
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        tree_frame = ttk.Frame(self.root, padding=10)
        tree_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Input Fields
        ttk.Label(input_frame, text="Serial No.").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_serial = ttk.Entry(input_frame, width=20)
        self.entry_serial.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Day").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_day = ttk.Entry(input_frame, width=20)
        self.entry_day.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Weight (kg)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_weight = ttk.Entry(input_frame, width=20)
        self.entry_weight.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Exercise Split").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_exercise = ttk.Entry(input_frame, width=20)
        self.entry_exercise.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Diet (Calories)").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_diet = ttk.Entry(input_frame, width=20)
        self.entry_diet.grid(row=4, column=1, padx=5, pady=5)

        # Search Bar
        ttk.Label(input_frame, text="Search:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(input_frame, width=20)
        self.search_entry.grid(row=5, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(button_frame, text="Add Data", command=self.add_data).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Search", command=self.search_data).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Row", command=self.delete_row).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Plot Data", command=self.plot_data).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Save Data", command=self.save_data).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(button_frame, text="Load Data", command=self.load_data).grid(row=0, column=5, padx=5, pady=5)

        # Message Label
        self.message_label = ttk.Label(self.root, text="", style="Success.TLabel")
        self.message_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Treeview Table
        self.tree = ttk.Treeview(tree_frame, columns=['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)'], show='headings', height=10)
        self.tree.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        # Add column headers to the Treeview
        for col in ['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add a scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=5, sticky="ns")

        # Load Initial Data
        self.load_data()

        # Configure Grid Weights for resizing
        self.root.grid_rowconfigure(2, weight=1)  # Make the Treeview's row expandable
        self.root.grid_columnconfigure(0, weight=1)  # Expand horizontally

    # ---------------- Functions ---------------- #

    def update_status(self, message, success=True):
        """Update status label with a message."""
        style_name = "Success.TLabel" if success else "Error.TLabel"
        self.message_label.config(text=message, style=style_name)

    def add_data(self):
        """Add user input to the DataFrame."""
        serial_no = self.entry_serial.get()
        day = self.entry_day.get()
        weight = self.entry_weight.get()
        exercise_split = self.entry_exercise.get()
        diet = self.entry_diet.get()

        if not serial_no or not day or not weight or not exercise_split or not diet:
            self.update_status("Please fill all fields", success=False)
            return

        try:
            weight = float(weight)
            diet = float(diet)
            new_data = pd.DataFrame([[serial_no, day, weight, exercise_split, diet]],
                                    columns=['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)'])
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.update_table()
            self.update_status(f"Data added successfully! Total Entries: {self.data.shape[0]}", success=True)
        except ValueError:
            self.update_status("Invalid data: Weight and Diet must be numbers.", success=False)

    def delete_row(self):
        """Delete selected row from the Treeview and DataFrame."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.update_status("No row selected to delete.", success=False)
            return

        try:
            # Get the selected row values
            row_values = self.tree.item(selected_item, 'values')
            serial_no_to_delete = row_values[0]

            # Remove from DataFrame
            self.data = self.data[self.data['Serial_No'] != serial_no_to_delete].reset_index(drop=True)

            # Remove from Treeview
            self.tree.delete(selected_item)

            self.update_status("Row deleted successfully.", success=True)
        except Exception as e:
            self.update_status(f"Error deleting row: {e}", success=False)

    def search_data(self):
        """Filter the Treeview based on the search query."""
        query = self.search_entry.get().lower()
        if not query:
            self.update_table()
            self.update_status("Search cleared. Showing all entries.", success=True)
            return

        filtered_data = self.data[
            self.data.apply(lambda row: query in str(row['Serial_No']).lower()
                                        or query in str(row['Day']).lower()
                                        or query in str(row['Weight (kg)']).lower()
                                        or query in str(row['Exercise_Split']).lower()
                                        or query in str(row['Diet (Calories)']).lower(), axis=1)
        ]

        if filtered_data.empty:
            self.update_status("No matching records found.", success=False)
            self.tree.delete(*self.tree.get_children())  # Clear Treeview
        else:
            self.tree.delete(*self.tree.get_children())  # Clear Treeview
            for _, row in filtered_data.iterrows():
                reordered_row = [row['Serial_No'], row['Day'], row['Weight (kg)'], row['Exercise_Split'], row['Diet (Calories)']]
            self.tree.insert("", "end", values=reordered_row)
            self.update_status(f"Showing {len(filtered_data)} matching records.", success=True)

    def plot_data(self):
        """Enhanced line plot for weight and diet trends."""
        if self.data.empty:
            self.update_status("No data to plot", success=False)
            return

        plt.figure(figsize=(10, 6))

        # Line Plots
        plt.plot(self.data.index, self.data['Weight (kg)'], marker='o', label='Weight (kg)', color='#1f77b4', linewidth=2)
        plt.plot(self.data.index, self.data['Diet (Calories)'], marker='x', label='Diet (Calories)', color='#ff7f0e', linewidth=2)

        # Adding Annotations for Min/Max
        min_weight_idx = self.data['Weight (kg)'].idxmin()
        max_weight_idx = self.data['Weight (kg)'].idxmax()
        plt.annotate(f"Min: {self.data['Weight (kg)'][min_weight_idx]}",
                     (min_weight_idx, self.data['Weight (kg)'][min_weight_idx]),
                     textcoords="offset points", xytext=(-10, 10), ha='center', fontsize=10, color="blue")
        plt.annotate(f"Max: {self.data['Weight (kg)'][max_weight_idx]}",
                     (max_weight_idx, self.data['Weight (kg)'][max_weight_idx]),
                     textcoords="offset points", xytext=(-10, -15), ha='center', fontsize=10, color="red")

        # Title and Labels
        plt.title(f"Fitness Trends ({len(self.data)} Entries)", fontsize=16, fontweight='bold')
        plt.xlabel('Index', fontsize=12)
        plt.ylabel('Values', fontsize=12)

        # Grid and Legend
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend(fontsize=12, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

        # Display Plot
        plt.tight_layout()
        plt.show()

    def save_data(self):
        """Save data to a CSV file."""
        if self.data.empty:
            self.update_status("No data to save", success=False)
            return

        self.data.to_csv(self.data_file, index=False)
        self.update_status("Data saved successfully!", success=True)

    def load_data(self):
        """Load data from a CSV file."""
        try:
            self.data = pd.read_csv(self.data_file)
            self.update_table()
            self.update_status(f"Data loaded successfully! Total Entries: {self.data.shape[0]}", success=True)
        except FileNotFoundError:
            self.update_status("No saved data found", success=False)

    def update_table(self):
        """Update the Treeview table."""
        self.tree.delete(*self.tree.get_children())  # Clear existing rows
        for _, row in self.data.iterrows():
            reordered_row = [row['Serial_No'], row['Day'], row['Weight (kg)'], row['Exercise_Split'], row['Diet (Calories)']]
            self.tree.insert("", "end", values=reordered_row)


