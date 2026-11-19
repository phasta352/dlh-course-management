#!/usr/bin/env python3
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from courses import ClassroomCourse, OnlineCourse
from db import (
    APPLICATION_STATUSES,
    add_application,
    add_student,
    add_course,
    get_applications,
    initialize_database,
)

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
        student_id_entry.delete(0, tk.END)
        student_name_entry.delete(0, tk.END)
        student_email_entry.delete(0, tk.END)

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
        course_id_entry.delete(0, tk.END)
        course_title_entry.delete(0, tk.END)
        course_price_entry.delete(0, tk.END)
        course_capacity_entry.delete(0, tk.END)
        course_meeting_link_entry.delete(0, tk.END)
        course_room_number_entry.delete(0, tk.END)
        course_address_entry.delete(0, tk.END)

def display_saved_applications():
    try:
        applications = get_applications()
    except sqlite3.Error as error:
        messagebox.showerror(
            "Could not load applications", str(error), parent=window
        )
        return

    for item in application_list.get_children():
        application_list.delete(item)
    for application in applications:
        application_list.insert("", tk.END, values=application)


def save_application():
    company = company_entry.get().strip()
    job_title = job_title_entry.get().strip()
    status = application_status.get()

    if not company or not job_title:
        messagebox.showwarning(
            "Missing application details",
            "Please enter both a company and a job title.",
            parent=window,
        )
        return

    try:
        add_application(company, job_title, status)
    except sqlite3.Error as error:
        messagebox.showerror(
            "Could not save application", str(error), parent=window
        )
        return

    company_entry.delete(0, tk.END)
    job_title_entry.delete(0, tk.END)
    display_saved_applications()


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
application_tab = ttk.Frame(notebook)
notebook.add(application_tab, text="Applications")

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

company_label, company_entry = add_field(
    application_tab, "Company", 0, 0, width=30
)
job_title_label, job_title_entry = add_field(
    application_tab, "Job Title", 1, 0, width=30
)
tk.Label(application_tab, text="Status").grid(
    row=2, column=0, sticky="w", padx=8, pady=4
)
application_status = ttk.Combobox(
    application_tab,
    values=APPLICATION_STATUSES,
    state="readonly",
    width=27,
)
application_status.grid(row=2, column=1, sticky="w")
application_status.set(APPLICATION_STATUSES[0])

save_application_button = tk.Button(
    application_tab,
    text="Save Application",
    command=save_application,
    width=18,
    border=3,
)
save_application_button.grid(row=3, column=1, pady=10, padx=10)

application_list = ttk.Treeview(
    application_tab,
    columns=("company", "job_title", "status"),
    show="headings",
)
application_list.heading("company", text="Company")
application_list.heading("job_title", text="Job Title")
application_list.heading("status", text="Status")
application_list.grid(
    row=4, column=0, columnspan=2, sticky="nsew", padx=8, pady=4
)
application_tab.columnconfigure(1, weight=1)
application_tab.rowconfigure(4, weight=1)
display_saved_applications()

window.mainloop()