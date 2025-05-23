from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

# Association table for 'student_teacher' many-to-many relationship
student_teacher = Table(
    "student_teacher",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    grade = Column(Integer, nullable=False)

    # Many-to-many relationship with 'Teacher' via 'student_teacher' association table
    teachers = relationship(
        "Teacher", secondary="student_teacher", back_populates="students"
    )
