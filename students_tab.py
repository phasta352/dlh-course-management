import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from create_fields import add_field
from db import add_student, get_students


def build_students_tab(notebook):
    students_tab = ttk.Frame(notebook)
    notebook.add(students_tab, text="Students")

    student_id_label, student_id_entry = add_field(
        students_tab, "Student Id", 0, 0, width=10
    )
    student_name_label, student_name_entry = add_field(
        students_tab, "Student Name", 2, 0, width=30
    )
    student_email_label, student_email_entry = add_field(
        students_tab, "Student Email", 3, 0, width=30
    )

    student_list = ttk.Treeview(
        students_tab, columns=("student_id", "name", "email"), show="headings"
    )
    for column, heading, width in (
        ("student_id", "Student ID", 100),
        ("name", "Name", 180),
        ("email", "Email", 220),
    ):
        student_list.heading(column, text=heading)
        student_list.column(column, width=width, stretch=False)

    def display_saved_students():
        try:
            students = get_students()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not load students", str(error), parent=students_tab
            )
            return

        for item in student_list.get_children():
            student_list.delete(item)
        for student in students:
            student_list.insert("", tk.END, values=student)

    def add_student_from_gui():
        student_id = student_id_entry.get()
        student_name = student_name_entry.get()
        student_email = student_email_entry.get()

        try:
            add_student(student_id, student_name, student_email)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not add student", str(error), parent=students_tab
            )
            return

        messagebox.showinfo(
            "Student added",
            f"{student_name} was added successfully.",
            parent=students_tab,
        )
        student_id_entry.delete(0, tk.END)
        student_name_entry.delete(0, tk.END)
        student_email_entry.delete(0, tk.END)
        display_saved_students()

    student_add_button = tk.Button(
        students_tab,
        text="Add Student",
        command=add_student_from_gui,
        width=15,
        border=3,
    )
    student_add_button.grid(row=4, column=1, pady=10, padx=10)
    student_display_button = tk.Button(
        students_tab,
        text="Display Students",
        command=display_saved_students,
        width=15,
        border=3,
    )
    student_display_button.grid(row=5, column=1, pady=10, padx=10)

    student_scrollbar = ttk.Scrollbar(
        students_tab, orient="vertical", command=student_list.yview
    )
    student_horizontal_scrollbar = ttk.Scrollbar(
        students_tab, orient="horizontal", command=student_list.xview
    )
    student_list.configure(
        yscrollcommand=student_scrollbar.set,
        xscrollcommand=student_horizontal_scrollbar.set,
    )
    student_list.grid(
        row=6, column=0, columnspan=2, sticky="nsew", padx=8, pady=4
    )
    student_scrollbar.grid(row=6, column=2, sticky="ns")
    student_horizontal_scrollbar.grid(
        row=7, column=0, columnspan=2, sticky="ew", padx=8
    )
    students_tab.columnconfigure(1, weight=1)
    students_tab.rowconfigure(6, weight=1)
    display_saved_students()
    return students_tab
