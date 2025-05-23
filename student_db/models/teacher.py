from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    subject = Column(String, nullable=False)

    # Many-to-many relationship with 'Student' via 'student_teacher' association table
    students = relationship(
        "Student", secondary="student_teacher", back_populates="teachers"
    )
