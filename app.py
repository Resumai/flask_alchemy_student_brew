from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
# for code highlighting:
from sqlalchemy import Column, Integer, String, select

# flask_sqlalchemy uses shortcuts to most of sqlalchemy,
# so, most things are safe to import from sqlalchemy.
# Things to avoid are infrastructure related, like:
# Session, engine, declartive base, metadata, etc.


app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']: str = 'sqlite:///students.db'
db: SQLAlchemy = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(100), nullable=False)
    age: int = Column(Integer, nullable=False)
    grade: str = Column(String(10), nullable=False)

    def __repr__(self) -> str:
        return f"<Student name={self.name} age={self.age} grade={self.grade}>"

# Create the database and tables
with app.app_context():
    db.create_all()

# Helper functions for CRUD operations

# Add a student
def add_student(name: str, age: int, grade: str) -> None:
    student: Student = Student(name=name, age=age, grade=grade)
    db.session.add(student)
    db.session.commit()

# Get a student by ID or a message indicating that the student doesn't exist.
def get_student_by_id(id: int) -> Optional[Student]:
    student = db.session.get(Student, id)
    if not student:
        # print(f"Student with ID {id} not found.")
        return f"Student with ID {id} not found."
    return student

# Get all students
def get_all_students() -> List[Student]:
    selection = select(Student)
    return db.session.execute(selection).scalars().all()

# Update a student
def update_student(id: int, name: str, age: int, grade: str) -> None:
    selection = select(Student).where(Student.id == id)
    student = db.session.execute(selection).scalar_one_or_none()
    if student:
        student.name = name
        student.age = age
        student.grade = grade
        db.session.commit()

# Delete a student
def delete_student(id: int) -> None:
    selection = select(Student).where(Student.id == id)
    student = db.session.execute(selection).scalar_one_or_none()
    if student:
        db.session.delete(student)
        db.session.commit()

if __name__ == '__main__':
    # Sample usage of the functions:
    with app.app_context():

        # Add students
        add_student("Jhonny Jhon", 20, "A")
        add_student("Jane Junior", 22, "B")
        
        # Get students by ID
        student = get_student_by_id(1)
        print("Student by ID:", student)

        # Get all students
        students = get_all_students()
        print("Before delete:", students)

        # Update student
        update_student(1, "Jhonny Jhon", 21, "A")

        # Delete student
        delete_student(2)


        # Get all students, after update and delete
        students2 = get_all_students()
        print("After update and delete:", students2)