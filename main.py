
import tkinter as tk
from tkinter import ttk, messagebox
import database

# Create database
database.connect_db()

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("950x600")
root.configure(bg="#eef2f7")

selected_id = None

# Heading
heading = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#263746",
    fg="white",
    pady=15
)
heading.pack(fill="x")

# Input frame
form_frame = tk.Frame(root, bg="#eef2f7", pady=15)
form_frame.pack()

# Input labels and fields
tk.Label(form_frame, text="Student Name", bg="#eef2f7").grid(row=0, column=0, padx=10, pady=8)
name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=1, padx=10)

tk.Label(form_frame, text="Age", bg="#eef2f7").grid(row=0, column=2, padx=10)
age_entry = tk.Entry(form_frame, width=25)
age_entry.grid(row=0, column=3, padx=10)

tk.Label(form_frame, text="Course", bg="#eef2f7").grid(row=1, column=0, padx=10, pady=8)
course_entry = tk.Entry(form_frame, width=25)
course_entry.grid(row=1, column=1, padx=10)

tk.Label(form_frame, text="Email", bg="#eef2f7").grid(row=1, column=2, padx=10)
email_entry = tk.Entry(form_frame, width=25)
email_entry.grid(row=1, column=3, padx=10)


# Clear input fields
def clear_fields():
    global selected_id
    selected_id = None

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


# Display records in table
def display_students(records=None):
    for item in student_table.get_children():
        student_table.delete(item)

    if records is None:
        records = database.get_students()

    for student in records:
        student_table.insert("", tk.END, values=student)


# Validate input
def get_form_data():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    if not all([name, age, course, email]):
        messagebox.showwarning("Warning", "Please fill all fields!")
        return None

    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid positive age!")
        return None

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Enter a valid email!")
        return None

    return name, age, course, email


# Add student
def add_record():
    data = get_form_data()

    if data is None:
        return

    database.add_student(*data)
    display_students()
    clear_fields()

    messagebox.showinfo("Success", "Student added successfully!")


# Select student from table
def select_student(event):
    global selected_id

    selected = student_table.selection()

    if not selected:
        return

    values = student_table.item(selected[0], "values")
    selected_id = int(values[0])

    clear_entries_only()

    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    course_entry.insert(0, values[3])
    email_entry.insert(0, values[4])


def clear_entries_only():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


# Update student
def update_record():
    if selected_id is None:
        messagebox.showwarning("Warning", "Select a student first!")
        return

    data = get_form_data()

    if data is None:
        return

    database.update_student(selected_id, *data)
    display_students()
    clear_fields()

    messagebox.showinfo("Success", "Student updated successfully!")


# Delete student
def delete_record():
    global selected_id

    if selected_id is None:
        messagebox.showwarning("Warning", "Select a student first!")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        database.delete_student(selected_id)
        display_students()
        clear_fields()

        messagebox.showinfo("Success", "Student deleted successfully!")


# Search student
def search_record():
    keyword = search_entry.get().strip()

    if not keyword:
        display_students()
        return

    records = database.search_student(keyword)
    display_students(records)


# Buttons
button_frame = tk.Frame(root, bg="#eef2f7", pady=10)
button_frame.pack()

tk.Button(button_frame, text="Add Student", width=15,
          command=add_record, bg="#198754", fg="white").grid(row=0, column=0, padx=8)

tk.Button(button_frame, text="Update Student", width=15,
          command=update_record, bg="#0d6efd", fg="white").grid(row=0, column=1, padx=8)

tk.Button(button_frame, text="Delete Student", width=15,
          command=delete_record, bg="#dc3545", fg="white").grid(row=0, column=2, padx=8)

tk.Button(button_frame, text="Clear", width=15,
          command=clear_fields, bg="#6c757d", fg="white").grid(row=0, column=3, padx=8)


# Search section
search_frame = tk.Frame(root, bg="#eef2f7", pady=10)
search_frame.pack()

tk.Label(search_frame, text="Search by ID or Name:", bg="#eef2f7").pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

tk.Button(search_frame, text="Search",
          command=search_record, bg="#263746", fg="white").pack(side="left", padx=5)

tk.Button(search_frame, text="Show All",
          command=lambda: display_students(),
          bg="#263746", fg="white").pack(side="left", padx=5)


# Student table
table_frame = tk.Frame(root, bg="#eef2f7")
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("ID", "Name", "Age", "Course", "Email")

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=150, anchor="center")

student_table.pack(fill="both", expand=True)

student_table.bind("<<TreeviewSelect>>", select_student)

# Load existing records
display_students()

# Start application
root.mainloop()
