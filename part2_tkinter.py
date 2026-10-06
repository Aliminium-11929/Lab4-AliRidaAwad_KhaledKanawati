"""Tkinter interface for managing students, instructors, courses, and enrollments."""

import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from part1_oop import Course, Instructor, Student, load_data, save_data
import part4_database as db


root = None
student_tab = instructor_tab = course_tab = enrollment_tab = records_tab = None
sv = iv = cv = None
student_course = course_inst = None
scb = cinst = None
stree = itree = ctree = enrollment_tree = alltree = None
search_var = None
enroll_student_var = enroll_course_var = None
enroll_student_cb = enroll_course_cb = None
student_old = [None]
instructor_old = [None]
course_old = [None]


def err(error):
    """Display an error message.

    :param error: Exception or message to display.
    """
    messagebox.showerror("Error", str(error))


def entries(frame, labels):
    """Create labeled entry fields.

    :param frame: Parent widget for the fields.
    :param labels: Labels to display beside the fields.
    :return: Entry variables keyed by label.
    :rtype: dict
    """
    result = {}
    for row, label in enumerate(labels):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=4)
        variable = tk.StringVar()
        ttk.Entry(frame, textvariable=variable, width=35).grid(row=row, column=1, padx=5, pady=4)
        result[label] = variable
    return result


def refresh():
    """Reload database records into all tables and selectors."""
    courses = db.get_courses()
    instructors = db.get_instructors()
    students = db.get_students()

    scb["values"] = [row[0] for row in courses]
    cinst["values"] = [""] + [row[0] for row in instructors]

    student_labels = [f"{sid} - {name}" for sid, name, _, _ in students]
    course_labels = [f"{cid} - {name}" for cid, name, _ in courses]
    enroll_student_cb["values"] = student_labels
    enroll_course_cb["values"] = course_labels

    for tree in (stree, itree, ctree, enrollment_tree, alltree):
        for item in tree.get_children():
            tree.delete(item)

    for sid, name, age, email in students:
        stree.insert("", "end", values=(sid, name, age, email, ", ".join(db.get_student_courses(sid))))
    for iid, name, age, email in instructors:
        assigned = ", ".join(row[0] for row in courses if row[2] == iid)
        itree.insert("", "end", values=(iid, name, age, email, assigned))
    for cid, name, iid in courses:
        ctree.insert("", "end", values=(cid, name, iid))

    student_names = {sid: name for sid, name, _, _ in students}
    course_names = {cid: name for cid, name, _ in courses}
    for sid, cid in db.get_enrollments():
        enrollment_tree.insert(
            "",
            "end",
            values=(sid, student_names.get(sid, ""), cid, course_names.get(cid, "")),
        )

    populate_all("")


def add_student():
    """Add a student from the form fields, optionally enrolling them in one course."""
    try:
        student = Student(sv["Name"].get(), sv["Age"].get(), sv["Email"].get(), sv["Student ID"].get())
        db.add_student_db(student.student_id, student.name, student.age, student.email)
        if student_course.get():
            db.enroll_student_db(student.student_id, student_course.get())
        clear_student()
        refresh()
        messagebox.showinfo("Success", "Student added")
    except Exception as error:
        err(error)


def update_student():
    """Update the selected student, optionally adding one course enrollment."""
    try:
        if not student_old[0]:
            raise ValueError("Select a student first")
        student = Student(sv["Name"].get(), sv["Age"].get(), sv["Email"].get(), sv["Student ID"].get())
        db.update_student_db(student_old[0], student.student_id, student.name, student.age, student.email)
        if student_course.get():
            db.enroll_student_db(student.student_id, student_course.get())
        clear_student()
        refresh()
        messagebox.showinfo("Success", "Student updated")
    except Exception as error:
        err(error)


def delete_student():
    """Delete the selected student."""
    try:
        student_id = student_old[0] or sv["Student ID"].get()
        if not student_id:
            raise ValueError("Select a student first")
        db.delete_student_db(student_id)
        clear_student()
        refresh()
    except Exception as error:
        err(error)


def select_student(_event=None):
    """Load the selected student into the form."""
    if not stree.selection():
        return
    values = stree.item(stree.selection()[0], "values")
    student_old[0] = values[0]
    for key, value in zip(("Student ID", "Name", "Age", "Email"), values[:4]):
        sv[key].set(value)
    student_course.set(values[4].split(", ")[0] if values[4] else "")


def clear_student():
    """Clear the student form fields."""
    student_old[0] = None
    for variable in sv.values():
        variable.set("")
    student_course.set("")


def add_instructor():
    """Add an instructor from the form fields."""
    try:
        instructor = Instructor(iv["Name"].get(), iv["Age"].get(), iv["Email"].get(), iv["Instructor ID"].get())
        db.add_instructor_db(instructor.instructor_id, instructor.name, instructor.age, instructor.email)
        clear_instructor()
        refresh()
    except Exception as error:
        err(error)


def update_instructor():
    """Update the selected instructor."""
    try:
        if not instructor_old[0]:
            raise ValueError("Select an instructor first")
        instructor = Instructor(iv["Name"].get(), iv["Age"].get(), iv["Email"].get(), iv["Instructor ID"].get())
        db.update_instructor_db(instructor_old[0], instructor.instructor_id, instructor.name, instructor.age, instructor.email)
        clear_instructor()
        refresh()
    except Exception as error:
        err(error)


def delete_instructor():
    """Delete the selected instructor."""
    try:
        instructor_id = instructor_old[0] or iv["Instructor ID"].get()
        if not instructor_id:
            raise ValueError("Select an instructor first")
        db.delete_instructor_db(instructor_id)
        clear_instructor()
        refresh()
    except Exception as error:
        err(error)


def select_instructor(_event=None):
    """Load the selected instructor into the form."""
    if not itree.selection():
        return
    values = itree.item(itree.selection()[0], "values")
    instructor_old[0] = values[0]
    for key, value in zip(("Instructor ID", "Name", "Age", "Email"), values[:4]):
        iv[key].set(value)


def clear_instructor():
    """Clear the instructor form fields."""
    instructor_old[0] = None
    for variable in iv.values():
        variable.set("")


def add_course():
    """Add a course from the form fields."""
    try:
        course = Course(cv["Course ID"].get(), cv["Course Name"].get(), course_inst.get())
        db.add_course_db(course.course_id, course.course_name, course.instructor)
        clear_course()
        refresh()
    except Exception as error:
        err(error)


def update_course():
    """Update the selected course."""
    try:
        if not course_old[0]:
            raise ValueError("Select a course first")
        course = Course(cv["Course ID"].get(), cv["Course Name"].get(), course_inst.get())
        db.update_course_db(course_old[0], course.course_id, course.course_name, course.instructor)
        clear_course()
        refresh()
    except Exception as error:
        err(error)


def delete_course():
    """Delete the selected course."""
    try:
        course_id = course_old[0] or cv["Course ID"].get()
        if not course_id:
            raise ValueError("Select a course first")
        db.delete_course_db(course_id)
        clear_course()
        refresh()
    except Exception as error:
        err(error)


def select_course(_event=None):
    """Load the selected course into the form."""
    if not ctree.selection():
        return
    values = ctree.item(ctree.selection()[0], "values")
    course_old[0] = values[0]
    cv["Course ID"].set(values[0])
    cv["Course Name"].set(values[1])
    course_inst.set(values[2])


def clear_course():
    """Clear the course form fields."""
    course_old[0] = None
    for variable in cv.values():
        variable.set("")
    course_inst.set("")


def _selected_id(label):
    """Extract the identifier from a ``ID - name`` selector value."""
    return label.split(" - ", 1)[0].strip() if label else ""


def enroll_student():
    """Enroll the selected student in the selected course."""
    try:
        student_id = _selected_id(enroll_student_var.get())
        course_id = _selected_id(enroll_course_var.get())
        if not student_id or not course_id:
            raise ValueError("Select both a student and a course")
        changed = db.enroll_student_db(student_id, course_id)
        refresh()
        if changed:
            messagebox.showinfo("Enrollment", "Student enrolled successfully")
        else:
            messagebox.showinfo("Enrollment", "Student is already enrolled in that course")
    except Exception as error:
        err(error)


def unenroll_student():
    """Remove the selected student-course enrollment."""
    try:
        selection = enrollment_tree.selection()
        if not selection:
            raise ValueError("Select an enrollment first")
        values = enrollment_tree.item(selection[0], "values")
        student_id, course_id = values[0], values[2]
        if not messagebox.askyesno("Confirm Unenroll", f"Unenroll {student_id} from {course_id}?"):
            return
        db.unenroll_student_db(student_id, course_id)
        refresh()
        messagebox.showinfo("Enrollment", "Student unenrolled successfully")
    except Exception as error:
        err(error)


def populate_all(term):
    """Search for and display combined records.

    :param term: Search text, or an empty string for all records.
    """
    for item in alltree.get_children():
        alltree.delete(item)
    if term:
        rows = db.search_records(term)
    else:
        rows = (
            [("Student", row[0], row[1], row[3]) for row in db.get_students()]
            + [("Instructor", row[0], row[1], row[3]) for row in db.get_instructors()]
            + [("Course", row[0], row[1], row[2]) for row in db.get_courses()]
        )
    for row in rows:
        alltree.insert("", "end", values=row)


def save_json():
    """Save the database data to a JSON file."""
    path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
    if not path:
        return
    data = {
        "students": [Student(name, age, email, sid, db.get_student_courses(sid)) for sid, name, age, email in db.get_students()],
        "instructors": [Instructor(name, age, email, iid, [c[0] for c in db.get_courses() if c[2] == iid]) for iid, name, age, email in db.get_instructors()],
        "courses": [Course(cid, name, iid, [sid for sid, course_id in db.get_enrollments() if course_id == cid]) for cid, name, iid in db.get_courses()],
    }
    save_data(data, path)
    messagebox.showinfo("Saved", path)


def load_json_gui():
    """Load database data from a JSON file."""
    path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    if not path:
        return
    try:
        data = load_data(path)
        with db.connect_db() as connection:
            connection.execute("DELETE FROM enrollments")
            connection.execute("DELETE FROM courses")
            connection.execute("DELETE FROM instructors")
            connection.execute("DELETE FROM students")
        for student in data.get("students", []):
            db.add_student_db(student.student_id, student.name, student.age, student.email)
        for instructor in data.get("instructors", []):
            db.add_instructor_db(instructor.instructor_id, instructor.name, instructor.age, instructor.email)
        for course in data.get("courses", []):
            db.add_course_db(course.course_id, course.course_name, course.instructor)
        for student in data.get("students", []):
            for course_id in student.registered_courses:
                db.enroll_student_db(student.student_id, course_id)
        refresh()
        messagebox.showinfo("Loaded", "JSON data restored")
    except Exception as error:
        err(error)


def export_csv():
    """Export students, instructors, and courses to one CSV file."""
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if not path:
        return
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "ID", "Name", "Age", "Email", "Course/Instructor"])
        courses = db.get_courses()
        for sid, name, age, email in db.get_students():
            writer.writerow(["Student", sid, name, age, email, ", ".join(db.get_student_courses(sid))])
        for iid, name, age, email in db.get_instructors():
            writer.writerow(["Instructor", iid, name, age, email, ", ".join(c[0] for c in courses if c[2] == iid)])
        for cid, name, iid in courses:
            writer.writerow(["Course", cid, name, "", "", iid])
    messagebox.showinfo("Export", "CSV exported successfully")


def backup_database():
    """Create a backup of the SQLite database."""
    try:
        messagebox.showinfo("Backup", db.backup_db())
    except Exception as error:
        err(error)


def restore_database():
    """Restore the SQLite database from the default backup file."""
    try:
        db.restore_db()
        refresh()
        messagebox.showinfo("Restore", "Database restored")
    except Exception as error:
        err(error)


def build_interface():
    """Construct and return the Tkinter application window."""
    global root, student_tab, instructor_tab, course_tab, enrollment_tab, records_tab
    global sv, iv, cv, student_course, course_inst, scb, cinst
    global stree, itree, ctree, enrollment_tree, alltree, search_var
    global enroll_student_var, enroll_course_var, enroll_student_cb, enroll_course_cb

    db.setup_db().close()
    root = tk.Tk()
    root.title("School Management System - Tkinter")
    root.geometry("1050x700")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)
    student_tab, instructor_tab, course_tab, enrollment_tab, records_tab = [ttk.Frame(notebook) for _ in range(5)]
    for frame, title in zip(
        (student_tab, instructor_tab, course_tab, enrollment_tab, records_tab),
        ("Students", "Instructors", "Courses", "Enrollment", "All Records / Search"),
    ):
        notebook.add(frame, text=title)

    sv = entries(student_tab, ["Student ID", "Name", "Age", "Email"])
    ttk.Label(student_tab, text="Course").grid(row=4, column=0, sticky="w", padx=5, pady=4)
    student_course = tk.StringVar()
    scb = ttk.Combobox(student_tab, textvariable=student_course, state="readonly", width=32)
    scb.grid(row=4, column=1, padx=5, pady=4)
    stree = ttk.Treeview(student_tab, columns=("id", "name", "age", "email", "courses"), show="headings", height=13)
    for column, title, width in (("id", "ID", 100), ("name", "Name", 160), ("age", "Age", 60), ("email", "Email", 220), ("courses", "Registered Courses", 260)):
        stree.heading(column, text=title)
        stree.column(column, width=width)
    stree.grid(row=7, column=0, columnspan=4, sticky="nsew", padx=5, pady=8)
    stree.bind("<<TreeviewSelect>>", select_student)
    for column, (text, command) in enumerate((("Add", add_student), ("Edit", update_student), ("Delete", delete_student), ("Clear", clear_student))):
        ttk.Button(student_tab, text=text, command=command).grid(row=5, column=column, padx=4, pady=6)

    iv = entries(instructor_tab, ["Instructor ID", "Name", "Age", "Email"])
    itree = ttk.Treeview(instructor_tab, columns=("id", "name", "age", "email", "courses"), show="headings", height=14)
    for column, title, width in (("id", "ID", 110), ("name", "Name", 170), ("age", "Age", 60), ("email", "Email", 220), ("courses", "Assigned Courses", 270)):
        itree.heading(column, text=title)
        itree.column(column, width=width)
    itree.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=5, pady=8)
    itree.bind("<<TreeviewSelect>>", select_instructor)
    for column, (text, command) in enumerate((("Add", add_instructor), ("Edit", update_instructor), ("Delete", delete_instructor), ("Clear", clear_instructor))):
        ttk.Button(instructor_tab, text=text, command=command).grid(row=4, column=column, padx=4, pady=6)

    cv = entries(course_tab, ["Course ID", "Course Name"])
    ttk.Label(course_tab, text="Instructor").grid(row=2, column=0, sticky="w", padx=5, pady=4)
    course_inst = tk.StringVar()
    cinst = ttk.Combobox(course_tab, textvariable=course_inst, state="readonly", width=32)
    cinst.grid(row=2, column=1, padx=5, pady=4)
    ctree = ttk.Treeview(course_tab, columns=("id", "name", "instructor"), show="headings", height=15)
    for column, title, width in (("id", "Course ID", 160), ("name", "Course Name", 300), ("instructor", "Instructor ID", 200)):
        ctree.heading(column, text=title)
        ctree.column(column, width=width)
    ctree.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=8)
    ctree.bind("<<TreeviewSelect>>", select_course)
    for column, (text, command) in enumerate((("Add", add_course), ("Edit", update_course), ("Delete", delete_course), ("Clear", clear_course))):
        ttk.Button(course_tab, text=text, command=command).grid(row=3, column=column, padx=4, pady=6)

    enrollment_form = ttk.LabelFrame(enrollment_tab, text="Manage Enrollment")
    enrollment_form.pack(fill="x", padx=8, pady=8)
    ttk.Label(enrollment_form, text="Student").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    enroll_student_var = tk.StringVar()
    enroll_student_cb = ttk.Combobox(enrollment_form, textvariable=enroll_student_var, state="readonly", width=40)
    enroll_student_cb.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(enrollment_form, text="Course").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    enroll_course_var = tk.StringVar()
    enroll_course_cb = ttk.Combobox(enrollment_form, textvariable=enroll_course_var, state="readonly", width=40)
    enroll_course_cb.grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(enrollment_form, text="Enroll", command=enroll_student).grid(row=2, column=0, columnspan=2, pady=6)

    enrollment_tree = ttk.Treeview(enrollment_tab, columns=("sid", "student", "cid", "course"), show="headings", height=16)
    for column, title, width in (("sid", "Student ID", 130), ("student", "Student Name", 220), ("cid", "Course ID", 130), ("course", "Course Name", 240)):
        enrollment_tree.heading(column, text=title)
        enrollment_tree.column(column, width=width)
    enrollment_tree.pack(fill="both", expand=True, padx=8, pady=8)
    ttk.Button(enrollment_tab, text="Unenroll Selected", command=unenroll_student).pack(pady=(0, 8))

    search_var = tk.StringVar()
    ttk.Label(records_tab, text="Search by name, ID, email, or course:").pack(anchor="w", padx=8, pady=(8, 2))
    ttk.Entry(records_tab, textvariable=search_var, width=50).pack(anchor="w", padx=8)
    alltree = ttk.Treeview(records_tab, columns=("type", "id", "name", "details"), show="headings", height=18)
    for column, title, width in (("type", "Type", 100), ("id", "ID", 150), ("name", "Name / Course", 250), ("details", "Email / Instructor", 300)):
        alltree.heading(column, text=title)
        alltree.column(column, width=width)
    alltree.pack(fill="both", expand=True, padx=8, pady=8)
    search_var.trace_add("write", lambda *_: populate_all(search_var.get()))

    button_frame = ttk.Frame(records_tab)
    button_frame.pack(fill="x", padx=8, pady=5)
    for text, command in (
        ("Save JSON", save_json),
        ("Load JSON", load_json_gui),
        ("Export CSV", export_csv),
        ("Backup DB", backup_database),
        ("Restore DB", restore_database),
    ):
        ttk.Button(button_frame, text=text, command=command).pack(side="left", padx=4)

    refresh()
    return root


def main():
    """Start the Tkinter application."""
    build_interface().mainloop()


if __name__ == "__main__":
    main()
