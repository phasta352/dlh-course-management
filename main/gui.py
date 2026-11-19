#!/usr/bin/env python3
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

if __package__ in (None, ""):
    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from tabs.applications_tab import build_applications_tab
from tabs.courses_tab import build_courses_tab
from db.db import initialize_database
from tabs.students_tab import build_students_tab


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
