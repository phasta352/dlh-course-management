#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

from applications_tab import build_applications_tab
from courses_tab import build_courses_tab
from db import initialize_database
from students_tab import build_students_tab


def main():
    initialize_database()

    window = tk.Tk()
    window.title("Course Management")

    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", pady=10, expand=True)
    build_courses_tab(notebook)
    build_students_tab(notebook)
    build_applications_tab(notebook)

    window.mainloop()

if __name__ == "__main__":
    main()
