"""
Пояснення:
Імпорти: Імплементуйте ваші моделі в models.py.
Налаштування бази даних: Змініть DATABASE_URL, якщо потрібно.
Функції для створення даних:
create_groups: генерує групи.
create_teachers: генерує викладачів.
create_subjects: генерує предмети.
create_students: генерує студентів з оцінками.
Функція main: викликає всі функції для заповнення бази даних.
Запуск:
Запустіть скрипт, і ваша база даних буде заповнена випадковими даними.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subjects = relationship("Subject", back_populates="teacher")
    teacher = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    grade = Column(Float)
    date_received = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
