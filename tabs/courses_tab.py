import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from main.courses import ClassroomCourse, OnlineCourse
from main.create_fields import add_field
from db.db import add_course, delete_course, get_courses, update_course


def build_courses_tab(notebook):
    courses_tab = ttk.Frame(notebook)
    notebook.add(courses_tab, text="Courses")

    course_id_label, course_id_entry = add_field(
        courses_tab, "Course Id", 0, 0, width=10
    )
    course_title_label, course_title_entry = add_field(
        courses_tab, "Course Title", 1, 0, width=30
    )
    course_price_label, course_price_entry = add_field(
        courses_tab, "Course Price", 2, 0, width=10
    )
    course_capacity_label, course_capacity_entry = add_field(
        courses_tab, "Course Capacity", 3, 0, width=10
    )
    course_meeting_link_label, course_meeting_link_entry = add_field(
        courses_tab, "Course Meeting Link", 4, 0, width=30
    )
    course_room_number_label, course_room_number_entry = add_field(
        courses_tab, "Course Room Number", 5, 0, width=10
    )
    course_address_label, course_address_entry = add_field(
        courses_tab, "Course Address", 6, 0, width=30
    )

    onlinevar = tk.BooleanVar(master=courses_tab)
    online_checkbutton = tk.Checkbutton(
        courses_tab, text="Online Course", variable=onlinevar
    )
    online_checkbutton.grid(row=7, column=0, padx=8, pady=4)

    classroomvar = tk.BooleanVar(master=courses_tab)
    classroom_checkbutton = tk.Checkbutton(
        courses_tab, text="Classroom Course", variable=classroomvar
    )
    classroom_checkbutton.grid(row=7, column=1, padx=8, pady=4)

    course_list = ttk.Treeview(
        courses_tab,
        columns=(
            "course_id",
            "title",
            "course_type",
            "price",
            "capacity",
            "meeting_link",
            "room_number",
            "address",
        ),
        show="headings",
    )
    selected_course_id = None
    for column, heading, width in (
        ("course_id", "Course ID", 90),
        ("title", "Title", 160),
        ("course_type", "Type", 90),
        ("price", "Price", 80),
        ("capacity", "Capacity", 90),
        ("meeting_link", "Meeting Link", 220),
        ("room_number", "Room Number", 110),
        ("address", "Address", 220),
    ):
        course_list.heading(column, text=heading)
        course_list.column(column, width=width, stretch=False)

    def display_saved_courses():
        try:
            courses = get_courses()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not load courses", str(error), parent=courses_tab
            )
            return

        clear_course_form()
        for item in course_list.get_children():
            course_list.delete(item)
        for course in courses:
            course_list.insert("", tk.END, values=course)

    def clear_course_form():
        nonlocal selected_course_id
        selected_course_id = None
        course_id_entry.configure(state="normal")
        for entry in (
            course_id_entry,
            course_title_entry,
            course_price_entry,
            course_capacity_entry,
            course_meeting_link_entry,
            course_room_number_entry,
            course_address_entry,
        ):
            entry.delete(0, tk.END)
        onlinevar.set(False)
        classroomvar.set(False)
        course_list.selection_remove(course_list.selection())

    def populate_course_form(_event=None):
        nonlocal selected_course_id
        selection = course_list.selection()
        if not selection:
            return

        (
            selected_course_id,
            title,
            course_type,
            price,
            capacity,
            meeting_link,
            room_number,
            address,
        ) = course_list.item(selection[0], "values")
        course_id_entry.configure(state="normal")
        values = (
            (course_id_entry, selected_course_id),
            (course_title_entry, title),
            (course_price_entry, price),
            (course_capacity_entry, capacity),
            (course_meeting_link_entry, meeting_link or ""),
            (course_room_number_entry, room_number or ""),
            (course_address_entry, address or ""),
        )
        for entry, value in values:
            entry.delete(0, tk.END)
            entry.insert(0, value)
        onlinevar.set(course_type == "online")
        classroomvar.set(course_type == "classroom")

    def create_course():
        course_id = course_id_entry.get()
        course_title = course_title_entry.get().strip()
        try:
            course_price = float(course_price_entry.get())
            course_capacity = int(course_capacity_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid course details",
                "Enter a valid price and whole-number capacity.",
                parent=courses_tab,
            )
            return

        if course_price < 0 or course_capacity <= 0:
            messagebox.showerror(
                "Invalid course details",
                "Price cannot be negative and capacity must be greater than zero.",
                parent=courses_tab,
            )
            return

        course_room_number = course_room_number_entry.get()
        course_address = course_address_entry.get()
        course_meeting_link = None

        if onlinevar.get():
            course_type = "online"
            course_meeting_link = course_meeting_link_entry.get()
            if not course_meeting_link:
                messagebox.showwarning(
                    "Missing course details",
                    "Please provide a meeting link for the online course.",
                    parent=courses_tab,
                )
                return
            course = OnlineCourse(
                course_id,
                course_title,
                course_price,
                course_capacity,
                course_meeting_link,
            )
        elif classroomvar.get():
            course_type = "classroom"
            if not course_room_number or not course_address:
                messagebox.showwarning(
                    "Missing course details",
                    "Please provide both room number and address for the classroom course.",
                    parent=courses_tab,
                )
                return
            course = ClassroomCourse(
                course_id,
                course_title,
                course_price,
                course_capacity,
                course_room_number,
                course_address,
            )
        else:
            messagebox.showwarning(
                "Course type required",
                "Select online or classroom course.",
                parent=courses_tab,
            )
            return

        try:
            add_course(
                course_id,
                course_title,
                course_price,
                course_capacity,
                course_type,
                meeting_link=course_meeting_link or None,
                room_number=course_room_number or None,
                address=course_address or None,
            )
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not add course", str(error), parent=courses_tab
            )
            return

        messagebox.showinfo(
            "Course created",
            f"{course.title} was created successfully!",
            parent=courses_tab,
        )
        clear_course_form()
        display_saved_courses()

    def update_selected_course():
        if selected_course_id is None:
            messagebox.showwarning(
                "No course selected",
                "Select a course to update.",
                parent=courses_tab,
            )
            return

        course_id = course_id_entry.get().strip()
        course_title = course_title_entry.get().strip()
        if not course_id:
            messagebox.showwarning(
                "Missing course details",
                "Please enter a course ID.",
                parent=courses_tab,
            )
            return

        try:
            course_price = float(course_price_entry.get())
            course_capacity = int(course_capacity_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid course details",
                "Enter a valid price and whole-number capacity.",
                parent=courses_tab,
            )
            return

        if course_price < 0 or course_capacity <= 0:
            messagebox.showerror(
                "Invalid course details",
                "Price cannot be negative and capacity must be greater than zero.",
                parent=courses_tab,
            )
            return

        course_room_number = course_room_number_entry.get().strip()
        course_address = course_address_entry.get().strip()
        course_meeting_link = None
        if onlinevar.get():
            course_type = "online"
            course_meeting_link = course_meeting_link_entry.get().strip()
            if not course_meeting_link:
                messagebox.showwarning(
                    "Missing course details",
                    "Please provide a meeting link for the online course.",
                    parent=courses_tab,
                )
                return
            course = OnlineCourse(
                selected_course_id,
                course_title,
                course_price,
                course_capacity,
                course_meeting_link,
            )
        elif classroomvar.get():
            course_type = "classroom"
            if not course_room_number or not course_address:
                messagebox.showwarning(
                    "Missing course details",
                    "Please provide both room number and address for the classroom course.",
                    parent=courses_tab,
                )
                return
            course = ClassroomCourse(
                selected_course_id,
                course_title,
                course_price,
                course_capacity,
                course_room_number,
                course_address,
            )
        else:
            messagebox.showwarning(
                "Course type required",
                "Select online or classroom course.",
                parent=courses_tab,
            )
            return

        try:
            update_course(
                selected_course_id,
                course_title,
                course_price,
                course_capacity,
                course_type,
                meeting_link=course_meeting_link,
                room_number=course_room_number or None,
                address=course_address or None,
                new_course_id=course_id,
            )
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not update course", str(error), parent=courses_tab
            )
            return

        messagebox.showinfo(
            "Course updated",
            f"{course.title} was updated successfully!",
            parent=courses_tab,
        )
        clear_course_form()
        display_saved_courses()

    def delete_selected_course():
        if selected_course_id is None:
            messagebox.showwarning(
                "No course selected",
                "Select a course to delete.",
                parent=courses_tab,
            )
            return
        if not messagebox.askyesno(
            "Delete course",
            f"Delete course {selected_course_id}?",
            parent=courses_tab,
        ):
            return

        try:
            delete_course(selected_course_id)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not delete course", str(error), parent=courses_tab
            )
            return

        clear_course_form()
        display_saved_courses()

    course_list.bind("<<TreeviewSelect>>", populate_course_form)
    create_button = tk.Button(
        courses_tab, text="Create Course", command=create_course, width=15, border=3
    )
    create_button.grid(row=8, column=0, pady=10, padx=10)
    course_update_button = tk.Button(
        courses_tab,
        text="Update Course",
        command=update_selected_course,
        width=15,
        border=3,
    )
    course_update_button.grid(row=8, column=1, pady=10, padx=10)
    course_delete_button = tk.Button(
        courses_tab,
        text="Delete Course",
        command=delete_selected_course,
        width=15,
        border=3,
    )
    course_delete_button.grid(row=8, column=2, pady=10, padx=10)

    course_scrollbar = ttk.Scrollbar(
        courses_tab, orient="vertical", command=course_list.yview
    )
    course_horizontal_scrollbar = ttk.Scrollbar(
        courses_tab, orient="horizontal", command=course_list.xview
    )
    course_list.configure(
        yscrollcommand=course_scrollbar.set,
        xscrollcommand=course_horizontal_scrollbar.set,
    )
    course_list.grid(
        row=10, column=0, columnspan=3, sticky="nsew", padx=8, pady=4
    )
    course_scrollbar.grid(row=10, column=3, sticky="ns")
    course_horizontal_scrollbar.grid(
        row=11, column=0, columnspan=3, sticky="ew", padx=8
    )
    courses_tab.columnconfigure(1, weight=1)
    courses_tab.rowconfigure(10, weight=1)
    display_saved_courses()
    return courses_tab
