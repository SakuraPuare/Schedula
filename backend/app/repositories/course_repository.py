from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from crud.ClassCrud import ClassCrud
from crud.ClassPlanCrud import ClassPlanCrud
from crud.EnrollCrud import EnrollCrud
from crud.EnrollmentHistoryCrud import EnrollmentHistoryCrud
from crud.SCCrud import StudentCourseCrud
from crud.ScheduleCrud import ScheduleCrud
from model.ClassModel import Class
from model.ClassPlanModel import ClassPlan
from model.ClassScheduleModel import ClassSchedule
from model.ClassroomModel import Classroom
from model.SCModel import StudentCourse
from model.StudentModel import Student
from model.TeacherScheduleModel import TeacherSchedule


class CourseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_course_plans(
        self,
        student_id: int,
        page: int,
        page_size: int,
        name: str,
        college: str,
        profession: str,
        credit: int,
        is_selected: int,
        course_type: str,
    ) -> dict:
        return ClassPlanCrud.get_by_filters(
            self.session,
            student_id=student_id,
            page=page,
            page_size=page_size,
            name=name,
            college=college,
            profession=profession,
            credit=credit,
            is_selected=is_selected,
            type=course_type,
        )

    def get_course_plan(self, plan_id: int) -> Optional[ClassPlan]:
        return self.session.query(ClassPlan).filter(ClassPlan.id == plan_id).first()

    def get_course_class_detail(self, class_id: int) -> Optional[dict]:
        return ClassCrud.get_by_id(self.session, class_id)

    def list_course_classes(
        self, student_id: int, plan_id: int, page: int, page_size: int
    ) -> dict:
        return ClassCrud.get_by_id_paginated(
            self.session,
            user_id=student_id,
            id=plan_id,
            page=page,
            page_size=page_size,
        )

    def enroll_course(self, student_id: int, class_id: int, action_time: datetime) -> None:
        EnrollCrud.enroll_course(self.session, student_id=student_id, class_id=class_id, time=action_time)

    def drop_course(self, student_id: int, class_id: int, action_time: datetime) -> None:
        EnrollCrud.drop_course(self.session, student_id=student_id, class_id=class_id, time=action_time)

    def list_enrollment_history(
        self,
        student_id: int,
        page: int,
        page_size: int,
        class_id: int,
        action_type: str,
    ) -> dict:
        return EnrollmentHistoryCrud.get_by_filters(
            self.session,
            page=page,
            page_size=page_size,
            student_id=student_id,
            class_id=class_id,
            action_type=action_type,
        )

    def list_student_month_schedule(self, student_id: int, month: int, year: int) -> list[dict]:
        records = (
            self.session.query(
                ClassPlan.name.label("course_name"),
                ClassSchedule.start_time,
            )
            .join(Class, ClassPlan.id == Class.class_plan_id)
            .join(ClassSchedule, Class.id == ClassSchedule.class_id)
            .join(StudentCourse, StudentCourse.class_id == Class.id)
            .filter(
                StudentCourse.student_id == student_id,
                extract("month", ClassSchedule.start_time) == month,
                extract("year", ClassSchedule.start_time) == year,
            )
            .all()
        )
        return [{"name": name, "date": start_time} for name, start_time in records]

    def list_student_day_schedule(self, student_id: int, specific_date: datetime) -> list[dict]:
        records = (
            self.session.query(
                ClassPlan.name.label("course_name"),
                ClassSchedule,
            )
            .select_from(StudentCourse)
            .join(Class, StudentCourse.class_id == Class.id)
            .join(ClassPlan, ClassPlan.id == Class.class_plan_id)
            .join(ClassSchedule, ClassSchedule.class_id == Class.id)
            .filter(
                StudentCourse.student_id == student_id,
                func.date(ClassSchedule.start_time) == specific_date.date(),
            )
            .all()
        )
        return [
            {
                "name": name,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "classroom": self.serialize_classroom(schedule.classroom),
            }
            for name, schedule in records
        ]

    def list_teacher_month_schedule(self, teacher_id: int, month: int, year: int) -> list[dict]:
        records = (
            self.session.query(
                ClassPlan.name.label("course_name"),
                ClassSchedule.start_time,
            )
            .join(Class, ClassPlan.id == Class.class_plan_id)
            .join(ClassSchedule, Class.id == ClassSchedule.class_id)
            .filter(
                Class.teacher_id == teacher_id,
                extract("month", ClassSchedule.start_time) == month,
                extract("year", ClassSchedule.start_time) == year,
            )
            .all()
        )
        return [{"name": name, "date": start_time} for name, start_time in records]

    def list_teacher_day_schedule(self, teacher_id: int, specific_date: datetime) -> list[dict]:
        records = (
            self.session.query(
                ClassPlan.name.label("course_name"),
                ClassSchedule,
            )
            .join(Class, ClassPlan.id == Class.class_plan_id)
            .join(ClassSchedule, Class.id == ClassSchedule.class_id)
            .filter(
                Class.teacher_id == teacher_id,
                func.date(ClassSchedule.start_time) == specific_date.date(),
            )
            .all()
        )
        return [
            {
                "name": name,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "classroom": self.serialize_classroom(schedule.classroom),
            }
            for name, schedule in records
        ]

    def list_student_grades(self, student_id: int, page: int, page_size: int) -> dict:
        return StudentCourseCrud.get_student_grade_page(
            self.session,
            student_id=student_id,
            page=page,
            page_size=page_size,
        )

    def teacher_owns_class(self, teacher_id: int, class_id: int) -> bool:
        return (
            self.session.query(Class)
            .filter(Class.id == class_id, Class.teacher_id == teacher_id)
            .first()
            is not None
        )

    def list_teacher_grades(self, class_id: int) -> list[dict]:
        results = (
            self.session.query(Student.id, Student.name, StudentCourse.grade)
            .join(StudentCourse, Student.id == StudentCourse.student_id)
            .filter(StudentCourse.class_id == class_id)
            .order_by(Student.id.asc())
            .all()
        )
        return [{"id": row[0], "name": row[1], "grade": row[2]} for row in results]

    def update_teacher_grades(
        self, class_id: int, student_ids: list[int], grades: list[int]
    ) -> None:
        records = (
            self.session.query(StudentCourse)
            .filter(
                StudentCourse.class_id == class_id,
                StudentCourse.student_id.in_(student_ids),
            )
            .all()
        )
        records_by_student = {record.student_id: record for record in records}
        missing_student_ids = [
            student_id for student_id in student_ids if student_id not in records_by_student
        ]
        if missing_student_ids:
            raise AppError("存在未选该课的学生，无法录入成绩")

        for student_id, grade in zip(student_ids, grades):
            records_by_student[student_id].grade = grade

        self.session.commit()

    def list_teacher_courses(self, teacher_id: int) -> list[dict]:
        results = (
            self.session.query(ClassPlan, Class)
            .join(Class, Class.class_plan_id == ClassPlan.id)
            .filter(Class.teacher_id == teacher_id)
            .all()
        )
        return [
            {
                "class_id": classer.id,
                "name": plan.name,
                "num": classer.num,
                "type": plan.type,
                "credit": plan.credit,
            }
            for plan, classer in results
        ]

    def list_classrooms(self, minimum_capacity: int) -> list[Classroom]:
        return (
            self.session.query(Classroom)
            .filter(Classroom.capacity >= minimum_capacity)
            .order_by(Classroom.type.asc(), Classroom.capacity.asc(), Classroom.id.asc())
            .all()
        )

    def list_class_schedules(self, class_id: int) -> list[dict]:
        schedule_rows = (
            self.session.query(ClassSchedule)
            .filter(ClassSchedule.class_id == class_id)
            .order_by(ClassSchedule.start_time.asc())
            .all()
        )
        result = []
        for schedule in schedule_rows:
            teacher_schedule = (
                self.session.query(TeacherSchedule)
                .filter(TeacherSchedule.class_schedule_id == schedule.id)
                .first()
            )
            result.append(
                {
                    "id": teacher_schedule.id if teacher_schedule else -1,
                    "start_time": schedule.start_time,
                    "end_time": schedule.end_time,
                    "classroom": schedule.classroom.name,
                    "is_teacher": teacher_schedule is not None,
                }
            )
        return result

    def get_teacher_schedule(self, teacher_id: int, teacher_schedule_id: int) -> Optional[TeacherSchedule]:
        return (
            self.session.query(TeacherSchedule)
            .filter(
                TeacherSchedule.id == teacher_schedule_id,
                TeacherSchedule.teacher_id == teacher_id,
            )
            .first()
        )

    def get_teacher_schedule_detail(self, teacher_id: int, teacher_schedule_id: int) -> Optional[dict]:
        teacher_schedule = self.get_teacher_schedule(teacher_id, teacher_schedule_id)
        if teacher_schedule is None:
            return None

        conflict_ids = json.loads(teacher_schedule.conflict_student_ids or "[]")
        conflict_names = []
        if conflict_ids:
            students = (
                self.session.query(Student)
                .filter(Student.id.in_(conflict_ids))
                .order_by(Student.id.asc())
                .all()
            )
            conflict_names = [student.name for student in students]

        return {
            "start_time": teacher_schedule.class_schedule.start_time,
            "end_time": teacher_schedule.class_schedule.end_time,
            "conflict_rate": teacher_schedule.conflict_rate,
            "prefer_rate": teacher_schedule.preference_satisfaction,
            "conflict_student": conflict_names,
        }

    def delete_teacher_schedule(self, teacher_id: int, teacher_schedule_id: int) -> bool:
        teacher_schedule = self.get_teacher_schedule(teacher_id, teacher_schedule_id)
        if teacher_schedule is None:
            return False

        class_schedule = teacher_schedule.class_schedule
        self.session.delete(teacher_schedule)
        if class_schedule is not None:
            self.session.delete(class_schedule)
        self.session.commit()
        return True

    def get_class_by_id(self, class_id: int) -> Optional[Class]:
        return self.session.query(Class).filter(Class.id == class_id).first()

    def get_student_schedule_matrix(self, class_id: int, start_date: str, end_date: str):
        return ScheduleCrud.get_student_schedule_matrix(
            self.session,
            course_id=class_id,
            start_date=start_date,
            end_date=end_date,
        )

    def get_classroom_schedule_matrix(self, classroom_ids: list[int], start_date: str, end_date: str):
        return ScheduleCrud.get_classroom_schedule_matrix(
            self.session,
            classroom_ids=classroom_ids,
            start_date=start_date,
            end_date=end_date,
        )

    def create_schedule(
        self,
        teacher_id: int,
        class_id: int,
        classroom_id: int,
        start_time: datetime,
        end_time: datetime,
        conflict_rate: float,
        preference_satisfaction: float,
        conflict_student_ids: list[int],
    ) -> dict:
        class_schedule = ClassSchedule(
            start_time=start_time,
            end_time=end_time,
            classroom_id=classroom_id,
            class_id=class_id,
        )
        self.session.add(class_schedule)
        self.session.flush()

        teacher_schedule = TeacherSchedule(
            teacher_id=teacher_id,
            class_schedule_id=class_schedule.id,
            conflict_rate=conflict_rate,
            preference_satisfaction=preference_satisfaction,
            conflict_student_ids=json.dumps(conflict_student_ids),
        )
        self.session.add(teacher_schedule)
        self.session.commit()
        self.session.refresh(class_schedule)
        self.session.refresh(teacher_schedule)

        return {
            "teacher_schedule_id": teacher_schedule.id,
            "class_schedule_id": class_schedule.id,
        }

    @staticmethod
    def serialize_classroom(classroom: Optional[Classroom]) -> Optional[dict]:
        if classroom is None:
            return None
        return {
            "id": classroom.id,
            "name": classroom.name,
            "location": classroom.location,
            "capacity": classroom.capacity,
            "type": classroom.type,
        }
