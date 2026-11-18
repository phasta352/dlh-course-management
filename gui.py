#!/usr/bin/env python3
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from courses import ClassroomCourse, OnlineCourse
from db import add_student, add_course, initialize_database

initialize_database()

def add_student_from_gui():
    student_id = student_id_entry.get()
    student_name = student_name_entry.get()
    student_email = student_email_entry.get()

    try:
        add_student(student_id, student_name, student_email)
    except sqlite3.Error as error:
        messagebox.showerror("Could not add student", str(error), parent=window)
    else:
        messagebox.showinfo(
            "Student added",
            f"{student_name} was added successfully.",
            parent=window,
        )

def create_course():
    course_id = course_id_entry.get()
    course_title = course_title_entry.get()
    try:
        course_price = float(course_price_entry.get())
        course_capacity = int(course_capacity_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid course details",
            "Enter a valid price and whole-number capacity.",
            parent=window,
        )
        return

    course_room_number = course_room_number_entry.get()
    course_address = course_address_entry.get()

    if onlinevar.get():
        course_type = "online"
        course_meeting_link = course_meeting_link_entry.get()
        if not course_meeting_link:
            messagebox.showwarning(
                "Missing course details",
                "Please provide a meeting link for the online course.",
                parent=window,
            )
            return
        course = OnlineCourse(course_id, course_title, course_price, course_capacity, course_meeting_link)
    elif classroomvar.get():
        course_type = "classroom"
        if not course_room_number or not course_address:
            messagebox.showwarning(
                "Missing course details",
                "Please provide both room number and address for the classroom course.",
                parent=window,
            )
            return
        course = ClassroomCourse(course_id, course_title, course_price, course_capacity, course_room_number, course_address)
    else:
        messagebox.showwarning(
            "Course type required",
            "Select online or classroom course.",
            parent=window,
        )
        return

    try:
        add_course(course_id, course_title, course_type, course_price, course_capacity, room_number=course_room_number, address=course_address,
                   meeting_link=course_meeting_link)
    except sqlite3.Error as error:
        messagebox.showerror("Could not add course", str(error), parent=window)
    else:
        messagebox.showinfo(
        "Course created",
        f"{course.title} was created successfully!",
        parent=window,
        )

def add_field(parent, label_text, row, column, width=20):
    label = tk.Label(parent, text=label_text)
    label.grid(row=row, column=column, sticky="w", padx=8, pady=4)

    entry = tk.Entry(parent, width=width, border=3)
    entry.grid(row=row, column=column + 1, sticky="w")
    return label, entry

# GUI setup of the main window
window = tk.Tk()
window.title("Course Management")

# Create a notebook (tabbed interface) to separate course and student management
notebook = ttk.Notebook(window)
notebook.pack(fill="both", pady=10, expand=True)
course_tab = ttk.Frame(notebook)
notebook.add(course_tab, text="Courses")
student_tab = ttk.Frame(notebook)
notebook.add(student_tab, text="Students")

# Add fields and buttons for student management
student_id_label, student_id_entry = add_field(student_tab, "Student Id", 0, 0, width=10)
student_name_label, student_name_entry = add_field(student_tab, "Student Name", 2, 0, width=30)
student_email_label, student_email_entry = add_field(student_tab, "Student Email", 3, 0, width=30)

student_add_button = tk.Button(student_tab, text="Add Student", command=add_student_from_gui, width=15, border=3)
student_add_button.grid(row=4, column=1, columnspan=1, pady=10, padx=10)

course_id_label, course_id_entry = add_field(course_tab, "Course Id", 0, 0, width=10)
course_title_label, course_title_entry = add_field(course_tab, "Course Title", 1, 0, width=30)
course_price_label, course_price_entry = add_field(course_tab, "Course Price", 2, 0, width=10)
course_capacity_label, course_capacity_entry = add_field(course_tab, "Course Capacity", 3, 0, width=10)
course_meeting_link_label, course_meeting_link_entry = add_field(course_tab, "Course Meeting Link", 4, 0, width=30)
course_room_number_label, course_room_number_entry = add_field(course_tab, "Course Room Number", 5, 0, width=10)
course_address_label, course_address_entry = add_field(course_tab, "Course Address", 6, 0, width=30)

onlinevar = tk.BooleanVar()
online_checkbutton = tk.Checkbutton(course_tab, text="Online Course", variable=onlinevar)
online_checkbutton.grid(row=7, column=0, padx=8, pady=4)

classroomvar = tk.BooleanVar()
classroom_checkbutton = tk.Checkbutton(course_tab, text="Classroom Course", variable=classroomvar)
classroom_checkbutton.grid(row=7, column=1, padx=8, pady=4)

create_button = tk.Button(course_tab, text="Create Course", command=create_course, width=15, border=3)
create_button.grid(row=14, column=1, pady=10, padx=10)

window.mainloop()