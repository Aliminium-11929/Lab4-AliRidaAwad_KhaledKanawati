"""SQLite persistence and relationship operations for the school system."""

import os
import shutil
import sqlite3
import logging
from contextlib import closing

DB_FILE = "school.db"
BACKUP_FILE = "school_backup.db"
logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(message)s")

def connect_db():
    """Open the SQLite database with foreign-key checks enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def setup_db():
    """Create the application tables when they do not already exist."""
    conn = connect_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL CHECK(age >= 0), email TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS instructors(
        instructor_id TEXT PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL CHECK(age >= 0), email TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS courses(
        course_id TEXT PRIMARY KEY, course_name TEXT NOT NULL,
        instructor_id TEXT, FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL ON UPDATE CASCADE);
    CREATE TABLE IF NOT EXISTS enrollments(
        student_id TEXT NOT NULL, course_id TEXT NOT NULL,
        PRIMARY KEY(student_id, course_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE);
    """)
    conn.commit()
    return conn

def execute(query, params=()):
    """Execute a write query and return the affected row count."""
    with closing(connect_db()) as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.rowcount

def fetch_all(query, params=()):
    """Execute a query and return all result rows."""
    with closing(connect_db()) as conn:
        return conn.execute(query, params).fetchall()

"""Student CRUD operations."""
def add_student_db(student_id, name, age, email):
    """Insert a student and return the affected row count."""
    return execute("INSERT INTO students VALUES(?,?,?,?)", (student_id,name,age,email))
def get_students():
    """Return all students ordered by identifier."""
    return fetch_all("SELECT student_id,name,age,email FROM students ORDER BY student_id")
def update_student_db(old_id, student_id, name, age, email):
    """Update a student identifier and profile fields."""
    return execute("UPDATE students SET student_id=?,name=?,age=?,email=? WHERE student_id=?", (student_id,name,age,email,old_id))
def delete_student_db(student_id):
    """Delete a student by identifier."""
    return execute("DELETE FROM students WHERE student_id=?", (student_id,))

"""Instructor CRUD operations."""
def add_instructor_db(instructor_id, name, age, email):
    """Insert an instructor and return the affected row count."""
    return execute("INSERT INTO instructors VALUES(?,?,?,?)", (instructor_id,name,age,email))
def get_instructors():
    """Return all instructors ordered by identifier."""
    return fetch_all("SELECT instructor_id,name,age,email FROM instructors ORDER BY instructor_id")
def update_instructor_db(old_id, instructor_id, name, age, email):
    """Update an instructor identifier and profile fields."""
    return execute("UPDATE instructors SET instructor_id=?,name=?,age=?,email=? WHERE instructor_id=?", (instructor_id,name,age,email,old_id))
def delete_instructor_db(instructor_id):
    """Delete an instructor by identifier."""
    return execute("DELETE FROM instructors WHERE instructor_id=?", (instructor_id,))

"""Course CRUD operations."""
def add_course_db(course_id, course_name, instructor_id=None):
    """Insert a course and return the affected row count."""
    return execute("INSERT INTO courses VALUES(?,?,?)", (course_id,course_name,instructor_id or None))
def get_courses():
    """Return all courses ordered by identifier."""
    return fetch_all("SELECT course_id,course_name,COALESCE(instructor_id,'') FROM courses ORDER BY course_id")
def update_course_db(old_id, course_id, course_name, instructor_id=None):
    """Update a course identifier, name, and instructor."""
    return execute("UPDATE courses SET course_id=?,course_name=?,instructor_id=? WHERE course_id=?", (course_id,course_name,instructor_id or None,old_id))
def delete_course_db(course_id):
    """Delete a course by identifier."""
    return execute("DELETE FROM courses WHERE course_id=?", (course_id,))
def assign_instructor_db(course_id, instructor_id):
    """Assign or clear an instructor for a course."""
    return execute("UPDATE courses SET instructor_id=? WHERE course_id=?", (instructor_id or None,course_id))

"""Enrollment and relationship operations."""
def enroll_student_db(student_id, course_id):
    """Enroll a student in a course without duplicating a relationship."""
    return execute("INSERT OR IGNORE INTO enrollments VALUES(?,?)", (student_id,course_id))
def unenroll_student_db(student_id, course_id):
    """Remove one student-course relationship."""
    return execute("DELETE FROM enrollments WHERE student_id=? AND course_id=?", (student_id,course_id))
def get_enrollments():
    """Return all student-course relationships."""
    return fetch_all("SELECT student_id,course_id FROM enrollments ORDER BY student_id,course_id")
def get_student_courses(student_id):
    """Return course identifiers registered by one student."""
    return [r[0] for r in fetch_all("SELECT course_id FROM enrollments WHERE student_id=? ORDER BY course_id", (student_id,))]

def search_records(term):
    """Search students, instructors, and courses by related text."""
    q = f"%{term}%"
    students = fetch_all("SELECT 'Student',student_id,name,email FROM students WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ? OR student_id IN (SELECT student_id FROM enrollments WHERE course_id LIKE ?)", (q,q,q,q))
    instructors = fetch_all("SELECT 'Instructor',instructor_id,name,email FROM instructors WHERE instructor_id LIKE ? OR name LIKE ? OR email LIKE ? OR instructor_id IN (SELECT instructor_id FROM courses WHERE course_id LIKE ? OR course_name LIKE ?)", (q,q,q,q,q))
    courses = fetch_all("SELECT 'Course',course_id,course_name,COALESCE(instructor_id,'') FROM courses WHERE course_id LIKE ? OR course_name LIKE ? OR instructor_id LIKE ?", (q,q,q))
    return students + instructors + courses

def backup_db(destination=BACKUP_FILE):
    """Copy the active database to a backup file and return its path."""
    setup_db().close()
    shutil.copy2(DB_FILE, destination)
    logging.info("Database backed up to %s", destination)
    return destination

def restore_db(source=BACKUP_FILE):
    """Replace the active database with a previously saved backup."""
    if not os.path.exists(source):
        raise FileNotFoundError(f"Backup file not found: {source}")
    shutil.copy2(source, DB_FILE)
    setup_db().close()
    logging.info("Database restored from %s", source)
    return DB_FILE

if __name__ == "__main__":
    setup_db().close()
    print("Database ready with students, instructors, courses, and enrollments tables.")
    print("CRUD, search, backup, and restore functions are available for the GUIs.")
