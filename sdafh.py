import tkinter as tk
from tkinter import ttk, Frame

# Global variable to track the current step
current_step = 0
steps = []  # Store frames for each step


# Function to handle Next Button click
def next_step():
    global current_step
    if current_step < len(steps) - 1:
        current_step += 1
        show_step()


# Function to handle Previous Button click
def previous_step():
    global current_step
    if current_step > 0:
        current_step -= 1
        show_step()


# Function to display the current step
def show_step():
    global current_step
    # Destroy the previous frame if exists
    for widget in root.winfo_children():
        widget.destroy()
    # Create and pack the current step frame
    frame = steps[current_step]()
    frame.pack(fill="both", expand=True)


# Function to create a generic TreeView frame
def create_treeview_frame(title, col_defs):
    def frame_func():
        frame = tk.Frame(root)
        # Title
        label = tk.Label(frame, text=title, font=("Arial", 16))
        label.pack(pady=10)

        # Treeview container (Frame for better layout flexibility)
        tsFrame = Frame(frame, bg='white')
        tsFrame.pack(fill="both", expand=True, padx=20, pady=10)

        # Extract column names from col_defs
        columns = list(col_defs.keys())

        # Create TreeView for the step
        table = ttk.Treeview(tsFrame, columns=columns, show='headings')
        table.pack(fill="both", expand=True)

        # Define columns
        for col, width in col_defs.items():
            table.heading(col, text=col)  # Set the column heading
            table.column(col, width=width)  # Set the column width

        # Navigation buttons
        nav_frame = tk.Frame(frame)
        nav_frame.pack(pady=10)

        if current_step > 0:  # Show Previous button if not on the first step
            prev_button = ttk.Button(nav_frame, text="Previous", command=previous_step)
            prev_button.pack(side="left", padx=5)

        if current_step < len(steps) - 1:  # Show Next button if not on the last step
            next_button = ttk.Button(nav_frame, text="Next", command=next_step)
            next_button.pack(side="right", padx=5)

        if current_step == len(steps) - 1:  # Show Submit button on the last step
            submit_button = ttk.Button(nav_frame, text="Submit", command=root.quit)
            submit_button.pack(side="right", padx=5)

        return frame

    return frame_func


# Define column definitions (reused across all steps)
columns = {
    "Course Number": 120,
    "Subject": 200,
    "Units": 100,
    "Rating": 100,
    "Final Grade": 120,
    "Status": 100,
}

# List of steps (titles for each and their associated TreeView column definitions)
step_definitions = [
    ("1st Year 1st Semester", columns),
    ("1st Year 2nd Semester", columns),
    ("2nd Year 1st Semester", columns),
    ("2nd Year 2nd Semester", columns),
    ("3rd Year 1st Semester", columns),
    ("3rd Year 2nd Semester", columns),
    ("4th Year 1st Semester", columns),
    ("4th Year 2nd Semester", columns),
]

# Generate step functions dynamically based on step definitions
steps = [create_treeview_frame(title, col_defs) for title, col_defs in step_definitions]

# Create the main window (root)
root = tk.Tk()
root.title("Multi-Step TreeView Form")
root.geometry("800x600")

# Display the initial step
show_step()

# Run the Tkinter main loop
root.mainloop()