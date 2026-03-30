from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np

from app.core.exceptions import AppError, ForbiddenError, NotFoundError
from app.core.responses import success
from app.core.settings import Settings
from app.core.time_windows import TIME_FORMAT, TimeWindowStore
from app.repositories.course_repository import CourseRepository
from utils.opt_client.opt import run_opt_client


class CourseService:
    def __init__(
        self,
        settings: Settings,
        repository: CourseRepository,
        time_window_store: TimeWindowStore,
    ) -> None:
        self._settings = settings
        self._repository = repository
        self._time_window_store = time_window_store

    def list_course_plans(self, student_id: int, query) -> dict:
        data = self._repository.list_course_plans(
            student_id=student_id,
            page=query.page,
            page_size=query.pagesize,
            name=query.name,
            college=query.college,
            profession=query.profession,
            credit=query.credit,
            is_selected=query.is_selected,
            course_type=query.type,
        )
        return success(data)

    def get_course_plan(self, plan_id: int) -> dict:
        plan = self._repository.get_course_plan(plan_id)
        if plan is None:
            raise NotFoundError("ClassPlan Not Found")
        return success(
            {
                "id": plan.id,
                "name": plan.name,
                "introduction": plan.introduction,
                "profession": plan.profession,
                "college": plan.college,
                "credit": plan.credit,
                "type": plan.type,
            }
        )

    def get_course_class_detail(self, class_id: int) -> dict:
        data = self._repository.get_course_class_detail(class_id)
        if data is None:
            raise NotFoundError("Class Not Found")
        return success(data)

    def list_course_classes(self, student_id: int, query) -> dict:
        data = self._repository.list_course_classes(
            student_id=student_id,
            plan_id=query.id,
            page=query.page,
            page_size=query.pagesize,
        )
        return success(data)

    def enroll_course(self, student_id: int, class_id: int) -> dict:
        self._ensure_window_open("select", "不在选课时间")
        self._repository.enroll_course(student_id, class_id, datetime.now())
        return success()

    def drop_course(self, student_id: int, class_id: int) -> dict:
        self._ensure_window_open("select", "不在选课时间")
        self._repository.drop_course(student_id, class_id, datetime.now())
        return success()

    def list_selection_history(self, student_id: int, query) -> dict:
        data = self._repository.list_enrollment_history(
            student_id=student_id,
            page=query.page,
            page_size=query.pagesize,
            class_id=query.class_id,
            action_type=query.action_type,
        )
        return success(data)

    def list_student_month_schedule(self, student_id: int, time_str: str) -> dict:
        time_obj = self._parse_datetime(
            time_str,
            "%Y-%m",
            "Invalid time format, expected YYYY-MM",
        )
        data = self._repository.list_student_month_schedule(
            student_id=student_id,
            month=time_obj.month,
            year=time_obj.year,
        )
        return success(data)

    def list_student_day_schedule(self, student_id: int, time_str: str) -> dict:
        time_obj = self._parse_datetime(
            time_str,
            "%Y-%m-%d",
            "Invalid time format, expected YYYY-MM-DD",
        )
        return success(self._repository.list_student_day_schedule(student_id, time_obj))

    def list_teacher_month_schedule(self, teacher_id: int, time_str: str) -> dict:
        time_obj = self._parse_datetime(
            time_str,
            "%Y-%m",
            "Invalid time format, expected YYYY-MM",
        )
        data = self._repository.list_teacher_month_schedule(
            teacher_id=teacher_id,
            month=time_obj.month,
            year=time_obj.year,
        )
        return success(data)

    def list_teacher_day_schedule(self, teacher_id: int, time_str: str) -> dict:
        time_obj = self._parse_datetime(
            time_str,
            "%Y-%m-%d",
            "Invalid time format, expected YYYY-MM-DD",
        )
        return success(self._repository.list_teacher_day_schedule(teacher_id, time_obj))

    def list_student_grades(self, student_id: int, query) -> dict:
        return success(self._repository.list_student_grades(student_id, query.page, query.pagesize))

    def list_teacher_grades(self, teacher_id: int, class_id: int) -> dict:
        self._assert_teacher_owns_class(teacher_id, class_id)
        return success(self._repository.list_teacher_grades(class_id))

    def update_teacher_grades(
        self, teacher_id: int, class_id: int, student_ids: list[int], grades: list[int]
    ) -> dict:
        self._ensure_window_open("grade", "不在成绩录入时间")
        self._assert_teacher_owns_class(teacher_id, class_id)
        if len(student_ids) != len(grades):
            raise AppError("student len != grade len")
        if not student_ids:
            raise AppError("No student data provided")
        self._repository.update_teacher_grades(class_id, student_ids, grades)
        return success()

    def list_teacher_classes(self, teacher_id: int) -> dict:
        return success(self._repository.list_teacher_courses(teacher_id))

    def list_classrooms(self, minimum_capacity: int) -> dict:
        classrooms = self._repository.list_classrooms(minimum_capacity)
        data = [
            {
                "classroom_id": classroom.id,
                "name": classroom.name,
                "location": classroom.location,
                "capacity": classroom.capacity,
                "type": classroom.type,
            }
            for classroom in classrooms
        ]
        return success(data)

    def list_class_schedules(self, teacher_id: int, class_id: int) -> dict:
        self._assert_teacher_owns_class(teacher_id, class_id)
        return success(self._repository.list_class_schedules(class_id))

    def get_teacher_schedule_detail(self, teacher_id: int, teacher_schedule_id: int) -> dict:
        data = self._repository.get_teacher_schedule_detail(teacher_id, teacher_schedule_id)
        if data is None:
            raise NotFoundError("Teacher schedule not found")
        return success(data)

    def delete_teacher_schedule(self, teacher_id: int, teacher_schedule_id: int) -> dict:
        self._ensure_window_open("schedule", "不在排课时间")
        deleted = self._repository.delete_teacher_schedule(teacher_id, teacher_schedule_id)
        if not deleted:
            raise NotFoundError("Teacher schedule not found")
        return success()

    def create_schedule(
        self,
        teacher_id: int,
        class_id: int,
        start_date: str,
        end_date: str,
        classroom_ids: list[int],
        prefer: list[int],
    ) -> dict:
        self._ensure_window_open("schedule", "不在排课时间")
        self._assert_teacher_owns_class(teacher_id, class_id)

        if len(prefer) != 5:
            raise AppError("prefer must contain 5 time slots")
        if not classroom_ids:
            raise AppError("classroom list cannot be empty")

        start_dt = self._parse_datetime(
            start_date,
            TIME_FORMAT,
            "Invalid time format, expected YYYY-MM-DD HH:MM:SS",
        )
        end_dt = self._parse_datetime(
            end_date,
            TIME_FORMAT,
            "Invalid time format, expected YYYY-MM-DD HH:MM:SS",
        )
        if start_dt >= end_dt:
            raise AppError("时间范围无效")

        course = self._repository.get_class_by_id(class_id)
        if course is None:
            raise NotFoundError("Class Not Found")

        student_schedule_matrix, student_ids = self._repository.get_student_schedule_matrix(
            class_id, start_date, end_date
        )
        classroom_schedule_matrix = self._repository.get_classroom_schedule_matrix(
            classroom_ids, start_date, end_date
        )

        student_num, day_num, _ = student_schedule_matrix.shape
        classroom_num, _, _ = classroom_schedule_matrix.shape
        if day_num <= 0:
            raise AppError("时间范围至少需要覆盖一天")

        result = run_opt_client(
            self._settings.schedule_address,
            day_num,
            student_num,
            classroom_num,
            1,
            1,
            student_schedule_matrix.astype(int).flatten().tolist(),
            classroom_schedule_matrix.astype(int).flatten().tolist(),
            np.ones(day_num).tolist(),
            np.array(prefer).tolist(),
        )

        if not result.get("state"):
            raise AppError("教室冲突，排课失败", status_code=409)
        if result["w"] >= self._settings.schedule_conflict_threshold:
            raise AppError(
                f"学生冲突率{result['w'] * 100:.2f}%过高, 排课失败",
                status_code=409,
            )

        selected_slot = np.array(result["X"])
        slot_indices = np.where(selected_slot == 1)
        if len(slot_indices[0]) == 0:
            raise AppError("排课结果无有效时间", status_code=500)

        base_date = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        time_mapping = [
            timedelta(hours=8),
            timedelta(hours=10),
            timedelta(hours=14),
            timedelta(hours=16),
            timedelta(hours=19),
        ]
        scheduled_start_time = (
            base_date
            + timedelta(days=int(slot_indices[0][0]))
            + time_mapping[int(slot_indices[1][0])]
        )
        scheduled_end_time = scheduled_start_time + timedelta(hours=2)

        selected_classroom = np.array(result["Y"])
        classroom_indices = np.where(selected_classroom == 1)
        if len(classroom_indices[0]) == 0:
            raise AppError("排课结果无有效教室", status_code=500)
        classroom_id = classroom_ids[int(classroom_indices[0][0])]

        conflict_vector = np.sum(
            student_schedule_matrix * selected_slot.reshape(-1, 5), axis=(1, 2)
        )
        conflict_student_ids = [
            student_ids[index]
            for index, value in enumerate(conflict_vector.tolist())
            if value
        ]

        self._repository.create_schedule(
            teacher_id=teacher_id,
            class_id=class_id,
            classroom_id=classroom_id,
            start_time=scheduled_start_time,
            end_time=scheduled_end_time,
            conflict_rate=result["w"],
            preference_satisfaction=result["pref"],
            conflict_student_ids=conflict_student_ids,
        )

        return success(
            {
                "perf": result["pref"],
                "w": result["w"],
                "schedule": {
                    "start_time": scheduled_start_time,
                    "end_time": scheduled_end_time,
                    "classroom_id": classroom_id,
                },
                "conflict_students": conflict_student_ids,
            }
        )

    def _assert_teacher_owns_class(self, teacher_id: int, class_id: int) -> None:
        if not self._repository.teacher_owns_class(teacher_id, class_id):
            raise ForbiddenError("该课程不属于当前教师")

    def _ensure_window_open(self, window_name: str, message: str) -> None:
        window = self._time_window_store.get(window_name)
        if not window.contains(datetime.now()):
            raise AppError(message)

    @staticmethod
    def _parse_datetime(value: str, pattern: str, error_message: str) -> datetime:
        try:
            return datetime.strptime(value, pattern)
        except ValueError as exc:
            raise AppError(error_message) from exc
