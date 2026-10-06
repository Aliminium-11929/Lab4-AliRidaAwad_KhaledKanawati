"""Domain models and JSON persistence for the school management system."""

import json
import logging
import re

logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(message)s")

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def sanitize_input(value, max_length=100):
    """Strip surrounding whitespace and limit a value to a safe length.

    Args:
        value: Value to convert to text.
        max_length (int): Maximum number of characters to keep.

    Returns:
        str: Cleaned text value.
    """
    return str(value).strip()[:max_length]

class Person:
    """Base model containing shared identity and contact information."""

    def __init__(self, name, age, email):
        """Create a person after validating name, age, and email."""
        self.name = sanitize_input(name)
        self._email = sanitize_input(email)
        if not self.name:
            raise ValueError("Name is required")
        try:
            self.age = int(age)
        except (TypeError, ValueError):
            raise ValueError("Age must be an integer")
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if not EMAIL_RE.fullmatch(self._email):
            raise ValueError("Invalid email format")

    @property
    def email(self):
        """Return the validated email address."""
        return self._email

    def introduce(self):
        """Return a short introduction for the person."""
        return f"Hi, I'm {self.name}, age {self.age}."

    def _person_dict(self):
        """Return the fields shared by serialized person models."""
        return {"name": self.name, "age": self.age, "email": self._email}

class Student(Person):
    """Person who can register for courses."""

    def __init__(self, name, age, email, student_id, registered_courses=None):
        """Create a student with an identifier and optional courses."""
        super().__init__(name, age, email)
        self.student_id = sanitize_input(student_id)
        if not self.student_id:
            raise ValueError("Student ID is required")
        self.registered_courses = list(registered_courses or [])

    def register_course(self, course):
        """Register the student for a course or course identifier."""
        course_id = course.course_id if isinstance(course, Course) else sanitize_input(course)
        if course_id and course_id not in self.registered_courses:
            self.registered_courses.append(course_id)

    def to_dict(self):
        """Return the student in a JSON-serializable dictionary."""
        return {"type": "Student", **self._person_dict(), "student_id": self.student_id,
                "registered_courses": self.registered_courses}

class Instructor(Person):
    """Person who can be assigned to courses."""

    def __init__(self, name, age, email, instructor_id, assigned_courses=None):
        """Create an instructor with an identifier and optional courses."""
        super().__init__(name, age, email)
        self.instructor_id = sanitize_input(instructor_id)
        if not self.instructor_id:
            raise ValueError("Instructor ID is required")
        self.assigned_courses = list(assigned_courses or [])

    def assign_course(self, course):
        """Assign the instructor to a course or course identifier."""
        course_id = course.course_id if isinstance(course, Course) else sanitize_input(course)
        if course_id and course_id not in self.assigned_courses:
            self.assigned_courses.append(course_id)

    def to_dict(self):
        """Return the instructor in a JSON-serializable dictionary."""
        return {"type": "Instructor", **self._person_dict(), "instructor_id": self.instructor_id,
                "assigned_courses": self.assigned_courses}

class Course:
    """Course model linking an instructor and enrolled students."""

    def __init__(self, course_id, course_name, instructor="", enrolled_students=None):
        """Create a course with an optional instructor and enrollment list."""
        self.course_id = sanitize_input(course_id)
        self.course_name = sanitize_input(course_name)
        if not self.course_id or not self.course_name:
            raise ValueError("Course ID and course name are required")
        self.instructor = instructor.instructor_id if isinstance(instructor, Instructor) else sanitize_input(instructor)
        self.enrolled_students = list(enrolled_students or [])

    def add_student(self, student):
        """Add a student or student identifier to the course."""
        student_id = student.student_id if isinstance(student, Student) else sanitize_input(student)
        if student_id and student_id not in self.enrolled_students:
            self.enrolled_students.append(student_id)
        if isinstance(student, Student):
            student.register_course(self)

    def to_dict(self):
        """Return the course in a JSON-serializable dictionary."""
        return {"type": "Course", "course_id": self.course_id, "course_name": self.course_name,
                "instructor": self.instructor, "enrolled_students": self.enrolled_students}

def _serialize(obj):
    """Convert a supported model object to a dictionary for JSON encoding."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def save_data(data, filename="data.json"):
    """Save model data as formatted JSON.

    Args:
        data: Model object or collection of model objects.
        filename (str): Destination JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, default=_serialize, indent=2)
    logging.info("Data saved to %s", filename)

def _deserialize(item):
    """Convert a serialized model dictionary back to a model object."""
    if not isinstance(item, dict) or "type" not in item:
        return item
    t = item["type"]
    if t == "Student":
        return Student(item["name"], item["age"], item["email"], item["student_id"], item.get("registered_courses", []))
    if t == "Instructor":
        return Instructor(item["name"], item["age"], item["email"], item["instructor_id"], item.get("assigned_courses", []))
    if t == "Course":
        return Course(item["course_id"], item["course_name"], item.get("instructor", ""), item.get("enrolled_students", []))
    return item

def load_data(filename="data.json"):
    """Load model data from JSON, returning an empty list if absent.

    Args:
        filename (str): JSON file to read.

    Returns:
        object: Reconstructed model data.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return []
    if isinstance(raw, list):
        return [_deserialize(x) for x in raw]
    if isinstance(raw, dict):
        return {k: [_deserialize(x) for x in v] if isinstance(v, list) else v for k, v in raw.items()}
    return raw
