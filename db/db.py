#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("training_center.db")
APPLICATION_STATUSES = ("Applied", "Interview", "Offer", "Rejected")

# Initialize the database and create tables if they don't exist --------------------------------------
def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE)""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                capacity INTEGER NOT NULL CHECK(capacity > 0),
                course_type TEXT NOT NULL,
                meeting_link TEXT,
                room_number TEXT,
                address TEXT)""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL CHECK (trim(company) <> ''),
                job_title TEXT NOT NULL CHECK (trim(job_title) <> ''),
                status TEXT NOT NULL CHECK (
                    status IN ('Applied', 'Interview', 'Offer', 'Rejected')
                ))""")
    conn.commit()


# Functions for adding and retrieving students, courses, and applications --------------------------------------
def add_student(student_id, name, email):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO students (student_id, name, email) VALUES (?, ?, ?)",(student_id, name, email))
        conn.commit()

def add_course(course_id, title, price, capacity, course_type, meeting_link=None, room_number=None, address=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""INSERT INTO courses (course_id, title, price, capacity, course_type, meeting_link, room_number, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (course_id, title, price, capacity, course_type, meeting_link, room_number, address))
        conn.commit()

def get_students():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            """SELECT student_id, name, email
               FROM students
               ORDER BY student_id"""
        ).fetchall()

def get_courses():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            """SELECT course_id, title, course_type, price, capacity,
                      meeting_link, room_number, address
               FROM courses
               ORDER BY course_id"""
        ).fetchall()

def add_application(company, job_title, status):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO applications (company, job_title, status) VALUES (?, ?, ?)",
            (company, job_title, status),
        )
        conn.commit()

def get_applications():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            """SELECT company, job_title, status
               FROM applications
               ORDER BY application_id"""
        ).fetchall()

    
# Update functions for students, courses, and applications --------------------------------------
def update_student(student_id, name, email):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE students SET name = ?, email = ? WHERE student_id = ?",
            (name, email, student_id),
        )
        conn.commit()

def update_course(course_id, title, price, capacity, course_type, meeting_link=None, room_number=None, address=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """UPDATE courses
               SET title = ?, price = ?, capacity = ?, course_type = ?,
                   meeting_link = ?, room_number = ?, address = ?
               WHERE course_id = ?""",
            (title, price, capacity, course_type, meeting_link, room_number, address, course_id),
        )
        conn.commit()

def update_application(application_id, company, job_title, status):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE applications SET company = ?, job_title = ?, status = ? WHERE application_id = ?",
            (company, job_title, status, application_id),
        )
        conn.commit()