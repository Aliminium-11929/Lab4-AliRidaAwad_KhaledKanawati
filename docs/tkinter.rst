Tkinter Interface
==================

The Tkinter application provides the same school-management workflow as the
PyQt5 application while using Python's built-in Tkinter toolkit. It includes
separate tabs for students, instructors, courses, enrollment management, and
combined search and record operations.

The interface supports:

* Create, edit, delete, and clear operations for students, instructors, and courses.
* Explicit student enrollment and unenrollment.
* Instructor assignment to courses.
* Search by name, ID, email, or course.
* JSON save and restore.
* CSV export.
* SQLite backup and restore.

The module uses a ``main()`` entry point, so importing it for documentation no
longer starts the Tkinter event loop. Sphinx can therefore document its helpers
and callbacks directly.

Tkinter API
-----------

.. automodule:: part2_tkinter
   :members:
   :undoc-members:
   :show-inheritance:
