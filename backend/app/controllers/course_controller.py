"""
Feature F05 - Course domain API controller set.
Design intent: gather course planning, enrollment, timetable, grading, and scheduling routes
under one controller so the course lifecycle is externally visible as a coherent API surface.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import SessionDependency, require_role
from app.api.schemas import (
    ClassroomListQuery,
    CourseClassDetailQuery,
    CourseClassListQuery,
    CourseDayTableQuery,
    CourseGradeQuery,
    CourseHistoryQuery,
    CoursePlanDetailQuery,
    CoursePlanSearchQuery,
    CourseSelectionRequest,
    CourseTableQuery,
    CourseTeacherGradeQuery,
    CourseTeacherGradeUpdateRequest,
    ScheduleListQuery,
    SchedulePlanRequest,
    TeacherScheduleQuery,
)
from app.core.settings import Settings
from app.core.time_windows import TimeWindowStore
from app.repositories.course_repository import CourseRepository
from app.services.course_service import CourseService


class CourseController:
    def __init__(self, settings: Settings, time_window_store: TimeWindowStore) -> None:
        self._settings = settings
        self._time_window_store = time_window_store
        self.router = APIRouter(prefix="/course")

        self.router.add_api_route("/plan/list", self.list_course_plans, methods=["GET"])
        self.router.add_api_route("/plan/detail", self.get_course_plan, methods=["GET"])
        self.router.add_api_route("/classer/list", self.list_course_classes, methods=["GET"])
        self.router.add_api_route("/classer/detail", self.get_course_class_detail, methods=["GET"])

        self.router.add_api_route("/select/enroll", self.enroll_course, methods=["POST"])
        self.router.add_api_route("/select/drop", self.drop_course, methods=["DELETE"])
        self.router.add_api_route("/select/history", self.list_selection_history, methods=["GET"])
        self.router.add_api_route("/select/list", self.list_selection_history, methods=["GET"])

        self.router.add_api_route("/table/student/table", self.student_table, methods=["GET"])
        self.router.add_api_route("/table/student/dayTable", self.student_day_table, methods=["GET"])
        self.router.add_api_route("/table/teacher/table", self.teacher_table, methods=["GET"])
        self.router.add_api_route("/table/teacher/dayTable", self.teacher_day_table, methods=["GET"])

        self.router.add_api_route("/grade/student", self.student_grade, methods=["GET"])
        self.router.add_api_route("/grade/teacher", self.teacher_grade, methods=["GET"])
        self.router.add_api_route("/grade/teacher", self.update_teacher_grade, methods=["PUT"])

        self.router.add_api_route("/schedule/classList", self.class_list, methods=["GET"])
        self.router.add_api_route("/schedule/classroomList", self.classroom_list, methods=["GET"])
        self.router.add_api_route("/schedule/scheduleList", self.schedule_list, methods=["GET"])
        self.router.add_api_route("/schedule/schedule", self.create_schedule, methods=["POST"])
        self.router.add_api_route("/schedule/teacherSchedule", self.teacher_schedule_detail, methods=["GET"])
        self.router.add_api_route("/schedule/teacherSchedule", self.delete_teacher_schedule, methods=["DELETE"])

    def _service(self, db: SessionDependency) -> CourseService:
        return CourseService(
            settings=self._settings,
            repository=CourseRepository(db),
            time_window_store=self._time_window_store,
        )

    def list_course_plans(
        self,
        db: SessionDependency,
        query: CoursePlanSearchQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).list_course_plans(payload.get("user_id"), query)

    def get_course_plan(
        self,
        db: SessionDependency,
        query: CoursePlanDetailQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).get_course_plan(query.id)

    def list_course_classes(
        self,
        db: SessionDependency,
        query: CourseClassListQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).list_course_classes(payload.get("user_id"), query)

    def get_course_class_detail(
        self,
        db: SessionDependency,
        query: CourseClassDetailQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).get_course_class_detail(query.id)

    def enroll_course(
        self,
        body: CourseSelectionRequest,
        db: SessionDependency,
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).enroll_course(payload.get("user_id"), body.classid)

    def drop_course(
        self,
        body: CourseSelectionRequest,
        db: SessionDependency,
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).drop_course(payload.get("user_id"), body.classid)

    def list_selection_history(
        self,
        db: SessionDependency,
        query: CourseHistoryQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).list_selection_history(payload.get("user_id"), query)

    def student_table(
        self,
        db: SessionDependency,
        query: CourseTableQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).list_student_month_schedule(payload.get("user_id"), query.time)

    def student_day_table(
        self,
        db: SessionDependency,
        query: CourseDayTableQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).list_student_day_schedule(payload.get("user_id"), query.time)

    def teacher_table(
        self,
        db: SessionDependency,
        query: CourseTableQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).list_teacher_month_schedule(payload.get("user_id"), query.time)

    def teacher_day_table(
        self,
        db: SessionDependency,
        query: CourseDayTableQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).list_teacher_day_schedule(payload.get("user_id"), query.time)

    def student_grade(
        self,
        db: SessionDependency,
        query: CourseGradeQuery = Depends(),
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).list_student_grades(payload.get("user_id"), query)

    def teacher_grade(
        self,
        db: SessionDependency,
        query: CourseTeacherGradeQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).list_teacher_grades(payload.get("user_id"), query.class_id)

    def update_teacher_grade(
        self,
        body: CourseTeacherGradeUpdateRequest,
        db: SessionDependency,
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).update_teacher_grades(
            payload.get("user_id"),
            body.class_id,
            body.student_id,
            body.grade,
        )

    def class_list(
        self,
        db: SessionDependency,
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).list_teacher_classes(payload.get("user_id"))

    def classroom_list(
        self,
        db: SessionDependency,
        query: ClassroomListQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).list_classrooms(query.class_num)

    def schedule_list(
        self,
        db: SessionDependency,
        query: ScheduleListQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).list_class_schedules(payload.get("user_id"), query.class_id)

    def create_schedule(
        self,
        body: SchedulePlanRequest,
        db: SessionDependency,
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).create_schedule(
            teacher_id=payload.get("user_id"),
            class_id=body.course_id,
            start_date=body.start_date,
            end_date=body.end_date,
            classroom_ids=body.classroom,
            prefer=body.prefer,
        )

    def teacher_schedule_detail(
        self,
        db: SessionDependency,
        query: TeacherScheduleQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).get_teacher_schedule_detail(
            payload.get("user_id"),
            query.teacher_schedule,
        )

    def delete_teacher_schedule(
        self,
        body: TeacherScheduleQuery,
        db: SessionDependency,
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).delete_teacher_schedule(
            payload.get("user_id"),
            body.teacher_schedule,
        )
