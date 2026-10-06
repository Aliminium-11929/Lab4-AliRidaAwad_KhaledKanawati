# School Management System

This project is a simple school management application built in Python. It allows users to manage students, instructors, courses, and course enrollments through both Tkinter and PyQt5 interfaces.

The project also includes an SQLite database for storing the application data and Sphinx documentation for the main classes, functions, and GUI components.

## Features

- Add, edit, delete, and search for students
- Add, edit, delete, and search for instructors
- Add, edit, and delete courses
- Enroll and unenroll students from courses
- Export data to JSON and CSV
- Import data from JSON
- Backup and restore the SQLite database
- Two graphical interfaces:
  - Tkinter
  - PyQt5
- Sphinx-generated documentation

## Project Files

- `part1_oop.py` - Contains the main OOP classes such as `Person`, `Student`, `Instructor`, and `Course`
- `part2_tkinter.py` - Tkinter version of the graphical interface
- `part3_pyqt.py` - PyQt5 version of the graphical interface
- `part4_database.py` - Handles SQLite database operations
- `school.db` - SQLite database used by the application
- `docs/` - Contains the Sphinx documentation files

## Running the Project

Make sure Python is installed.

For the Tkinter interface:

```bash
python part2_tkinter.py
```

For the PyQt5 interface:

```bash
python part3_pyqt.py
```

PyQt5 may need to be installed first:

```bash
pip install -r requirements.txt
```

## Documentation

The project uses Sphinx for documentation.

Build the documentation using:

```bash
make html
```

The generated documentation can then be opened from:

```text
docs/_build/html/index.html
```

## Notes

The Tkinter and PyQt5 applications use the same underlying database, so changes made through either interface are stored in the same `school.db` file.

The project was developed as part of Lab 3 and focuses on applying object-oriented programming, graphical interfaces, database integration, and Python documentation.
