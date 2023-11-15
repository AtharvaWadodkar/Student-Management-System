import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import ctypes
from sqlite3 import Error


ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Create a database connection
try:

    conn = sqlite3.connect("alphadb.db", check_same_thread=False)
    cursor = conn.cursor()

except Error as e:
    print(e)

# Create the student_details table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS student_details (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, grade TEXT, fees REAL)")
# Create the attendance_details table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS attendance_details (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, classes_present INTEGER, classes_absent INTEGER, total_classes_attended INTEGER)")


def view_student_data():
    def search_student():
        student_name = name_entry.get()

        # Retrieve the student data from the database (case-insensitive search)
        cursor.execute("SELECT * FROM student_details WHERE LOWER(name) = LOWER(?)", (student_name,))
        student_data = cursor.fetchone()

        # Display the student data
        if student_data:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Name: {student_data[1]}\n")
            result_text.insert(tk.END, f"Age: {student_data[2]}\n")
            result_text.insert(tk.END, f"Grade: {student_data[3]}\n")
            if len(student_data) > 4:
                result_text.insert(tk.END, f"Fees: {student_data[4]}\n")
            if len(student_data) > 5:
                result_text.insert(tk.END, f"Monthly Fees: {student_data[5]}\n")  # Display monthly fees
        else:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "No student found.")

    view_window = tk.Toplevel()
    view_window.title("View Student Data")
    view_window.geometry("500x400")

    name_label = tk.Label(view_window, text="Student Name:", font=("Helvetica", 12))
    name_label.pack(pady=5)

    name_entry = tk.Entry(view_window)
    name_entry.pack(pady=5)

    search_button = ttk.Button(view_window, text="Search", command=search_student)
    search_button.pack(pady=15)

    result_text = tk.Text(view_window, height=6, width=30)
    result_text.pack(pady=10)
    view_window.grab_set()

    close_button = ttk.Button(view_window, text="Close", command=view_window.destroy)
    close_button.pack(pady=10)



def add_student_data():
    def save_student_data():
        student_name = name_entry.get()
        student_age = age_entry.get()
        student_grade = grade_entry.get()
        student_fees = fees_entry.get()  # Get the monthly fees

        # Insert the student data into the student_details table
        cursor.execute("INSERT INTO student_details (name, age, grade, monthly_fees) VALUES (?, ?, ?, ?)",
                       (student_name, student_age, student_grade, student_fees))
        conn.commit()

        # Retrieve the student_id of the inserted student
        cursor.execute("SELECT id FROM student_details WHERE name = ?", (student_name,))
        student_id = cursor.fetchone()[0]

        # Insert the student data into the attendance_details table
        cursor.execute("INSERT INTO attendance_details (id, name) VALUES (?, ?)",
                       (student_id, student_name))
        conn.commit()

        # Clear the entry fields
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        grade_entry.delete(0, tk.END)
        fees_entry.delete(0, tk.END)  # Clear the fees entry field

        # Show a success message
        tk.messagebox.showinfo("Success", "Student data added successfully.")

    add_window = tk.Toplevel()
    add_window.title("Add Student Data")
    add_window.geometry("600x500")

    name_label = tk.Label(add_window, text="Student Name:", font=("Helvetica", 10))
    name_label.pack(pady=5)

    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    age_label = tk.Label(add_window, text="Student Age:", font=("Helvetica", 10))
    age_label.pack(pady=5)

    age_entry = tk.Entry(add_window)
    age_entry.pack(pady=5)

    grade_label = tk.Label(add_window, text="Student Grade:", font=("Helvetica", 10))
    grade_label.pack(pady=5)

    grade_entry = tk.Entry(add_window)
    grade_entry.pack(pady=5)

    fees_label = tk.Label(add_window, text="Monthly Fees:", font=("Helvetica", 10))  # Add a label for the monthly fees
    fees_label.pack(pady=5)

    fees_entry = tk.Entry(add_window)  # Add an entry field for the monthly fees
    fees_entry.pack(pady=10)

    save_button = ttk.Button(add_window, text="Save", command=save_student_data)
    save_button.pack(pady=10)
    add_window.grab_set()

    close_button = ttk.Button(add_window, text="Close", command=add_window.destroy)
    close_button.pack(pady=10)



def delete_student_data():
    def confirm_delete():
        if confirm_var.get() == 1:
            student_name = name_entry.get()

            # Delete the student data from the database
            cursor.execute("DELETE FROM student_details WHERE name = ?", (student_name,))
            conn.commit()

            # Clear the entry field
            name_entry.delete(0, tk.END)

            # Show a success message
            tk.messagebox.showinfo("Success", "Student data deleted successfully.")
            delete_window.destroy()
        else:
            tk.messagebox.showinfo("Confirmation", "Please confirm deletion.")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Student Data")
    delete_window.geometry("600x500")
    delete_window.grab_set()

    name_label = tk.Label(delete_window, text="Student Name:", font=("Helvetica", 12))
    name_label.pack(pady=10)

    name_entry = tk.Entry(delete_window)
    name_entry.pack(pady=5)

    confirm_var = tk.IntVar()

    confirm_checkbutton = tk.Checkbutton(delete_window, text="Confirm Deletion",font=("Helvetica", 11), variable=confirm_var)
    confirm_checkbutton.pack(pady=10)

    delete_button = ttk.Button(delete_window, text="Delete", command=confirm_delete)
    delete_button.pack(pady=10)

    close_button = ttk.Button(delete_window, text="Close", command=delete_window.destroy)
    close_button.pack(pady=10)


def edit_student_data():
    def search_student():
        student_name = name_entry.get().lower()  # Convert input name to lowercase

        # Retrieve the student data from the database (case-insensitive search)
        cursor.execute("SELECT * FROM student_details WHERE LOWER(name) = ?", (student_name,))
        student_data = cursor.fetchone()

        # Display the student data
        if student_data:
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, student_data[1])

            age_entry.delete(0, tk.END)
            age_entry.insert(tk.END, student_data[2])

            grade_entry.delete(0, tk.END)
            grade_entry.insert(tk.END, student_data[3])

            fees_entry.delete(0, tk.END)
            fees_entry.insert(tk.END, student_data[4])
        else:
            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)
            grade_entry.delete(0, tk.END)
            tk.messagebox.showinfo("Error", "No student found.")

    def update_student_data():
        student_name = name_entry.get()
        student_age = age_entry.get()
        student_grade = grade_entry.get()
        student_fees = fees_entry.get()

        # Update the student data in the database
        cursor.execute("UPDATE student_details SET age = ?, grade = ?, monthly_fees = ? WHERE LOWER(name) = ?",
                       (student_age, student_grade, student_fees, student_name.lower()))  # Convert name to lowercase
        conn.commit()

        # Clear the entry fields
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        grade_entry.delete(0, tk.END)
        fees_entry.delete(0, tk.END)

        # Show a success message
        tk.messagebox.showinfo("Success", "Student data updated successfully.")


    edit_window = tk.Toplevel()
    edit_window.title("Edit Student Data")
    edit_window.geometry("700x650")
    edit_window.grab_set()

    name_label = tk.Label(edit_window, text="Student Name:", font=("Helvetica", 12))
    name_label.pack(pady=10)

    name_entry = tk.Entry(edit_window)
    name_entry.pack(pady=10)

    search_button = ttk.Button(edit_window, text="Search", command=search_student)
    search_button.pack(pady=10)

    age_label = tk.Label(edit_window, text="Student Age:", font=("Helvetica", 12))
    age_label.pack(pady=5)

    age_entry = tk.Entry(edit_window)
    age_entry.pack(pady=5)

    grade_label = tk.Label(edit_window, text="Student Grade:", font=("Helvetica", 12))
    grade_label.pack(pady=5)

    grade_entry = tk.Entry(edit_window)
    grade_entry.pack(pady=10)

    fees_label = tk.Label(edit_window, text="Monthly Fees:", font=("Helvetica", 12))
    fees_label.pack(pady=5)

    fees_entry = tk.Entry(edit_window)
    fees_entry.pack(pady=10)

    update_button = ttk.Button(edit_window, text="Update", command=update_student_data)
    update_button.pack(pady=15)

    close_button = ttk.Button(edit_window, text="Close", command=edit_window.destroy)
    close_button.pack(pady=5)

def manage_attendance():
    def search_student():
        student_name = name_entry.get()

        # Retrieve the student attendance data from the database
        cursor.execute("SELECT * FROM attendance_details WHERE name = ?", (student_name,))
        student_attendance = cursor.fetchone()
         # Display the student attendance data
        if student_attendance:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Name: {student_attendance[1]}\n")
                result_text.insert(tk.END, f"Classes Present: {student_attendance[2]}\n")
                result_text.insert(tk.END, f"Classes Absent: {student_attendance[3]}\n")
                result_text.insert(tk.END, f"Total Classes Taken: {student_attendance[4]}\n")
        else:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "No attendance record found.")

    def update_attendance(present):
        student_name = name_entry.get()

            # Retrieve the student attendance data from the database
        cursor.execute("SELECT * FROM attendance_details WHERE name = ?", (student_name,))
        student_attendance = cursor.fetchone()
        print(student_attendance)  # Added print statement

        if student_attendance is not None:
                # Update the attendance data based on the present parameter
            classes_present = student_attendance[2] + present if student_attendance[2] is not None else present
            classes_absent = student_attendance[3] + (1 - present) if student_attendance[3] is not None else (
                            1 - present)
            total_classes_attended = student_attendance[4] + 1 if student_attendance[4] is not None else 1

                # Update the attendance record in the database
            cursor.execute(
                    "UPDATE attendance_details SET classes_present = ?, classes_absent = ?, total_classes_attended = ? WHERE name = ?",
                    (classes_present, classes_absent, total_classes_attended, student_name))
            conn.commit()

                # Show a success message
            tk.messagebox.showinfo("Success", "Attendance updated successfully.")
        else:
                # No attendance record found, handle this case (e.g., show an error message)
            tk.messagebox.showerror("Error", "No attendance record found for the student.")

                # Create a new attendance record for the student
            classes_present = present
            classes_absent = 1 - present
            total_classes_attended = 1

                # Insert the attendance record into the database
            cursor.execute(
                    "INSERT INTO attendance_details (name, classes_present, classes_absent, total_classes_attended) VALUES (?, ?, ?, ?)",
                    (student_name, classes_present, classes_absent, total_classes_attended))
            conn.commit()

                # Show a success message
            tk.messagebox.showinfo("Success", "Attendance updated successfully.")

    attendance_window = tk.Toplevel()
    attendance_window.title("Manage Attendance")
    attendance_window.geometry("700x600")
    attendance_window.grab_set()

    name_label = tk.Label(attendance_window, text="Student Name:", font=("Helvetica", 12))
    name_label.pack(pady=10)

    name_entry = tk.Entry(attendance_window)
    name_entry.pack(pady=5)

    search_button = ttk.Button(attendance_window, text="Search", command=search_student)
    search_button.pack(pady=10)

    present_button = ttk.Button(attendance_window, text="Present", command=lambda: update_attendance(1))
    present_button.pack(pady=10)

    absent_button = ttk.Button(attendance_window, text="Absent", command=lambda: update_attendance(0))
    absent_button.pack(pady=10)

    result_text = tk.Text(attendance_window, height=6, width=30)
    result_text.pack(pady=15)

    close_button = ttk.Button(attendance_window, text="Close", command=attendance_window.destroy)
    close_button.pack(pady=20)


# Create the menu window
def create_menu_window():
    menu_window.title("Student Class Management")
    menu_window.geometry("800x600")

    welcome_label = tk.Label(menu_window, text="Welcome to Student Management System", font=("Helvetica", 15))
    welcome_label.pack(pady=25)

    # Create a style for the buttons
    style = ttk.Style()
    style.configure("TButton", padding=10, font=("Helvetica", 12))

    view_button = ttk.Button(menu_window, text="View Student Data", command=view_student_data)
    view_button.pack(pady=20)

    add_button = ttk.Button(menu_window, text="Add Student Data", command=add_student_data)
    add_button.pack(pady=20)

    delete_button = ttk.Button(menu_window, text="Delete Student Data", command=delete_student_data)
    delete_button.pack(pady=20)

    edit_button = ttk.Button(menu_window, text="Edit Student Data", command=edit_student_data)
    edit_button.pack(pady=20)

    attendance_button = ttk.Button(menu_window, text="Manage Attendance", command=manage_attendance)
    attendance_button.pack(pady=20)

    menu_window.mainloop()

# Run the program
menu_window = tk.Tk()
create_menu_window()

# Close the database connection
cursor.close()
conn.close()




