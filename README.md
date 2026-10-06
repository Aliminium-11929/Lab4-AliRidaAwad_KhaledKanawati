# School Management System

This project is a school management application developed in Python using both Tkinter and PyQt5.

The application allows users to manage students, instructors, courses, and student enrollments. Both graphical interfaces use the same SQLite database, so changes made in one interface are also available in the other.

The project was developed collaboratively using Git and GitHub.

## Team Members

- Ali Rida Awad - Tkinter interface
- Khaled Kanawati - PyQt5 interface

Both members also contributed to backend integration, testing, documentation, and the final integration of the project.

## Features

The application supports:

- Adding, editing, deleting, and searching for students
- Adding, editing, deleting, and searching for instructors
- Adding, editing, and deleting courses
- Enrolling students in courses
- Unenrolling students from courses
- Importing data from JSON files
- Exporting data to JSON
- Exporting data to CSV
- Backing up the SQLite database
- Restoring the database from a backup
- Tkinter graphical interface
- PyQt5 graphical interface
- Sphinx documentation

## Project Structure

```text
part1_oop.py
part2_tkinter.py
part3_pyqt.py
part4_database.py
school.db
docs/
README.md
```

### `part1_oop.py`

Contains the main object-oriented classes used in the project, including:

- `Person`
- `Student`
- `Instructor`
- `Course`

### `part2_tkinter.py`

Contains the Tkinter graphical interface.

### `part3_pyqt.py`

Contains the PyQt5 graphical interface.

### `part4_database.py`

Handles the SQLite database and the main database operations used by both interfaces.

### `school.db`

Stores the students, instructors, courses, and enrollment information.

### `docs/`

Contains the Sphinx documentation files for the project.

## Requirements

The project requires Python 3.

Tkinter is normally included with standard Python installations.

PyQt5 can be installed using:

```bash
pip install PyQt5
```

The documentation dependencies can be installed using:

```bash
pip install -r docs/requirements.txt
```

## How to Run the Tkinter Interface

Open a terminal in the project folder and run:

```bash
python part2_tkinter.py
```

The Tkinter window will open and allow the user to manage the school data.

The different sections of the interface can be used to manage students, instructors, courses, and enrollments.

## How to Run the PyQt5 Interface

Open a terminal in the project folder and run:

```bash
python part3_pyqt.py
```

If PyQt5 is not installed, install it first using:

```bash
pip install PyQt5
```

The PyQt5 application provides the same main school-management functionality using a PyQt interface.

## Using the Application

Both interfaces connect to the same `school.db` database.

Users can create students and instructors, create courses, assign instructors to courses, and enroll students in courses.

Existing records can also be edited or deleted.

Student, instructor, and course IDs can be updated even when they are linked to other records. The database uses foreign-key update rules to keep related records consistent.

The application also supports importing and exporting data, as well as database backup and restore operations.

## Documentation

The project documentation was created using Sphinx.

To build the documentation, first install the required packages:

```bash
pip install -r docs/requirements.txt
```

Then move to the documentation folder:

```bash
cd docs
```

Build the HTML documentation:

```bash
make html
```

The generated documentation can then be opened from:

```text
docs/_build/html/index.html
```

## Git and GitHub Collaboration

The project was developed using a shared GitHub repository.

Separate branches were used for the two graphical interfaces:

```text
feature-tkinter
feature-pyqt
```

The Tkinter work was developed and committed on the Tkinter branch, while the PyQt5 work was developed and committed on the PyQt branch.

After completing the separate parts, the changes were reviewed and merged into the main branch.

Both members then tested the integrated project and worked on the final documentation and submission.

## Contributions

### Ali Rida Awad

- Developed the Tkinter interface
- Integrated Tkinter with the shared database
- Tested Tkinter functionality
- Contributed to final integration and testing

### Khaled Kanawati

- Developed the PyQt5 interface
- Integrated PyQt5 with the shared database
- Tested PyQt5 functionality
- Contributed to final integration and testing

### Shared Work

Both members contributed to:

- Backend integration
- Database testing
- Final application testing
- Documentation
- GitHub integration
- Final project review

## Final Version

The final version combines the Tkinter and PyQt5 implementations into one project.

Both interfaces use the same OOP classes, database layer, and SQLite database, providing two different graphical interfaces for the same school management system.