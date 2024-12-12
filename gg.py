import sqlite3
import tkinter as tk
import ttkthemes
from tkinter import ttk, Frame, simpledialog, messagebox
from PIL import Image, ImageTk

def fetch_courses():
    # Connect to the SQLite database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Execute a query to fetch course names
    cursor.execute("SELECT course_name FROM courses")
    courses = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    # Return the list of course names
    return courses

def fetch_user_credentials(student_number, password):
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Query the students table to fetch the student data by student_number and password
    cursor.execute('SELECT name, student_number FROM students WHERE student_number = ? AND password = ?', (student_number, password))
    result = cursor.fetchone()  # Fetch the first result

    # Close the database connection
    conn.close()

    if result:
        return result  # Returns a tuple containing the student data (student_number, name, password, etc.)
    else:
        return None  # No matching user found

def fetch_user_credentials2(registrar_number, password):
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Query the registrars table to fetch the registrar data by registrar_number and password
    cursor.execute('SELECT * FROM registrars WHERE registrar_number = ? AND password = ?', (registrar_number, password))
    result = cursor.fetchone()  # Fetch the first result

    # Close the database connection
    conn.close()

    if result:
        return result  # Returns a tuple containing the registrar data (registrar_number, name, password, etc.)
    else:
        return None  # No matching user found

def populate_treeview_from_db(tree):
    # Connect to the database
    connection = sqlite3.connect('my_database.db')  # Adjust as necessary
    cursor = connection.cursor()

    try:
        # Fetch data
        cursor.execute("SELECT course_number, subject_name, units, rating, final_grade, status FROM student")
        data = cursor.fetchall()

        # Clear existing data in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Insert data into the Treeview
        for row in data:
            tree.insert('', 'end', values=row)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        connection.close()

def insert_user_data_st(name, student_number, course, mobile_number, email_address, password):
    try:
        conn = sqlite3.connect('my_database.db')

        # Insert the data into the students table
        data_insert_query='''INSERT INTO students (name, student_number, course, mobile_number, email_address, password) VALUES (?, ?, ?, ?, ?, ?)'''
        data_insert_tuple=(name, student_number, course, mobile_number, email_address, password)
        cursor = conn.cursor()
        conn.execute(data_insert_query, data_insert_tuple)
        conn.commit()  # Commit the changes

        print(f"Data inserted successfully: {name}, {student_number}, {course}, {mobile_number}, {email_address}")
    except sqlite3.IntegrityError:
        print(f"Error: Student number {student_number} already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Function to handle the sign-up
def sign_up_st():
    student_number = sn_entry.get()
    name = username_entry3.get()
    course = cs_combo.get()
    mobile_number = mn_entry.get()
    email_address = ea_entry.get()
    password = pass_entry.get()

    # Check if all fields are filled
    if not student_number or not name or not course or not mobile_number or not email_address or not password:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        # Call the function with all the necessary arguments
        insert_user_data_st(name, student_number, course, mobile_number, email_address, password)
        messagebox.showinfo("Success", "Sign-Up Successful!")
        showSL2()  # Assuming this is your function to show the next screen
        clear_form()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This student number is already taken.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to clear the form fields after submission
def clear_form():
    sn_entry.delete(0, tk.END)
    username_entry3.delete(0, tk.END)
    cs_combo.delete(0, tk.END)
    mn_entry.delete(0, tk.END)
    ea_entry.delete(0, tk.END)
    mn_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    cpass_entry.delete(0, tk.END)


def insert_user_dataR(registrar_number, name, password):
    try:
        conn = sqlite3.connect('my_database.db')

        # Insert the data into the registrars table
        data_insert_query2 = '''INSERT INTO registrars (registrar_number, name, password) VALUES (?, ?, ?)'''
        data_insert_tuple2 = (registrar_number, name, password)

        conn.execute(data_insert_query2, data_insert_tuple2)
        cursor = conn.cursor()
        conn.commit()  # Commit the changes
        print(f"Data inserted: {registrar_number}, {name}, {password}")
    except sqlite3.IntegrityError:
        print(f"Error: Registrar number {registrar_number} already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Function to handle the sign-up
def sign_up():
    registrar_number = rn_entry.get()
    name = username_entry1.get()
    password = pass_entry1.get()

    # Check if all fields are filled
    if not registrar_number or not name or not password:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        # Insert data into the database
        insert_user_dataR(registrar_number, name, password)
        messagebox.showinfo("Success", "Sign-Up Successful!")
        showRL2()
        clear_form2()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This registrar number is already taken.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to clear the form fields after submission
def clear_form2():
    rn_entry.delete(0, tk.END)
    username_entry1.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    cpass_entry.delete(0, tk.END)

def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(foreground='black')


def on_focusout(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(foreground='grey')



def showSL():
    eS.pack_forget()
    sl.pack(fill="both", expand=True)

def showGES():
    sl.pack_forget()
    eS.pack(fill="both", expand=True)

def showSS():
    sl.pack_forget()
    ss.pack(fill="both", expand=True)

def showSL2():
    ss.pack_forget()
    sl.pack(fill="both", expand=True)

def showST():
    # update_student_table(stdTable)  # Update the student table before showing it
    sl.pack_forget()
    st.pack(fill="both", expand=True)

def login():
    student_number = username_entry.get()  # Assuming you have a field for student number
    password = password_entry.get()

    # Fetch credentials from the database
    user_data = fetch_user_credentials(student_number, password)

    if user_data:
        name, student_number = user_data
        messagebox.showinfo("Access Granted", "Welcome, EECPIANS!")
        showST()  # Proceed to show the student frame
        Std_label.config(text=f"{name}  (# {student_number})")
    else:
        messagebox.showerror("Access Denied", "Invalid entry!")


def showRL():
    eS.pack_forget()
    rl.pack(fill="both", expand=True)

def showGES2():
    rl.pack_forget()
    eS.pack(fill="both", expand=True)

def showRS():
    rl.pack_forget()
    rs.pack(fill="both", expand=True)

def showRL2():
    rs.pack_forget()
    rl.pack(fill="both", expand=True)

def showRE():
    rl.pack_forget()
    re.pack(fill="both", expand=True)

def login2():
    registrar_number = username_entryr.get()  # Assuming you have a field for student number
    password = password_entryr.get()

    # Fetch credentials from the database
    user_data1 = fetch_user_credentials2(registrar_number, password)

    if user_data1:
        messagebox.showinfo("", "Access Granted!")
        showRE()  # Proceed to show the student frame
    else:
        messagebox.showerror("Access Denied", "Invalid entry!")

def SignOutST():
    st.pack_forget()
    eS.pack(fill="both", expand=True)

def SignOutRE():
    re.pack_forget()
    eS.pack(fill="both", expand=True)

# Shared Data Source
student_data = [
    ("CS101", "Mathematics", 4, "A", "90", "Pass"),
    ("ENG101", "English Literature", 3, "B", "85", "Pass"),
    ("BIO101", "Biology", 4, "C", "70", "Pass")
]


# Other function definitions...

def update_student_table(table):
    """Clear and update student table with shared data."""
    for item in table.get_children():
        table.delete(item)
    for item in student_data:
        table.insert('', 'end', values=item)


# Function to edit an item in the Treeview
def edit_item(event, tree):
    region = tree.identify_region(event.x, event.y)
    if region == 'cell':
        column = tree.identify_column(event.x)
        column_index = int(column[1:]) - 1
        selected_item = tree.selection()

        if selected_item:
            for item in selected_item:
                values = tree.item(item, "values")
                if 0 <= column_index < len(values):
                    current_value = values[column_index]
                    new_value = simpledialog.askstring("Edit Value",
                                                       f"Edit value for '{tree.heading(column, 'text')}'\nCurrent: {current_value}")

                    if new_value and new_value.strip():
                        values = list(values)
                        values[column_index] = new_value.strip()
                        tree.item(item, values=values)

                        # Update the shared data
                        item_index = tree.index(item)
                        student_data[item_index] = tuple(values)


ges = ttkthemes.ThemedTk()
ges.state('zoomed')
ges.title("EECP Grade Evaluation System")
ges.set_theme('arc')

#fontframe
eS = tk.Frame(ges)
eS.pack(fill="both", expand=True)
bg=Frame(eS,bg='#E8D8D8')
bg.place(x=0,y=0,width=1320,height=780)
background_image = Image.open("EECP GESYS Front.jpg")
background_image = background_image.resize((1320, 780))
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(bg, image=background_photo)
background_label.place(relwidth=1, relheight=1)

studentButton=ttk.Button(ges,text='STUDENT',command=showSL)
studentButton.place(x=993, y=430, width=150,height=50)
registrarButton=ttk.Button(ges,text='REGISTRAR',command=showRL)
registrarButton.place(x=993, y=490, width=150,height=50)

# Student Log in Frame
sl = tk.Frame(ges)
bgl=Frame(sl,bg='#E8D8D8')
bgl.place(x=0,y=0,width=1320,height=780)
bgI = Image.open("EECP GESYS FrontSS.jpg")
bgI = bgI.resize((1320, 780))
bgP = ImageTk.PhotoImage(bgI)
background_label1 = tk.Label(bgl, image=bgP)
background_label1.place(relwidth=1, relheight=1)

placeholder_text1 = "Student Number"
username_entry = ttk.Entry(sl, foreground='grey')
username_entry.place(x=900, y=420, width=300, height=30)
username_entry.insert(0, placeholder_text1)
username_entry.bind('<FocusIn>', lambda event: on_entry_click(event, username_entry, placeholder_text1))
username_entry.bind('<FocusOut>', lambda event: on_focusout(event, username_entry, placeholder_text1))

placeholder_text2 = "Password"
password_entry = ttk.Entry(sl, foreground='grey', show="*")
password_entry.place(x=900, y=470, width=300, height=30)
password_entry.insert(0, placeholder_text2)
password_entry.bind('<FocusIn>', lambda event: on_entry_click(event, password_entry, placeholder_text2))
password_entry.bind('<FocusOut>', lambda event: on_focusout(event, password_entry, placeholder_text2))

stdlButton=ttk.Button(sl,text='Login', command=login)
stdlButton.place(x=955, y=550, width=200,height=30)
stdSButton=ttk.Button(sl,text='Sign-up', command=showSS)
stdSButton.place(x=983, y=601, width=150,height=50)
studentBackButton=ttk.Button(sl,text='Back', command=showGES)
studentBackButton.place(x=983, y=661, width=150,height=50)

# Student Sign up Frame
ss = tk.Frame(ges)
bg2=Frame(ss,bg='#E8D8D8')
bg2.place(x=0,y=0,width=1320,height=780)
bgI2 = Image.open("signup.jpg")
bgI2 = bgI2.resize((1320, 780))
bgP2 = ImageTk.PhotoImage(bgI2)
background_label2 = tk.Label(bg2, image=bgP2)
background_label2.place(relwidth=1, relheight=1)

midFrame=Frame(ss,bg='grey')
midFrame.place(x=450,y=100,width=350,height=600)
midFrame=Frame(ss,bg='white')
midFrame.place(x=451,y=101,width=348,height=598)

login_titleLabel = tk.Label(ss, text='Sign up here', bg='white', font=('Cambria', 15, 'bold'))
login_titleLabel.place(x=525, y=150, width=200,height=30)

placeholder_text3 = "Student Name"
username_entry3 = ttk.Entry(ss, foreground='grey')
username_entry3.place(x=497,y=200, width=250, height=40)
username_entry3.insert(0, placeholder_text3)
username_entry3.bind('<FocusIn>', lambda event: on_entry_click(event,username_entry3, placeholder_text3))
username_entry3.bind('<FocusOut>', lambda event: on_focusout(event, username_entry3, placeholder_text3))

placeholder_text4 = "Student Number"
sn_entry = ttk.Entry(ss, foreground='grey')
sn_entry.place(x=497,y=260, width=250, height=40)
sn_entry.insert(0, placeholder_text4)
sn_entry.bind('<FocusIn>', lambda event: on_entry_click(event,sn_entry, placeholder_text4))
sn_entry.bind('<FocusOut>', lambda event: on_focusout(event, sn_entry, placeholder_text4))

course_list = fetch_courses()
placeholder_text5 = "Select a course"
cs_combo = ttk.Combobox(ss, foreground='grey', values=course_list)
cs_combo.place(x=497, y=320, width=250, height=40)
cs_combo.insert(0, placeholder_text5)
cs_combo.bind('<FocusIn>', lambda event: on_entry_click(event, cs_combo, placeholder_text5))
cs_combo.bind('<FocusOut>', lambda event: on_focusout(event, cs_combo, placeholder_text5))

placeholder_text6 = "Mobile.No"
mn_entry = ttk.Entry(ss, foreground='grey')
mn_entry.place(x=497,y=380, width=250, height=40)
mn_entry.insert(0, placeholder_text6)
mn_entry.bind('<FocusIn>', lambda event: on_entry_click(event,mn_entry, placeholder_text6))
mn_entry.bind('<FocusOut>', lambda event: on_focusout(event, mn_entry, placeholder_text6))

placeholder_text7 = "Email Address"
ea_entry = ttk.Entry(ss, foreground='grey')
ea_entry.place(x=497,y=440, width=250, height=40)
ea_entry.insert(0, placeholder_text7)
ea_entry.bind('<FocusIn>', lambda event: on_entry_click(event,ea_entry, placeholder_text7))
ea_entry.bind('<FocusOut>', lambda event: on_focusout(event, ea_entry, placeholder_text7))

placeholder_text8 = "Password"
pass_entry = ttk.Entry(ss, foreground='grey', show="*")
pass_entry.place(x=497,y=500, width=250, height=40)
pass_entry.insert(0, placeholder_text8)
pass_entry.bind('<FocusIn>', lambda event: on_entry_click(event,pass_entry, placeholder_text8))
pass_entry.bind('<FocusOut>', lambda event: on_focusout(event, pass_entry, placeholder_text8))

placeholder_text9 = "Confirm Password"
cpass_entry = ttk.Entry(ss, foreground='grey', show="*")
cpass_entry.place(x=497,y=560, width=250, height=40)
cpass_entry.insert(0, placeholder_text9)
cpass_entry.bind('<FocusIn>', lambda event: on_entry_click(event,cpass_entry, placeholder_text9))
cpass_entry.bind('<FocusOut>', lambda event: on_focusout(event, cpass_entry, placeholder_text9))

SignUpButton = ttk.Button(ss, text='Sign up', command=sign_up_st)
SignUpButton.place(x=497, y=610, width=250, height=30)
bButton1=ttk.Button(ss,text='Back',command=showSL2)
bButton1.place(x=497, y=650, width=250,height=30)

# Student Frame
st = tk.Frame(ges)
background_image3 = Image.open("stdform.jpg")
background_image3 = background_image3.resize((1320, 780))
background_photo3 = ImageTk.PhotoImage(background_image3)
background_label3 = tk.Label(st, image=background_photo3)
background_label3.place(relwidth=1, relheight=1)

mOFrame=Frame(st,bg='#E8D8D8')
mOFrame.place(x=85,y=80,width=1120,height=650)
mFrame=Frame(st,bg='white')
mFrame.place(x=86,y=81,width=1118,height=648)
m1Frame=Frame(st,bg='white')
m1Frame.place(x=111, y=180, width=1081,height=530)
searchButton=ttk.Button(mFrame,text='Search')
searchButton.place(x=435, y=50)
label= ttk.Label(mFrame,text='Awards')
label.place(x=900, y=70)

placeholder_text10 = "Subject/Year Level/Semester"
subj_entry = ttk.Entry(mFrame, foreground='grey')
subj_entry.place(x=30, y=49, width=400, height=30)
subj_entry.insert(0, placeholder_text10)
subj_entry.bind('<FocusIn>', lambda event: on_entry_click(event,subj_entry, placeholder_text10))
subj_entry.bind('<FocusOut>', lambda event: on_focusout(event, subj_entry, placeholder_text10))
Std_label = ttk.Label(mFrame, text="", foreground='black')
Std_label.place(x=50, y=20)

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
    for widget in m1Frame.winfo_children():
        widget.destroy()
    # Create and pack the current step frame
    frame = steps[current_step]()
    frame.pack(fill="both", expand=True)


# Function to create a generic TreeView frame
def create_treeview_frame(title, col_defs):
    def frame_func():
        frame = tk.Frame(m1Frame)
        # Title
        label = tk.Label(frame, text=title, font=("Calibri", 20))
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
            submit_button = ttk.Button(nav_frame, text="Submit", command=mFrame.quit)
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

show_step()

sign_outButton=ttk.Button(st, text='Sign Out', command=SignOutST)
sign_outButton.place(x=1170,y=15)

# Rlogin Frame
rl = tk.Frame(ges)
bgrl=Frame(rl,bg='#E8D8D8')
bgrl.place(x=0,y=0,width=1320,height=780)
bgI1 = Image.open("EECP GESYS FrontSS.jpg")
bgI1 = bgI1.resize((1320, 780))
bgP1 = ImageTk.PhotoImage(bgI1)
background_labelrl = tk.Label(bgrl, image=bgP1)
background_labelrl.place(relwidth=1, relheight=1)

placeholder_texta = "Registrar Number"
username_entryr = ttk.Entry(rl, foreground='grey')
username_entryr.place(x=900, y=420, width=300, height=30)
username_entryr.insert(0, placeholder_texta)
username_entryr.bind('<FocusIn>', lambda event: on_entry_click(event,username_entryr, placeholder_texta))
username_entryr.bind('<FocusOut>', lambda event: on_focusout(event, username_entryr, placeholder_texta))

placeholder_textb = "Password"
password_entryr = ttk.Entry(rl, foreground='grey', show="*")
password_entryr.place(x=900, y=470, width=300, height=30)
password_entryr.insert(0, placeholder_textb)
password_entryr.bind('<FocusIn>', lambda event: on_entry_click(event,password_entryr, placeholder_textb))
password_entryr.bind('<FocusOut>', lambda event: on_focusout(event, password_entryr, placeholder_textb))

rlButton=ttk.Button(rl,text='Login',command=login2)
rlButton.place(x=955, y=550, width=200,height=30)

rlSButton=ttk.Button(rl,text='Sign-up',command=showRS)
rlSButton.place(x=983, y=601, width=150,height=50)

rlBackButton=ttk.Button(rl,text='Back', command=showGES2)
rlBackButton.place(x=983, y=661, width=150,height=50)

# rsignup Frame
rs = tk.Frame(ges)

bg3=Frame(rs,bg='#E8D8D8')
bg3.place(x=0,y=0,width=1320,height=780)
bgI3 = Image.open("rsignup.jpg")
bgI3 = bgI3.resize((1320, 780))
bgP3 = ImageTk.PhotoImage(bgI3)
background_labelr = tk.Label(bg3, image=bgP3)
background_labelr.place(relwidth=1, relheight=1)

midFrame1=Frame(rs,bg='grey')
midFrame1.place(x=450,y=100,width=350,height=600)
midFrame1=Frame(rs,bg='white')
midFrame1.place(x=451,y=101,width=348,height=598)

login_titleLabel2 = tk.Label(rs,text='Sign up here', bg='white', font=('Cambria', 15, 'bold'))
login_titleLabel2.place(x=525, y=150, width=200,height=30)

placeholder_textc = "Name"
username_entry1 = ttk.Entry(rs, foreground='grey')
username_entry1.place(x=497,y=280, width=250, height=40)
username_entry1.insert(0, placeholder_textc)
username_entry1.bind('<FocusIn>', lambda event: on_entry_click(event,username_entry1, placeholder_textc))
username_entry1.bind('<FocusOut>', lambda event: on_focusout(event, username_entry1, placeholder_textc))

placeholder_textd = "Registrar Number"
rn_entry= ttk.Entry(rs, foreground='grey')
rn_entry.place(x=497,y=340, width=250, height=40)
rn_entry.insert(0, placeholder_textd)
rn_entry.bind('<FocusIn>', lambda event: on_entry_click(event,rn_entry, placeholder_textd))
rn_entry.bind('<FocusOut>', lambda event: on_focusout(event, rn_entry, placeholder_textd))

placeholder_texte = "Password"
pass_entry1 = ttk.Entry(rs, foreground='grey', show="*")
pass_entry1.place(x=497,y=400, width=250, height=40)
pass_entry1.insert(0, placeholder_texte)
pass_entry1.bind('<FocusIn>', lambda event: on_entry_click(event,pass_entry1, placeholder_texte))
pass_entry1.bind('<FocusOut>', lambda event: on_focusout(event, pass_entry1, placeholder_texte))

placeholder_textf = "Confirm Password"
cpass_entry1 = ttk.Entry(rs, foreground='grey', show="*")
cpass_entry1.place(x=497,y=460, width=250, height=40)
cpass_entry1.insert(0, placeholder_textf)
cpass_entry1.bind('<FocusIn>', lambda event: on_entry_click(event,cpass_entry1, placeholder_textf))
cpass_entry1.bind('<FocusOut>', lambda event: on_focusout(event, cpass_entry1, placeholder_textf))

SignUpButton1=ttk.Button(rs,text='Sign up',command=sign_up)
SignUpButton1.place(x=497, y=580, width=250,height=30)

bButton1=ttk.Button(rs,text='Back',command=showRL2)
bButton1.place(x=497, y=620, width=250,height=30)

# Registrar Frame
re = tk.Frame(ges)
connectButton=ttk.Button(re,text='Connect Database')
connectButton.place(x=980,y=15)

leftFrame=Frame(re,bg='#A64C4C')
leftFrame.place(x=50,y=80,width=10,height=650)

rightFrame=Frame(re,bg='#E8D8D8')
rightFrame.place(x=90,y=80,width=1120,height=650)

background_image4 = Image.open("studentbg.jpg")
background_image4 = background_image4.resize((1320, 780))
background_photo4 = ImageTk.PhotoImage(background_image4)
background_label4 = tk.Label(rightFrame, image=background_photo4)
background_label4.place(relwidth=1, relheight=1)

placeholder_textg = "Student Name/Student Number"
Std_entry = ttk.Entry(re, foreground='grey')
Std_entry.place(x=100, y=39, width=400, height=30)
Std_entry.insert(0, placeholder_textg)
Std_entry.bind('<FocusIn>', lambda event: on_entry_click(event,Std_entry, placeholder_textg))
Std_entry.bind('<FocusOut>', lambda event: on_focusout(event, Std_entry, placeholder_textg))

srcstudentButton=ttk.Button(re,text='Search')
srcstudentButton.place(x=510, y=40)

searchButton1=ttk.Button(rightFrame,text='Search')
searchButton1.place(x=435, y=50)

placeholder_texth = "Subject/Year Level/Semester"
subj_entry4 = ttk.Entry(rightFrame, foreground='grey')
subj_entry4.place(x=30, y=49, width=400, height=30)
subj_entry4.insert(0, placeholder_texth)
subj_entry4.bind('<FocusIn>', lambda event: on_entry_click(event,subj_entry4, placeholder_texth))
subj_entry4.bind('<FocusOut>', lambda event: on_focusout(event,subj_entry4, placeholder_texth))

std1Table = ttk.Treeview(rightFrame, columns=('Course Number','Subject', 'Units', 'Rating', 'Final Grade','Status'))
std1Table.place(x=30, y=100,width=1060 ,height=510)
std1Table.column('Course Number', width=30)
std1Table.column('Subject', width=380)
std1Table.column('Units', width=30)
std1Table.column('Rating', width=80)
std1Table.column('Final Grade', width=80)
std1Table.column('Status', width=60)

std1Table.heading('Course Number', text='Course No.')
std1Table.heading('Subject', text='Subject')
std1Table.heading('Units', text='Units')
std1Table.heading('Rating', text='Ratings')
std1Table.heading('Final Grade', text='Final Grade')
std1Table.heading('Status', text='Status')
std1Table.config(show='headings')

std1Table.bind("<Double-1>", lambda event: edit_item(event, std1Table))
std1Table.bind("<Double-1>", lambda event: edit_item(event, std1Table))

# Populate the registrar table initially
update_student_table(std1Table)

signoutButton=ttk.Button(re, text='Sign Out', command=SignOutRE)
signoutButton.place(x=1170,y=15)

ges.mainloop()