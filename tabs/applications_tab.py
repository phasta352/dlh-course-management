import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from create_fields import add_field
from db.db import APPLICATION_STATUSES, add_application, get_applications


def build_applications_tab(notebook):
    applications_tab = ttk.Frame(notebook)
    notebook.add(applications_tab, text="Applications")

    company_label, company_entry = add_field(
        applications_tab, "Company", 0, 0, width=30
    )
    job_title_label, job_title_entry = add_field(
        applications_tab, "Job Title", 1, 0, width=30
    )
    tk.Label(applications_tab, text="Status").grid(
        row=2, column=0, sticky="w", padx=8, pady=4
    )
    application_status = ttk.Combobox(
        applications_tab,
        values=APPLICATION_STATUSES,
        state="readonly",
        width=27,
    )
    application_status.grid(row=2, column=1, sticky="w")
    application_status.set(APPLICATION_STATUSES[0])

    application_list = ttk.Treeview(
        applications_tab,
        columns=("company", "job_title", "status"),
        show="headings",
    )
    application_list.heading("company", text="Company")
    application_list.heading("job_title", text="Job Title")
    application_list.heading("status", text="Status")

    def display_saved_applications():
        try:
            applications = get_applications()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not load applications",
                str(error),
                parent=applications_tab,
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
                parent=applications_tab,
            )
            return

        try:
            add_application(company, job_title, status)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not save application",
                str(error),
                parent=applications_tab,
            )
            return

        company_entry.delete(0, tk.END)
        job_title_entry.delete(0, tk.END)
        display_saved_applications()

    save_application_button = tk.Button(
        applications_tab,
        text="Save Application",
        command=save_application,
        width=18,
        border=3,
    )
    save_application_button.grid(row=3, column=1, pady=10, padx=10)
    application_list.grid(
        row=4, column=0, columnspan=2, sticky="nsew", padx=8, pady=4
    )
    applications_tab.columnconfigure(1, weight=1)
    applications_tab.rowconfigure(4, weight=1)
    display_saved_applications()
    return applications_tab
