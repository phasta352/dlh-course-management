# DLH Course Management

A desktop application for managing a training centre's **courses**, **students** and **job applications**. It is built with Python's **Tkinter** for the interface and **SQLite** for storage, so it runs without any external dependencies.

## Features

The app opens a single window with three tabs:

### Courses
- Create, update and delete courses
- Two course types, each with its own required fields:
  - **Online course**: needs a meeting link
  - **Classroom course**: needs a room number and an address
- Checks the input: price can't be negative, and capacity must be a whole number greater than zero
- All saved courses are listed in a scrollable table. Click a row to load it into the form for editing

### Students
- Create, update and delete students (ID, name, email)
- Email addresses must be unique

### Applications
- Track job applications by company, job title and status
- Status is picked from a fixed list: `Applied`, `Interview`, `Offer`, `Rejected`
- Create, update and delete entries from the table

Deletions ask for confirmation first, and database errors appear as pop-up messages instead of crashing the app.

## Tech stack

| Part        | Technology                     |
|-------------|--------------------------------|
| Language    | Python 3                       |
| GUI         | Tkinter / ttk (`Notebook`, `Treeview`) |
| Database    | SQLite (`sqlite3` standard library) |
| Design      | Object-oriented course model with inheritance |

## Project structure

```
dlh-course-management/
├── main/
│   ├── gui.py            # Entry point: builds the window and tabs
│   ├── courses.py        # Course base class + OnlineCourse / ClassroomCourse
│   └── create_fields.py  # Helper for creating label + entry pairs
├── tabs/
│   ├── courses_tab.py       # Courses tab (form, table, CRUD buttons)
│   ├── students_tab.py      # Students tab
│   └── applications_tab.py  # Applications tab
├── db/
│   └── db.py             # Database setup and all CRUD queries
└── .gitignore
```

## Getting started

### Requirements
- Python 3.8 or newer
- Tkinter, which comes with the standard Python installers for Windows and macOS. On Linux you may need to install it separately:
  ```bash
  sudo apt install python3-tk
  ```

No `pip install` is needed. The project uses only the standard library.

### Run the app

```bash
git clone https://github.com/phasta352/dlh-course-management.git
cd dlh-course-management
python main/gui.py
```

You can also run it as a module from the project root:

```bash
python -m main.gui
```

The first time the app runs, it creates an SQLite database at `db/training_center.db`. That file is excluded from version control in `.gitignore`.

## Database schema

**students**
| Column       | Type | Notes                 |
|--------------|------|-----------------------|
| student_id   | TEXT | Primary key           |
| name         | TEXT | Required              |
| email        | TEXT | Required, unique      |

**courses**
| Column       | Type    | Notes                              |
|--------------|---------|------------------------------------|
| course_id    | TEXT    | Primary key                        |
| title        | TEXT    | Required                           |
| price        | REAL    | Required, `>= 0`                   |
| capacity     | INTEGER | Required, `> 0`                    |
| course_type  | TEXT    | `online` or `classroom`            |
| meeting_link | TEXT    | Used by online courses             |
| room_number  | TEXT    | Used by classroom courses          |
| address      | TEXT    | Used by classroom courses          |

**applications**
| Column         | Type    | Notes                                         |
|----------------|---------|-----------------------------------------------|
| application_id | INTEGER | Primary key, auto-increment                   |
| company        | TEXT    | Required, cannot be blank                     |
| job_title      | TEXT    | Required, cannot be blank                     |
| status         | TEXT    | One of `Applied`, `Interview`, `Offer`, `Rejected` |

## OOP design

`main/courses.py` demonstrates the core object-oriented concepts used in the project:

- **Encapsulation**: `price` and `capacity` are stored as private attributes (`__price`, `__capacity`) and accessed through getters and setters that validate the values
- **Inheritance**: `OnlineCourse` and `ClassroomCourse` both extend the `Course` base class
- **Polymorphism**: each subclass implements its own `joining_instructions()` method, returning either the meeting link or the room and address

## Author

Created by [phasta352](https://github.com/phasta352) as a class project for the DLH course.
