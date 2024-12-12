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

    # Create the current step frame
    frame = steps[current_step]()
    frame.pack()


# Step 1: Student Number
def create_step1():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="1st Year 1st Semester")
    label.pack(pady=10)
    tsFrame = Frame(frame, bg='white')
    tsFrame.place(x=26, y=100, width=1080, height=530)
    first_year_1st_sem_table = ttk.Treeview(tsFrame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    first_year_1st_sem_table.place(x=2, y=2, width=1060, height=526)

    first_year_1st_sem_table.column('Course Number', width=30)
    first_year_1st_sem_table.column('Subject', width=380)
    first_year_1st_sem_table.column('Units', width=30)
    first_year_1st_sem_table.column('Rating', width=80)
    first_year_1st_sem_table.column('Final Grade', width=80)
    first_year_1st_sem_table.column('Status', width=60)

    first_year_1st_sem_table.heading('Course Number', text='Course No.')
    first_year_1st_sem_table.heading('Subject', text='Subject')
    first_year_1st_sem_table.heading('Units', text='Units')
    first_year_1st_sem_table.heading('Rating', text='Ratings')
    first_year_1st_sem_table.heading('Final Grade', text='Final Grade')
    first_year_1st_sem_table.heading('Status', text='Status')
    first_year_1st_sem_table.config(show='headings')

    # Next Button
    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 2: Password
def create_step2():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="1st Year 2nd Semester")
    label.pack(pady=10)
    first_year_2nd_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    first_year_2nd_sem_table.place(x=2, y=528, width=1060, height=526)
    first_year_2nd_sem_table.column('Course Number', width=30)
    first_year_2nd_sem_table.column('Subject', width=380)
    first_year_2nd_sem_table.column('Units', width=30)
    first_year_2nd_sem_table.column('Rating', width=80)
    first_year_2nd_sem_table.column('Final Grade', width=80)
    first_year_2nd_sem_table.column('Status', width=60)

    first_year_2nd_sem_table.heading('Course Number', text='Course No.')
    first_year_2nd_sem_table.heading('Subject', text='Subject')
    first_year_2nd_sem_table.heading('Units', text='Units')
    first_year_2nd_sem_table.heading('Rating', text='Ratings')
    first_year_2nd_sem_table.heading('Final Grade', text='Final Grade')
    first_year_2nd_sem_table.heading('Status', text='Status')
    first_year_2nd_sem_table.config(show='headings')

    # Previous and Next Buttons
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 3: Full Name
def create_step3():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="2nd Year 1st Semester")
    label.pack(pady=10)

    second_year_1st_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    second_year_1st_sem_table.place(x=2, y=1054, width=1060, height=526)
    second_year_1st_sem_table.column('Course Number', width=30)
    second_year_1st_sem_table.column('Subject', width=380)
    second_year_1st_sem_table.column('Units', width=30)
    second_year_1st_sem_table.column('Rating', width=80)
    second_year_1st_sem_table.column('Final Grade', width=80)
    second_year_1st_sem_table.column('Status', width=60)

    second_year_1st_sem_table.heading('Course Number', text='Course No.')
    second_year_1st_sem_table.heading('Subject', text='Subject')
    second_year_1st_sem_table.heading('Units', text='Units')
    second_year_1st_sem_table.heading('Rating', text='Ratings')
    second_year_1st_sem_table.heading('Final Grade', text='Final Grade')
    second_year_1st_sem_table.heading('Status', text='Status')
    second_year_1st_sem_table.config(show='headings')
    # Previous and Next Buttons
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 4: Email Address
def create_step4():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="2nd Year 2nd Semester")
    label.pack(pady=10)

    second_year_2nd_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    second_year_2nd_sem_table.place(x=2, y=1580, width=1060, height=526)
    second_year_2nd_sem_table.column('Course Number', width=30)
    second_year_2nd_sem_table.column('Subject', width=380)
    second_year_2nd_sem_table.column('Units', width=30)
    second_year_2nd_sem_table.column('Rating', width=80)
    second_year_2nd_sem_table.column('Final Grade', width=80)
    second_year_2nd_sem_table.column('Status', width=60)

    second_year_2nd_sem_table.heading('Course Number', text='Course No.')
    second_year_2nd_sem_table.heading('Subject', text='Subject')
    second_year_2nd_sem_table.heading('Units', text='Units')
    second_year_2nd_sem_table.heading('Rating', text='Ratings')
    second_year_2nd_sem_table.heading('Final Grade', text='Final Grade')
    second_year_2nd_sem_table.heading('Status', text='Status')
    second_year_2nd_sem_table.config(show='headings')

    # Previous and Next Buttons
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 5: Phone Number
def create_step5():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="3rd Year 1st Semester")
    label.pack(pady=10)

    third_year_1st_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    third_year_1st_sem_table.place(x=2, y=2106, width=1060, height=526)
    third_year_1st_sem_table.column('Course Number', width=30)
    third_year_1st_sem_table.column('Subject', width=380)
    third_year_1st_sem_table.column('Units', width=30)
    third_year_1st_sem_table.column('Rating', width=80)
    third_year_1st_sem_table.column('Final Grade', width=80)
    third_year_1st_sem_table.column('Status', width=60)

    third_year_1st_sem_table.heading('Course Number', text='Course No.')
    third_year_1st_sem_table.heading('Subject', text='Subject')
    third_year_1st_sem_table.heading('Units', text='Units')
    third_year_1st_sem_table.heading('Rating', text='Ratings')
    third_year_1st_sem_table.heading('Final Grade', text='Final Grade')
    third_year_1st_sem_table.heading('Status', text='Status')
    third_year_1st_sem_table.config(show='headings')

    # Previous and Next Buttons
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 6: Address
def create_step6():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="3rd Year 2nd Semester")
    label.pack(pady=10)

    third_year_2nd_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    third_year_2nd_sem_table.place(x=2, y=2632, width=1060, height=526)
    third_year_2nd_sem_table.column('Course Number', width=30)
    third_year_2nd_sem_table.column('Subject', width=380)
    third_year_2nd_sem_table.column('Units', width=30)
    third_year_2nd_sem_table.column('Rating', width=80)
    third_year_2nd_sem_table.column('Final Grade', width=80)
    third_year_2nd_sem_table.column('Status', width=60)

    third_year_2nd_sem_table.heading('Course Number', text='Course No.')
    third_year_2nd_sem_table.heading('Subject', text='Subject')
    third_year_2nd_sem_table.heading('Units', text='Units')
    third_year_2nd_sem_table.heading('Rating', text='Ratings')
    third_year_2nd_sem_table.heading('Final Grade', text='Final Grade')
    third_year_2nd_sem_table.heading('Status', text='Status')
    third_year_2nd_sem_table.config(show='headings')

    # Previous and Next Buttons
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 7: Additional Info
def create_step7():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="4th Year 1st Semester")
    label.pack(pady=10)

    fourth_year_1st_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    fourth_year_1st_sem_table.place(x=2, y=3158, width=1060, height=526)
    fourth_year_1st_sem_table.column('Course Number', width=30)
    fourth_year_1st_sem_table.column('Subject', width=380)
    fourth_year_1st_sem_table.column('Units', width=30)
    fourth_year_1st_sem_table.column('Rating', width=80)
    fourth_year_1st_sem_table.column('Final Grade', width=80)
    fourth_year_1st_sem_table.column('Status', width=60)

    fourth_year_1st_sem_table.heading('Course Number', text='Course No.')
    fourth_year_1st_sem_table.heading('Subject', text='Subject')
    fourth_year_1st_sem_table.heading('Units', text='Units')
    fourth_year_1st_sem_table.heading('Rating', text='Ratings')
    fourth_year_1st_sem_table.heading('Final Grade', text='Final Grade')
    fourth_year_1st_sem_table.heading('Status', text='Status')
    fourth_year_1st_sem_table.config(show='headings')

    # Previous and Next Buttons
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    next_button = ttk.Button(frame, text="Next", command=next_step)
    next_button.pack(side="right", padx=10, pady=10)

    return frame


# Step 8: Confirmation (Final Step)
def create_step8():
    frame = tk.Frame(root)
    label = tk.Label(frame, text="4th Year 2nd Semester")
    label.pack(pady=10)

    fourth_year_2nd_sem_table = ttk.Treeview(frame, columns=(
    'Course Number', 'Subject', 'Units', 'Rating', 'Final Grade', 'Status'))
    fourth_year_2nd_sem_table.place(x=2, y=3684, width=1060, height=526)
    fourth_year_2nd_sem_table.column('Course Number', width=30)
    fourth_year_2nd_sem_table.column('Subject', width=380)
    fourth_year_2nd_sem_table.column('Units', width=30)
    fourth_year_2nd_sem_table.column('Rating', width=80)
    fourth_year_2nd_sem_table.column('Final Grade', width=80)
    fourth_year_2nd_sem_table.column('Status', width=60)

    fourth_year_2nd_sem_table.heading('Course Number', text='Course No.')
    fourth_year_2nd_sem_table.heading('Subject', text='Subject')
    fourth_year_2nd_sem_table.heading('Units', text='Units')
    fourth_year_2nd_sem_table.heading('Rating', text='Ratings')
    fourth_year_2nd_sem_table.heading('Final Grade', text='Final Grade')
    fourth_year_2nd_sem_table.heading('Status', text='Status')
    fourth_year_2nd_sem_table.config(show='headings')

    submit_button = ttk.Button(frame, text="Submit", command=root.quit)
    submit_button.pack(pady=10)

    # Previous Button
    previous_button = ttk.Button(frame, text="Previous", command=previous_step)
    previous_button.pack(side="left", padx=10, pady=10)

    return frame


# Create the main window (root)
root = tk.Tk()
root.title("Multi-Step Form")

# Store the steps in the global list
steps = [
    create_step1,
    create_step2,
    create_step3,
    create_step4,
    create_step5,
    create_step6,
    create_step7,
    create_step8
]

# Display the initial step
show_step()

# Run the Tkinter main loop
root.mainloop()
