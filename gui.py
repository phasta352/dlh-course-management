#!/usr/bin/env python3
import sqlite3
import tkinter as tk
from tkinter import messagebox

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

# GUI setup of the main window and input fields
window = tk.Tk()
window.title("Course Management")
courses = []

student_id_label = tk.Label(window, text="Student Id")
student_id_label.grid(row=0, column=0, sticky="w", padx=8, pady= 4)
student_id_entry = tk.Entry(window, width=10, border=3)
student_id_entry.grid(row=0, column=1, sticky="w")

student_name_label = tk.Label(window, text="Student Name")
student_name_label.grid(row=2, column=0, sticky="w", padx=8 , pady= 4)
student_name_entry = tk.Entry(window, width=30, border=3)
student_name_entry.grid(row=2, column=1)

student_email_label = tk.Label(window, text="Student Email")
student_email_label.grid(row=3, column=0, sticky="w", padx=8, pady= 4)
student_email_entry = tk.Entry(window, width=30, border=3)
student_email_entry.grid(row=3, column=1)

student_add_button = tk.Button(window, text="Add Student", command=add_student_from_gui, width=15, border=3)
student_add_button.grid(row=4, column=1, columnspan=1, pady=10, padx=10)

course_id_label = tk.Label(window, text="Course Id")
course_id_label.grid(row=6, column=0, sticky="w", padx=8, pady= 4)
course_id_entry = tk.Entry(window, width=10, border=3)
course_id_entry.grid(row=6, column=1, sticky="w")

course_title_label = tk.Label(window, text="Course Title")
course_title_label.grid(row=7, column=0, sticky="w", padx=8, pady= 4)
course_title_entry = tk.Entry(window, width=30, border=3)
course_title_entry.grid(row=7, column=1)

course_price_label = tk.Label(window, text="Course Price")
course_price_label.grid(row=8, column=0, sticky="w", padx=8, pady= 4)
course_price_entry = tk.Entry(window, width=10, border=3)
course_price_entry.grid(row=8, column=1, sticky="w")

course_capacity_label = tk.Label(window, text="Course Capacity")
course_capacity_label.grid(row=9, column=0, sticky="w", padx=8, pady= 4)
course_capacity_entry = tk.Entry(window, width=10, border=3)
course_capacity_entry.grid(row=9, column=1, sticky="w")

course_meeting_link_label = tk.Label(window, text="Course Meeting Link")
course_meeting_link_label.grid(row=10, column=0, sticky="w", padx=8, pady= 4)
course_meeting_link_entry = tk.Entry(window, width=30, border=3)
course_meeting_link_entry.grid(row=10, column=1)

course_room_number_label = tk.Label(window, text="Course Room Number")
course_room_number_label.grid(row=11, column=0, sticky="w", padx=8, pady= 4)
course_room_number_entry = tk.Entry(window, width=10, border=3)
course_room_number_entry.grid(row=11, column=1, sticky="w")

course_address_label = tk.Label(window, text="Course Address")
course_address_label.grid(row=12, column=0, sticky="w", padx=8, pady= 4)
course_address_entry = tk.Entry(window, width=30, border=3)
course_address_entry.grid(row=12, column=1)

onlinevar = tk.BooleanVar()
online_checkbutton = tk.Checkbutton(window, text="Online Course", variable=onlinevar)
online_checkbutton.grid(row=13, column=0, padx=8, pady=4)

classroomvar = tk.BooleanVar()
classroom_checkbutton = tk.Checkbutton(window, text="Classroom Course", variable=classroomvar)
classroom_checkbutton.grid(row=13, column=1, padx=8, pady=4)

create_button = tk.Button(window, text="Create Course", command=create_course, width=15, border=3)
create_button.grid(row=14, column=1, pady=10, padx=10)

window.mainloop()