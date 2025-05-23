from sqlalchemy.orm import Session
from sqlalchemy import func
from models.base import SessionLocal
from student_db.models.model import Student, Group, Teacher, Subject, Grade


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Top 5 students by average grade
def select_1():
    db: Session = next(get_db())
    result = (
        db.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id, Student.name)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return [(name, round(avg_grade, 2)) for name, avg_grade in result]


# 2. Student with highest average grade for a specific subject
def select_2(subject_name: str):
    db: Session = next(get_db())
    result = (
        db.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id, Student.name)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    return (result.name, round(result.avg_grade, 2)) if result else None


# 3. Average grade in groups for a specific subject
def select_3(subject_name: str):
    db: Session = next(get_db())
    result = (
        db.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Group.id, Group.name)
        .all()
    )
    return [(name, round(avg_grade, 2)) for name, avg_grade in result]


# 4. Average grade across all grades
def select_4():
    db: Session = next(get_db())
    result = db.query(func.avg(Grade.grade)).scalar()
    return round(result, 2) if result else None


# 5. Courses taught by a specific teacher
def select_5(teacher_name: str):
    db: Session = next(get_db())
    result = (
        db.query(Subject.name).join(Teacher).filter(Teacher.name == teacher_name).all()
    )
    return [name for (name,) in result]


# 6. Students in a specific group
def select_6(group_name: str):
    db: Session = next(get_db())
    result = db.query(Student.name).join(Group).filter(Group.name == group_name).all()
    return [name for (name,) in result]


# 7. Grades of students in a specific group for a specific subject
def select_7(group_name: str, subject_name: str):
    db: Session = next(get_db())
    result = (
        db.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return [(name, grade) for name, grade in result]


# 8. Average grade given by a specific teacher
def select_8(teacher_name: str):
    db: Session = next(get_db())
    result = (
        db.query(func.avg(Grade.grade))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round(result, 2) if result else None


# 9. Courses attended by a specific student
def select_9(student_name: str):
    db: Session = next(get_db())
    result = (
        db.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )
    return [name for (name,) in result]


# 10. Courses taught by a specific teacher to a specific student
def select_10(student_name: str, teacher_name: str):
    db: Session = next(get_db())
    result = (
        db.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )
    return [name for (name,) in result]


# Example usage
if __name__ == "__main__":
    print("1. Top 5 students by average grade:", select_1())
    print("2. Top student in Math:", select_2("Math"))
    print("3. Average grades by group for Math:", select_3("Math"))
    print("4. Overall average grade:", select_4())
    print(
        "5. Courses by teacher:", select_5("John Doe")
    )  # Replace with a teacher name from your DB
    print("6. Students in group:", select_6("Alpha Group"))  # Replace with a group name
    print("7. Grades in Alpha Group for Math:", select_7("Alpha Group", "Math"))
    print("8. Average grade by teacher:", select_8("John Doe"))
    print(
        "9. Courses for student:", select_9("Jane Smith")
    )  # Replace with a student name
    print("10. Courses for student by teacher:", select_10("Jane Smith", "John Doe"))
