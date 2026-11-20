import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from main.create_fields import add_field
from db.db import add_student, delete_student, get_students, update_student


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
    selected_student_id = None
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

        clear_form()
        for item in student_list.get_children():
            student_list.delete(item)
        for student in students:
            student_list.insert("", tk.END, values=student)

    def clear_form():
        nonlocal selected_student_id
        selected_student_id = None
        student_id_entry.configure(state="normal")
        for entry in (student_id_entry, student_name_entry, student_email_entry):
            entry.delete(0, tk.END)
        student_list.selection_remove(student_list.selection())

    def populate_form(_event=None):
        nonlocal selected_student_id
        selection = student_list.selection()
        if not selection:
            return

        selected_student_id, name, email = student_list.item(
            selection[0], "values"
        )
        clear_form_entries = (
            (student_id_entry, selected_student_id),
            (student_name_entry, name),
            (student_email_entry, email),
        )
        student_id_entry.configure(state="normal")
        for entry, value in clear_form_entries:
            entry.delete(0, tk.END)
            entry.insert(0, value)

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

    def update_student_from_gui():
        if selected_student_id is None:
            messagebox.showwarning(
                "No student selected",
                "Select a student to update.",
                parent=students_tab,
            )
            return

        student_id = student_id_entry.get().strip()
        name = student_name_entry.get().strip()
        email = student_email_entry.get().strip()
        if not student_id or not name or not email:
            messagebox.showwarning(
                "Missing student details",
                "Please enter a student ID, name, and email.",
                parent=students_tab,
            )
            return

        try:
            update_student(
                selected_student_id,
                name,
                email,
                new_student_id=student_id,
            )
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not update student", str(error), parent=students_tab
            )
            return

        clear_form()
        display_saved_students()

    def delete_selected_student():
        if selected_student_id is None:
            messagebox.showwarning(
                "No student selected",
                "Select a student to delete.",
                parent=students_tab,
            )
            return
        if not messagebox.askyesno(
            "Delete student",
            f"Delete student {selected_student_id}?",
            parent=students_tab,
        ):
            return

        try:
            delete_student(selected_student_id)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not delete student", str(error), parent=students_tab
            )
            return

        clear_form()
        display_saved_students()

    student_list.bind("<<TreeviewSelect>>", populate_form)
    student_add_button = tk.Button(
        students_tab,
        text="Create Student",
        command=add_student_from_gui,
        width=15,
        border=3,
    )
    student_add_button.grid(row=4, column=0, pady=10, padx=10)
    student_update_button = tk.Button(
        students_tab,
        text="Update Student",
        command=update_student_from_gui,
        width=15,
        border=3,
    )
    student_update_button.grid(row=4, column=1, pady=10, padx=10)
    student_delete_button = tk.Button(
        students_tab,
        text="Delete Student",
        command=delete_selected_student,
        width=15,
        border=3,
    )
    student_delete_button.grid(row=4, column=2, pady=10, padx=10)

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
        row=6, column=0, columnspan=3, sticky="nsew", padx=8, pady=4
    )
    student_scrollbar.grid(row=6, column=3, sticky="ns")
    student_horizontal_scrollbar.grid(
        row=7, column=0, columnspan=3, sticky="ew", padx=8
    )
    students_tab.columnconfigure(1, weight=1)
    students_tab.rowconfigure(6, weight=1)
    display_saved_students()
    return students_tab
