
import sqlite3

# Connect to database
def connect_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add student
def add_student(name, age, course, email):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
        (name, age, course, email)
    )

    conn.commit()
    conn.close()


# Display all students
def get_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    conn.close()
    return records


# Update student
def update_student(student_id, name, age, course, email):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, age=?, course=?, email=?
        WHERE id=?
    """, (name, age, course, email, student_id))

    conn.commit()
    conn.close()


# Delete student
def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()


# Search student
def search_student(keyword):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE CAST(id AS TEXT) LIKE ?
        OR name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()
    conn.close()

    return records
