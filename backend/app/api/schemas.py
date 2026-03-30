from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


UserType = Literal["teacher", "student", "admin"]
RegisterUserType = Literal["teacher", "student"]
SexType = Literal["M", "F", "U"]
WindowType = Literal["select", "grade", "schedule"]


class UserAuthRequest(BaseModel):
    email: str
    password: str
    type: UserType


class UserRegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    type: RegisterUserType


class UserResendEmailRequest(BaseModel):
    email: str
    password: str
    type: RegisterUserType


class UserFeedbackRequest(BaseModel):
    title: str
    content: str


class StudentProfileUpdateRequest(BaseModel):
    username: str = ""
    password: str = ""
    sex: str = ""
    classer: str = ""
    profession: str = ""
    college: str = ""
    idcard: str = ""


class TeacherProfileUpdateRequest(BaseModel):
    username: str = ""
    password: str = ""
    sex: str = ""
    introduction: str = ""
    profession: str = ""
    college: str = ""
    idcard: str = ""


class TeacherLookupQuery(BaseModel):
    id: int


class AdminTimeRequest(BaseModel):
    start_time: str
    end_time: str


class CoursePlanSearchQuery(BaseModel):
    name: str = ""
    college: str = ""
    profession: str = ""
    credit: int = -1
    is_selected: int = -1
    type: str = ""
    page: int = 1
    pagesize: int = 10


class CoursePlanDetailQuery(BaseModel):
    id: int


class CourseClassDetailQuery(BaseModel):
    id: int


class CourseClassListQuery(BaseModel):
    id: int
    page: int = 1
    pagesize: int = 10


class CourseSelectionRequest(BaseModel):
    classid: int


class CourseHistoryQuery(BaseModel):
    page: int = 1
    pagesize: int = 10
    class_id: int = -1
    action_type: str = ""


class CourseTableQuery(BaseModel):
    time: str


class CourseDayTableQuery(BaseModel):
    time: str


class CourseGradeQuery(BaseModel):
    page: int = 1
    pagesize: int = 10


class CourseTeacherGradeQuery(BaseModel):
    class_id: int


class CourseTeacherGradeUpdateRequest(BaseModel):
    class_id: int
    student_id: list[int] = Field(default_factory=list)
    grade: list[int] = Field(default_factory=list)


class ClassroomListQuery(BaseModel):
    class_num: int


class SchedulePlanRequest(BaseModel):
    course_id: int
    start_date: str
    end_date: str
    classroom: list[int] = Field(default_factory=list)
    prefer: list[int] = Field(default_factory=list)


class ScheduleListQuery(BaseModel):
    class_id: int


class TeacherScheduleQuery(BaseModel):
    teacher_schedule: int
