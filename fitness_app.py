import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data_file = 'fitness.csv'

# Initialize the main window
root = tk.Tk()
root.title("Fitness Dashboard with Dynamic Charts")
root.geometry("1200x900")  # Larger window size
root.configure(bg="#f9f9f9")  # Light background for aesthetics

# Initialize an empty DataFrame for fitness data
data = pd.DataFrame(columns=['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)'])

# ---------------- Styling ---------------- #

style = ttk.Style()
style.theme_use("clam")  # Modern theme
style.configure("TButton", font=("Helvetica", 10, "bold"), padding=10, background="#007BFF", foreground="white")
style.map("TButton", background=[("active", "#0056b3")])  # Button hover color
style.configure("TLabel", font=("Helvetica", 10, "bold"))
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#007BFF", foreground="white")
style.configure("Treeview", font=("Helvetica", 9), rowheight=25, background="white", fieldbackground="white")
style.configure("Summary.TLabel", font=("Helvetica", 14, "bold"), background="#e8f4fc", padding=10)

# ---------------- Functions ---------------- #

# Styling
style.configure("Success.TLabel", foreground="green", font=("Helvetica", 12, "bold"))
style.configure("Error.TLabel", foreground="red", font=("Helvetica", 12, "bold"))

def update_status(message, success=True):
    """Update status label with a message."""
    style_name = "Success.TLabel" if success else "Error.TLabel"
    message_label.config(text=message, style=style_name)

# Message Label Initialization
message_label = ttk.Label(root, text="", style="Success.TLabel", font=("Helvetica", 12))
message_label.grid(row=5, column=0, padx=10, pady=10)


def add_data():
    """Add user input to the DataFrame."""
    global data
    serial_no = entry_serial.get()
    day = entry_day.get()
    weight = entry_weight.get()
    exercise_split = entry_exercise.get()
    diet = entry_diet.get()

    if not serial_no or not day or not weight or not exercise_split or not diet:
        update_status("Please fill all fields", success=False)
        return

    try:
        weight = float(weight)
        diet = float(diet)
        new_data = pd.DataFrame([[serial_no, day, weight, exercise_split, diet]],
                                columns=['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)'])
        data = pd.concat([data, new_data], ignore_index=True)
        update_table()
        update_dashboard_metrics()
        update_chart()  # Update the chart dynamically
        update_status(f"Data added successfully! Total Entries: {data.shape[0]}", success=True)
    except ValueError:
        update_status("Invalid data: Weight and Diet must be numbers.", success=False)

def delete_row():
    """Delete selected row from the Treeview and DataFrame."""
    global data
    selected_item = tree.selection()
    if not selected_item:
        update_status("No row selected to delete.", success=False)
        return

    try:
        # Get the selected row values
        row_values = tree.item(selected_item, 'values')
        serial_no_to_delete = row_values[0]

        # Remove from DataFrame
        data = data[data['Serial_No'] != serial_no_to_delete].reset_index(drop=True)

        # Remove from Treeview
        tree.delete(selected_item)
        update_dashboard_metrics()
        update_chart()  # Update the chart dynamically
        update_status("Row deleted successfully.", success=True)
    except Exception as e:
        update_status(f"Error deleting row: {e}", success=False)

def load_data():
    """Load data from a CSV file."""
    global data
    try:
        data = pd.read_csv(data_file)
        update_table()
        update_dashboard_metrics()
        update_chart()  # Update the chart dynamically
        update_status(f"Data loaded successfully! Total Entries: {data.shape[0]}", success=True)
    except FileNotFoundError:
        update_status("No saved data found.", success=False)

def save_data():
    """Save data to a CSV file."""
    if data.empty:
        update_status("No data to save", success=False)
        return

    data.to_csv(data_file, index=False)
    update_status("Data saved successfully!", success=True)

def update_table():
    """Update the Treeview table."""
    tree.delete(*tree.get_children())  # Clear existing rows
    for _, row in data.iterrows():
        reordered_row = [row['Serial_No'], row['Day'], row['Weight (kg)'], row['Exercise_Split'], row['Diet (Calories)']]
        tree.insert("", "end", values=reordered_row)

def update_dashboard_metrics():
    """Update dashboard summary metrics."""
    if data.empty:
        total_entries_label.config(text="Total Entries: 0")
        avg_weight_label.config(text="Average Weight: N/A")
        avg_calories_label.config(text="Average Calories: N/A")
        return

    total_entries_label.config(text=f"Total Entries: {len(data)}")
    avg_weight_label.config(text=f"Average Weight: {data['Weight (kg)'].mean():.2f} kg")
    avg_calories_label.config(text=f"Average Calories: {data['Diet (Calories)'].mean():.2f} kcal")

# Dynamic Chart
def update_chart():
    """Update the dynamic chart with the latest data."""
    for widget in chart_frame.winfo_children():
        widget.destroy()  # Clear the previous chart

    if data.empty:
        no_data_label = ttk.Label(chart_frame, text="No data to display.", font=("Helvetica", 14, "bold"))
        no_data_label.pack()
        return

    # Create Matplotlib Figure
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data.index, data['Weight (kg)'], marker='o', label='Weight (kg)', color='blue')
    ax.plot(data.index, data['Diet (Calories)'], marker='x', label='Diet (Calories)', color='orange')
    ax.set_title("Dynamic Fitness Trends", fontsize=16, fontweight="bold")
    ax.set_xlabel("Entry Index", fontsize=12)
    ax.set_ylabel("Values", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Embed Matplotlib Figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ---------------- Dashboard Layout ---------------- #

# Dashboard Summary
dashboard_frame = ttk.Frame(root, padding=10, style="Summary.TFrame")
dashboard_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

total_entries_label = ttk.Label(dashboard_frame, text="Total Entries: 0", style="Summary.TLabel")
total_entries_label.grid(row=0, column=0, padx=20, pady=5)

avg_weight_label = ttk.Label(dashboard_frame, text="Average Weight: N/A", style="Summary.TLabel")
avg_weight_label.grid(row=0, column=1, padx=20, pady=5)

avg_calories_label = ttk.Label(dashboard_frame, text="Average Calories: N/A", style="Summary.TLabel")
avg_calories_label.grid(row=0, column=2, padx=20, pady=5)

# Data Table
tree_frame = ttk.Frame(root, padding=10)
tree_frame.grid(row=1, column=0, sticky="nsew", pady=10)

tree = ttk.Treeview(tree_frame, columns=['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)'], show='headings', height=10)
tree.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

# Add column headers to the Treeview
for col in ['Serial_No', 'Day', 'Weight (kg)', 'Exercise_Split', 'Diet (Calories)']:
    tree.heading(col, text=col)
    tree.column(col, width=150)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=6, sticky="ns")

# Buttons
button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=2, column=0, pady=10)

ttk.Button(button_frame, text="Add Data", command=add_data).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Delete Row", command=delete_row).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Plot Data", command=update_chart).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Save Data", command=save_data).grid(row=0, column=3, padx=5)
ttk.Button(button_frame, text="Load Data", command=load_data).grid(row=0, column=4, padx=5)

# Dynamic Chart Frame
chart_frame = ttk.Frame(root, padding=10)
chart_frame.grid(row=3, column=0, sticky="nsew", pady=10)
chart_frame.columnconfigure(0, weight=1)
chart_frame.rowconfigure(0, weight=1)

# Input Form
input_frame = ttk.Frame(root, padding=10)
input_frame.grid(row=4, column=0, sticky="ew", pady=10)

# Input Fields
ttk.Label(input_frame, text="Serial No.").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_serial = ttk.Entry(input_frame, width=20)
entry_serial.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Day").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_day = ttk.Entry(input_frame, width=20)
entry_day.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Weight (kg)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_weight = ttk.Entry(input_frame, width=20)
entry_weight.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Exercise Split").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_exercise = ttk.Entry(input_frame, width=20)
entry_exercise.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Diet (Calories)").grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_diet = ttk.Entry(input_frame, width=20)
entry_diet.grid(row=4, column=1, padx=5, pady=5)

# Message Label
message_label = ttk.Label(root, text="", font=("Helvetica", 12))
message_label.grid(row=5, column=0, padx=10, pady=10)

# Grid Configuration for Resizing
root.grid_rowconfigure(1, weight=1)  # Make the data table expandable
root.grid_rowconfigure(3, weight=1)  # Make the chart frame expandable
root.grid_columnconfigure(0, weight=1)  # Expand horizontally

# Load Initial Data
load_data()
update_dashboard_metrics()
update_chart()

# Run the GUI Loop
root.mainloop()

