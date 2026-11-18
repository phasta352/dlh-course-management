#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("training_center.db")

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
    conn.commit()

def add_student(student_id, name, email):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO students (student_id, name, email) VALUES (?, ?, ?)",(student_id, name, email))
        conn.commit()

def add_course(course_id, title, price, capacity, course_type, meeting_link=None, room_number=None, address=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""INSERT INTO courses (course_id, title, price, capacity, course_type, meeting_link, room_number, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (course_id, title, price, capacity, course_type, meeting_link, room_number, address))
        conn.commit()