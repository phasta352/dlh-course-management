import tkinter as tk
from courses import *

def show_course_id():
    result_label.config(text=f"{course_id_entry.get()}: {course_title_entry.get()} - ${course_price_entry.get()} ({course_capacity_entry.get()} seats available)")

def create_online_course():
    course_id = course_id_entry.get()
    course_title = course_title_entry.get()
    course_price = float(course_price_entry.get())
    course_capacity = int(course_capacity_entry.get())
    course_meeting_link = course_meeting_link_entry.get()
    
    if course_meeting_link:
        course = OnlineCourse(course_id, course_title, course_price, course_capacity, course_meeting_link)
        courses.append(course)
        result_label.config(text=f"{course.title} created successfully! Number of courses: {len(courses)}")
    else:
        result_label.config(text="Please provide a meeting link for the online course.")

def create_classroom_course():
    course_id = course_id_entry.get()
    course_title = course_title_entry.get()
    course_price = float(course_price_entry.get())
    course_capacity = int(course_capacity_entry.get())
    course_room_number = course_room_number_entry.get()
    course_address = course_address_entry.get()
    
    if course_room_number and course_address:
        course = ClassroomCourse(course_id, course_title, course_price, course_capacity, course_room_number, course_address)
        courses.append(course)
        result_label.config(text=f"{course.title} created successfully! Number of courses: {len(courses)}")
    else:
        result_label.config(text="Please provide both room number and address for the classroom course.")

window = tk.Tk()
window.title("Course Management")
courses = []

course_id_label = tk.Label(window, text="Course Id")
course_id_label.grid(row=0, column=0, sticky="w", padx=8, pady= 4)
course_id_entry = tk.Entry(window, width=10, border=3)
course_id_entry.grid(row=0, column=1, sticky="w")

course_title_label = tk.Label(window, text="Course Title")
course_title_label.grid(row=1, column=0, sticky="w", padx=8, pady= 4)
course_title_entry = tk.Entry(window, width=30, border=3)
course_title_entry.grid(row=1, column=1)

course_price_label = tk.Label(window, text="Course Price")
course_price_label.grid(row=2, column=0, sticky="w", padx=8, pady= 4)
course_price_entry = tk.Entry(window, width=10, border=3)
course_price_entry.grid(row=2, column=1, sticky="w")

course_capacity_label = tk.Label(window, text="Course Capacity")
course_capacity_label.grid(row=3, column=0, sticky="w", padx=8, pady= 4)
course_capacity_entry = tk.Entry(window, width=10, border=3)
course_capacity_entry.grid(row=3, column=1, sticky="w")

course_meeting_link_label = tk.Label(window, text="Course Meeting Link")
course_meeting_link_label.grid(row=4, column=0, sticky="w", padx=8, pady= 4)
course_meeting_link_entry = tk.Entry(window, width=30, border=3)
course_meeting_link_entry.grid(row=4, column=1)

course_room_number_label = tk.Label(window, text="Course Room Number")
course_room_number_label.grid(row=5, column=0, sticky="w", padx=8, pady= 4)
course_room_number_entry = tk.Entry(window, width=10, border=3)
course_room_number_entry.grid(row=5, column=1, sticky="w")

course_address_label = tk.Label(window, text="Course Address")
course_address_label.grid(row=6, column=0, sticky="w", padx=8, pady= 4)
course_address_entry = tk.Entry(window, width=30, border=3)
course_address_entry.grid(row=6, column=1)

button = tk.Button(window, text="Create Online Course", command=create_online_course, width=15, border=3)
button.grid(row=7, column=0, columnspan=1, pady=10)

button = tk.Button(window, text="Create Classroom Course", command=create_classroom_course, width=15, border=3)
button.grid(row=7, column=1, columnspan=1, pady=10, padx=10)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

window.mainloop()