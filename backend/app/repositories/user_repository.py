"""
Feature F12 - User data access abstraction.
Design intent: separate persistence concerns from account lifecycle logic, making user lookup,
creation, and feedback storage traceable and reusable.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from model.AdminModel import Admin
from model.FeedbackModel import Feedback
from model.StudentModel import Student
from model.TeacherModel import Teacher


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_role_and_email(self, role: str, email: str):
        if role == "student":
            return self.session.query(Student).filter(Student.email == email).first()
        if role == "teacher":
            return self.session.query(Teacher).filter(Teacher.email == email).first()
        if role == "admin":
            return self.session.query(Admin).filter(Admin.name == email).first()
        return None

    def get_by_role_and_id(self, role: str, user_id: int):
        model = {"student": Student, "teacher": Teacher, "admin": Admin}.get(role)
        if model is None:
            return None
        return self.session.query(model).filter(model.id == user_id).first()

    def create_account(self, role: str, username: str, password_hash: str, email: str):
        if role == "student":
            user = Student(
                name=username,
                idcard=None,
                sex="U",
                password=password_hash,
                email=email,
            )
        elif role == "teacher":
            user = Teacher(
                name=username,
                password=password_hash,
                sex="U",
                email=email,
            )
        else:
            raise ValueError(f"Unsupported role: {role}")

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def save(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def create_feedback(self, title: str, content: str) -> Feedback:
        feedback = Feedback(
            title=title,
            content=content,
            created=int(datetime.now().timestamp()),
            is_read=0,
        )
        self.session.add(feedback)
        self.session.commit()
        self.session.refresh(feedback)
        return feedback
