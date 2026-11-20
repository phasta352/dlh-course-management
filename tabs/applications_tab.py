import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from main.create_fields import add_field
from db.db import (
    APPLICATION_STATUSES,
    add_application,
    delete_application,
    get_applications,
    update_application,
)


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
        columns=("application_id", "company", "job_title", "status"),
        show="headings",
    )
    selected_application_id = None
    for column, heading, width in (
        ("application_id", "ID", 60),
        ("company", "Company", 180),
        ("job_title", "Job Title", 220),
        ("status", "Status", 110),
    ):
        application_list.heading(column, text=heading)
        application_list.column(column, width=width, stretch=False)

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

        clear_form()
        for item in application_list.get_children():
            application_list.delete(item)
        for application in applications:
            application_list.insert("", tk.END, values=application)

    def clear_form():
        nonlocal selected_application_id
        selected_application_id = None
        company_entry.delete(0, tk.END)
        job_title_entry.delete(0, tk.END)
        application_status.set(APPLICATION_STATUSES[0])
        application_list.selection_remove(application_list.selection())

    def populate_form(_event=None):
        nonlocal selected_application_id
        selection = application_list.selection()
        if not selection:
            return

        application_id, company, job_title, status = application_list.item(
            selection[0], "values"
        )
        selected_application_id = int(application_id)
        company_entry.delete(0, tk.END)
        company_entry.insert(0, company)
        job_title_entry.delete(0, tk.END)
        job_title_entry.insert(0, job_title)
        application_status.set(status)

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

        clear_form()
        display_saved_applications()

    def update_selected_application():
        if selected_application_id is None:
            messagebox.showwarning(
                "No application selected",
                "Select an application to update.",
                parent=applications_tab,
            )
            return

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
            update_application(
                selected_application_id, company, job_title, status
            )
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not update application",
                str(error),
                parent=applications_tab,
            )
            return

        clear_form()
        display_saved_applications()

    def delete_selected_application():
        if selected_application_id is None:
            messagebox.showwarning(
                "No application selected",
                "Select an application to delete.",
                parent=applications_tab,
            )
            return
        if not messagebox.askyesno(
            "Delete application",
            f"Delete the application for {company_entry.get()}?",
            parent=applications_tab,
        ):
            return

        try:
            delete_application(selected_application_id)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Could not delete application",
                str(error),
                parent=applications_tab,
            )
            return

        clear_form()
        display_saved_applications()

    application_list.bind("<<TreeviewSelect>>", populate_form)
    create_application_button = tk.Button(
        applications_tab,
        text="Create Application",
        command=save_application,
        width=18,
        border=3,
    )
    create_application_button.grid(row=3, column=0, pady=10, padx=10)
    application_update_button = tk.Button(
        applications_tab,
        text="Update Application",
        command=update_selected_application,
        width=18,
        border=3,
    )
    application_update_button.grid(row=3, column=1, pady=10, padx=10)
    application_delete_button = tk.Button(
        applications_tab,
        text="Delete Application",
        command=delete_selected_application,
        width=18,
        border=3,
    )
    application_delete_button.grid(row=3, column=2, pady=10, padx=10)
    application_list.grid(
        row=4, column=0, columnspan=4, sticky="nsew", padx=8, pady=4
    )
    applications_tab.columnconfigure(1, weight=1)
    applications_tab.rowconfigure(4, weight=1)
    display_saved_applications()
    return applications_tab
