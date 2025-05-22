#!/usr/bin/pythonexport PATH=/Library/PostgreSQL/16/bin:$PATH
# type: ignore

from faker import Faker
from sqlalchemy.orm import Session
from models.base import SessionLocal, Base, engine
from models.models import Group, Student, Teacher, Subject, Grade
import random
from datetime import datetime, timedelta

fake = Faker()


def seed_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Create groups
        groups = [Group(name=fake.word().capitalize() + " Group") for _ in range(3)]
        db.add_all(groups)
        db.commit()

        # Create teachers
        teachers = [Teacher(name=fake.name()) for _ in range(5)]
        db.add_all(teachers)
        db.commit()

        # Create subjects
        subject_names = [
            "Math",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Literature",
            "Art",
            "Computer Science",
        ]
        subjects = [
            Subject(name=name, teacher_id=random.choice(teachers).id)
            for name in random.sample(subject_names, 6)
        ]
        db.add_all(subjects)
        db.commit()

        # Create students
        students = [
            Student(name=fake.name(), group_id=random.choice(groups).id)
            for _ in range(40)
        ]
        db.add_all(students)
        db.commit()

        # Create grades
        grades = []
        for student in students:
            for _ in range(random.randint(15, 20)):
                grades.append(
                    Grade(
                        student_id=student.id,
                        subject_id=random.choice(subjects).id,
                        grade=round(random.uniform(60, 100), 2),
                        date_received=fake.date_time_between(
                            start_date="-1y", end_date="now"
                        ),
                    )
                )
        db.add_all(grades)
        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
