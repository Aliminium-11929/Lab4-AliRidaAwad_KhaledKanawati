"""PyQt5 interface for managing the school database."""

import csv, sys
from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,QTabWidget,QLineEdit,QPushButton,QComboBox,QTableWidget,QTableWidgetItem,QMessageBox,QFileDialog,QLabel)
from part1_oop import Student, Instructor, Course, save_data, load_data
import part4_database as db

db.setup_db().close()

class App(QWidget):
    """Main window containing CRUD, search, export, and backup controls."""

    def __init__(self):
        """Build the window, tabs, controls, and initial database view."""
        super().__init__(); self.setWindowTitle("School Management System - PyQt5"); self.resize(1050,650)
        self.s_old=self.i_old=self.c_old=None
        self.tabs=QTabWidget(); self.build_students(); self.build_instructors(); self.build_courses(); self.build_enrollment(); self.build_records()
        lay=QVBoxLayout(self); lay.addWidget(self.tabs); self.refresh()
    def warn(self,e):
        """Show a database or validation error in a warning dialog."""
        QMessageBox.warning(self,"Error",str(e))
    def mk_table(self, headers):
        """Create a read-only table with row selection enabled."""
        t=QTableWidget(0,len(headers)); t.setHorizontalHeaderLabels(headers); t.setSelectionBehavior(QTableWidget.SelectRows); t.setEditTriggers(QTableWidget.NoEditTriggers); return t
    def fields(self, labels):
        """Create a form layout and its labeled line-edit controls."""
        f=QFormLayout(); d={}
        for x in labels: d[x]=QLineEdit(); f.addRow(x,d[x])
        return f,d
    def buttons(self, specs):
        """Create a horizontal row of connected push buttons."""
        l=QHBoxLayout()
        for name,fn in specs: b=QPushButton(name); b.clicked.connect(fn); l.addWidget(b)
        return l
    def build_students(self):
        """Build the student management tab."""
        w=QWidget(); l=QVBoxLayout(w); f,self.s=self.fields(["Student ID","Name","Age","Email"]); self.s_course=QComboBox(); f.addRow("Course",self.s_course); l.addLayout(f); l.addLayout(self.buttons([("Add",self.add_student),("Edit",self.edit_student),("Delete",self.del_student),("Clear",self.clear_student)])); self.st=self.mk_table(["ID","Name","Age","Email","Registered Courses"]); self.st.cellClicked.connect(self.pick_student); l.addWidget(self.st); self.tabs.addTab(w,"Students")
    def build_instructors(self):
        """Build the instructor management tab."""
        w=QWidget(); l=QVBoxLayout(w); f,self.i=self.fields(["Instructor ID","Name","Age","Email"]); l.addLayout(f); l.addLayout(self.buttons([("Add",self.add_instructor),("Edit",self.edit_instructor),("Delete",self.del_instructor),("Clear",self.clear_instructor)])); self.it=self.mk_table(["ID","Name","Age","Email","Assigned Courses"]); self.it.cellClicked.connect(self.pick_instructor); l.addWidget(self.it); self.tabs.addTab(w,"Instructors")
    def build_courses(self):
        """Build the course management tab."""
        w=QWidget(); l=QVBoxLayout(w); f,self.c=self.fields(["Course ID","Course Name"]); self.c_inst=QComboBox(); f.addRow("Instructor",self.c_inst); l.addLayout(f); l.addLayout(self.buttons([("Add",self.add_course),("Edit",self.edit_course),("Delete",self.del_course),("Clear",self.clear_course)])); self.ct=self.mk_table(["Course ID","Course Name","Instructor ID"]); self.ct.cellClicked.connect(self.pick_course); l.addWidget(self.ct); self.tabs.addTab(w,"Courses")
    def build_enrollment(self):
        """Build the enrollment management tab."""
        w=QWidget(); l=QVBoxLayout(w); f=QFormLayout()
        self.enroll_student_combo=QComboBox(); self.enroll_course_combo=QComboBox()
        f.addRow("Student",self.enroll_student_combo); f.addRow("Course",self.enroll_course_combo); l.addLayout(f)
        l.addLayout(self.buttons([("Enroll",self.enroll_student), ("Unenroll Selected",self.unenroll_student)]))
        self.et=self.mk_table(["Student ID","Student Name","Course ID","Course Name"]); l.addWidget(self.et); self.tabs.addTab(w,"Enrollment")
    def build_records(self):
        """Build the combined search and file operations tab."""
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(QLabel("Search by name, ID, email, or course:")); self.search=QLineEdit(); self.search.textChanged.connect(self.refresh_records); l.addWidget(self.search); self.rt=self.mk_table(["Type","ID","Name / Course","Email / Instructor"]); l.addWidget(self.rt); l.addLayout(self.buttons([("Save JSON",self.save_json),("Load JSON",self.load_json),("Export CSV",self.export_csv),("Backup DB",self.backup),("Restore DB",self.restore)])); self.tabs.addTab(w,"All Records / Search")
    def set_table(self,t,rows):
        """Replace a table's contents with the supplied rows."""
        t.setRowCount(len(rows))
        for r,row in enumerate(rows):
            for c,val in enumerate(row): t.setItem(r,c,QTableWidgetItem(str(val)))
        t.resizeColumnsToContents()
    def refresh(self):
        """Reload database records and refresh all tabs."""
        courses=db.get_courses(); instructors=db.get_instructors(); students=db.get_students()
        self.s_course.clear(); self.s_course.addItem(""); self.s_course.addItems([x[0] for x in courses]); self.c_inst.clear(); self.c_inst.addItem(""); self.c_inst.addItems([x[0] for x in instructors])
        self.set_table(self.st,[(sid,n,a,e,", ".join(db.get_student_courses(sid))) for sid,n,a,e in students]); self.set_table(self.it,[(iid,n,a,e,", ".join(c[0] for c in courses if c[2]==iid)) for iid,n,a,e in instructors]); self.set_table(self.ct,courses)
        self.enroll_student_combo.clear(); self.enroll_course_combo.clear()
        for sid,n,_,_ in students: self.enroll_student_combo.addItem(f"{sid} - {n}",sid)
        for cid,n,_ in courses: self.enroll_course_combo.addItem(f"{cid} - {n}",cid)
        student_names={sid:n for sid,n,_,_ in students}; course_names={cid:n for cid,n,_ in courses}
        self.set_table(self.et,[(sid,student_names.get(sid,""),cid,course_names.get(cid,"")) for sid,cid in db.get_enrollments()])
        self.refresh_records()
    def enroll_student(self):
        """Enroll the selected student in the selected course."""
        try:
            student_id=self.enroll_student_combo.currentData(); course_id=self.enroll_course_combo.currentData()
            if not student_id or not course_id: raise ValueError("Select both a student and a course")
            changed=db.enroll_student_db(student_id,course_id); self.refresh()
            QMessageBox.information(self,"Enrollment","Student enrolled successfully" if changed else "Student is already enrolled in that course")
        except Exception as e:self.warn(e)
    def unenroll_student(self):
        """Remove the selected student-course enrollment."""
        try:
            row=self.et.currentRow()
            if row < 0: raise ValueError("Select an enrollment first")
            student_id=self.et.item(row,0).text(); course_id=self.et.item(row,2).text()
            answer=QMessageBox.question(self,"Confirm Unenroll",f"Unenroll {student_id} from {course_id}?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if answer != QMessageBox.Yes: return
            db.unenroll_student_db(student_id,course_id); self.refresh(); QMessageBox.information(self,"Enrollment","Student unenrolled successfully")
        except Exception as e:self.warn(e)
    def refresh_records(self):
        """Refresh the combined records table using the search field."""
        term=self.search.text() if hasattr(self,"search") else ""; rows=db.search_records(term) if term else ([("Student",r[0],r[1],r[3]) for r in db.get_students()]+[("Instructor",r[0],r[1],r[3]) for r in db.get_instructors()]+[("Course",r[0],r[1],r[2]) for r in db.get_courses()]); self.set_table(self.rt,rows)
    def add_student(self):
        """Validate and add a student, optionally enrolling them."""
        try:
            s=Student(self.s["Name"].text(),self.s["Age"].text(),self.s["Email"].text(),self.s["Student ID"].text()); db.add_student_db(s.student_id,s.name,s.age,s.email)
            if self.s_course.currentText(): db.enroll_student_db(s.student_id,self.s_course.currentText())
            self.clear_student(); self.refresh()
        except Exception as e:self.warn(e)
    def edit_student(self):
        """Validate and update the selected student."""
        try:
            if not self.s_old: raise ValueError("Select a student first")
            s=Student(self.s["Name"].text(),self.s["Age"].text(),self.s["Email"].text(),self.s["Student ID"].text()); db.update_student_db(self.s_old,s.student_id,s.name,s.age,s.email)
            if self.s_course.currentText(): db.enroll_student_db(s.student_id,self.s_course.currentText())
            self.clear_student(); self.refresh()
        except Exception as e:self.warn(e)
    def del_student(self):
        """Delete the selected student."""
        try:
            if not self.s_old: raise ValueError("Select a student first")
            db.delete_student_db(self.s_old); self.clear_student(); self.refresh()
        except Exception as e:self.warn(e)
    def pick_student(self,row,_):
        """Copy a selected student row into the form controls."""
        vals=[self.st.item(row,c).text() for c in range(5)]; self.s_old=vals[0]
        for k,v in zip(["Student ID","Name","Age","Email"],vals[:4]): self.s[k].setText(v)
        self.s_course.setCurrentText(vals[4].split(", ")[0] if vals[4] else "")
    def clear_student(self):
        """Clear student controls and selection state."""
        self.s_old=None; [x.clear() for x in self.s.values()]; self.s_course.setCurrentIndex(0)
    def add_instructor(self):
        """Validate and add an instructor."""
        try:
            i=Instructor(self.i["Name"].text(),self.i["Age"].text(),self.i["Email"].text(),self.i["Instructor ID"].text()); db.add_instructor_db(i.instructor_id,i.name,i.age,i.email); self.clear_instructor(); self.refresh()
        except Exception as e:self.warn(e)
    def edit_instructor(self):
        """Validate and update the selected instructor."""
        try:
            if not self.i_old: raise ValueError("Select an instructor first")
            i=Instructor(self.i["Name"].text(),self.i["Age"].text(),self.i["Email"].text(),self.i["Instructor ID"].text()); db.update_instructor_db(self.i_old,i.instructor_id,i.name,i.age,i.email); self.clear_instructor(); self.refresh()
        except Exception as e:self.warn(e)
    def del_instructor(self):
        """Delete the selected instructor."""
        try:
            if not self.i_old: raise ValueError("Select an instructor first")
            db.delete_instructor_db(self.i_old); self.clear_instructor(); self.refresh()
        except Exception as e:self.warn(e)
    def pick_instructor(self,row,_):
        """Copy a selected instructor row into the form controls."""
        vals=[self.it.item(row,c).text() for c in range(4)]; self.i_old=vals[0]
        for k,v in zip(["Instructor ID","Name","Age","Email"],vals): self.i[k].setText(v)
    def clear_instructor(self):
        """Clear instructor controls and selection state."""
        self.i_old=None; [x.clear() for x in self.i.values()]
    def add_course(self):
        """Validate and add a course."""
        try:
            c=Course(self.c["Course ID"].text(),self.c["Course Name"].text(),self.c_inst.currentText()); db.add_course_db(c.course_id,c.course_name,c.instructor); self.clear_course(); self.refresh()
        except Exception as e:self.warn(e)
    def edit_course(self):
        """Validate and update the selected course."""
        try:
            if not self.c_old: raise ValueError("Select a course first")
            c=Course(self.c["Course ID"].text(),self.c["Course Name"].text(),self.c_inst.currentText()); db.update_course_db(self.c_old,c.course_id,c.course_name,c.instructor); self.clear_course(); self.refresh()
        except Exception as e:self.warn(e)
    def del_course(self):
        """Delete the selected course."""
        try:
            if not self.c_old: raise ValueError("Select a course first")
            db.delete_course_db(self.c_old); self.clear_course(); self.refresh()
        except Exception as e:self.warn(e)
    def pick_course(self,row,_):
        """Copy a selected course row into the form controls."""
        vals=[self.ct.item(row,c).text() for c in range(3)]; self.c_old=vals[0]; self.c["Course ID"].setText(vals[0]); self.c["Course Name"].setText(vals[1]); self.c_inst.setCurrentText(vals[2])
    def clear_course(self):
        """Clear course controls and selection state."""
        self.c_old=None; [x.clear() for x in self.c.values()]; self.c_inst.setCurrentIndex(0)
    def data_objects(self):
        """Build model objects from the current database records."""
        return {"students":[Student(n,a,e,sid,db.get_student_courses(sid)) for sid,n,a,e in db.get_students()],"instructors":[Instructor(n,a,e,iid,[c[0] for c in db.get_courses() if c[2]==iid]) for iid,n,a,e in db.get_instructors()],"courses":[Course(cid,n,iid,[sid for sid,c in db.get_enrollments() if c==cid]) for cid,n,iid in db.get_courses()]}
    def save_json(self):
        """Save the current records to a user-selected JSON file."""
        p,_=QFileDialog.getSaveFileName(self,"Save data","data.json","JSON (*.json)");
        if p: save_data(self.data_objects(),p); QMessageBox.information(self,"Saved",p)
    def load_json(self):
        """Restore records from a user-selected JSON file."""
        p,_=QFileDialog.getOpenFileName(self,"Load data","","JSON (*.json)");
        if not p:return
        try:
            data=load_data(p)
            with db.connect_db() as con: con.execute("DELETE FROM enrollments"); con.execute("DELETE FROM courses"); con.execute("DELETE FROM instructors"); con.execute("DELETE FROM students")
            for s in data.get("students",[]): db.add_student_db(s.student_id,s.name,s.age,s.email)
            for i in data.get("instructors",[]): db.add_instructor_db(i.instructor_id,i.name,i.age,i.email)
            for c in data.get("courses",[]): db.add_course_db(c.course_id,c.course_name,c.instructor)
            for s in data.get("students",[]):
                for cid in s.registered_courses: db.enroll_student_db(s.student_id,cid)
            self.refresh()
        except Exception as e:self.warn(e)
    def export_csv(self):
        """Export students, instructors, and courses to CSV."""
        p,_=QFileDialog.getSaveFileName(self,"Export CSV","school_records.csv","CSV (*.csv)");
        if not p:return
        with open(p,"w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["Type","ID","Name","Age","Email","Course/Instructor"])
            for sid,n,a,e in db.get_students(): w.writerow(["Student",sid,n,a,e,", ".join(db.get_student_courses(sid))])
            for iid,n,a,e in db.get_instructors(): w.writerow(["Instructor",iid,n,a,e,", ".join(c[0] for c in db.get_courses() if c[2]==iid)])
            for cid,n,iid in db.get_courses(): w.writerow(["Course",cid,n,"","",iid])
        QMessageBox.information(self,"Export","CSV exported successfully")
    def backup(self):
        """Create a database backup and report its path."""
        try: QMessageBox.information(self,"Backup",f"Saved to {db.backup_db()}")
        except Exception as e:self.warn(e)
    def restore(self):
        """Restore the database backup and refresh the interface."""
        try: db.restore_db(); self.refresh(); QMessageBox.information(self,"Restore","Database restored successfully")
        except Exception as e:self.warn(e)

if __name__=="__main__":
    app=QApplication(sys.argv); win=App(); win.show(); sys.exit(app.exec_())
