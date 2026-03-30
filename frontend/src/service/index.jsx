import axios from "axios";

const normalizeBaseURL = (value) => (value.endsWith("/") ? value : `${value}/`);

const resolveBaseURL = () => {
  const configuredBaseURL = window.baseURL;
  if (configuredBaseURL) {
    return normalizeBaseURL(configuredBaseURL);
  }

  const protocol = window.location.protocol || "http:";
  const hostname = window.location.hostname || "127.0.0.1";
  return normalizeBaseURL(`${protocol}//${hostname}:8000`);
};

class HttpClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  request({ method, url, data, params }) {
    const token = localStorage.getItem("token");
    const headers = token ? { Authorization: `Bearer ${token}` } : undefined;

    return axios({
      baseURL: this.baseURL,
      method,
      url,
      data,
      params,
      headers,
    });
  }

  get(url, params) {
    return this.request({ method: "get", url, params });
  }

  post(url, data) {
    return this.request({ method: "post", url, data });
  }

  put(url, data) {
    return this.request({ method: "put", url, data });
  }

  delete(url, data) {
    return this.request({ method: "delete", url, data });
  }
}

class UserApi {
  constructor(client) {
    this.client = client;
  }

  auth(email, password, type) {
    return this.client.post("/user/auth", { email, password, type });
  }

  check() {
    return this.client.post("/user/check");
  }

  register(email, username, password, type) {
    return this.client.post("/user/register", {
      username,
      email,
      password,
      type,
    });
  }

  resendEmail(email, password, type) {
    return this.client.post("/user/resendEmail", { email, password, type });
  }

  feedback(title, content) {
    return this.client.post("/user/feedback", { title, content });
  }
}

class TeacherApi {
  constructor(client) {
    this.client = client;
  }

  updateInfo(username, password, sex, introduction, profession, college, idcard) {
    return this.client.put("/teacher/updateInfo", {
      username,
      password,
      sex,
      introduction,
      profession,
      college,
      idcard,
    });
  }

  getInfo() {
    return this.client.get("/teacher/getInfo");
  }

  listInfo(id) {
    return this.client.get("/teacher/listInfo", { id });
  }
}

class StudentApi {
  constructor(client) {
    this.client = client;
  }

  getInfo() {
    return this.client.get("/student/getInfo");
  }

  updateInfo(username, password, sex, classer, profession, college, idcard) {
    return this.client.put("/student/updateInfo", {
      username,
      password,
      sex,
      classer,
      profession,
      college,
      idcard,
    });
  }
}

class CoursePlanApi {
  constructor(client) {
    this.client = client;
  }

  detail(id) {
    return this.client.get("/course/plan/detail", { id });
  }

  list(page, pagesize, name, college, profession, credit, is_selected, type) {
    return this.client.get("/course/plan/list", {
      name,
      college,
      profession,
      credit,
      is_selected,
      type,
      page,
      pagesize,
    });
  }
}

class CourseClassApi {
  constructor(client) {
    this.client = client;
  }

  detail(id) {
    return this.client.get("/course/classer/detail", { id });
  }

  list(id, page, pagesize) {
    return this.client.get("/course/classer/list", { id, page, pagesize });
  }
}

class CourseApi {
  constructor(client) {
    this.client = client;
  }

  enroll(classid) {
    return this.client.post("/course/select/enroll", { classid });
  }

  drop(classid) {
    return this.client.delete("/course/select/drop", { classid });
  }

  list(page, pagesize, class_id, action_type) {
    return this.client.get("/course/select/list", {
      page,
      pagesize,
      class_id,
      action_type,
    });
  }

  history(page, pagesize, class_id, action_type) {
    return this.client.get("/course/select/history", {
      page,
      pagesize,
      class_id,
      action_type,
    });
  }

  studentTable(time) {
    return this.client.get("/course/table/student/table", { time });
  }

  studentDayTable(time) {
    return this.client.get("/course/table/student/dayTable", { time });
  }

  teacherTable(time) {
    return this.client.get("/course/table/teacher/table", { time });
  }

  teacherDayTable(time) {
    return this.client.get("/course/table/teacher/dayTable", { time });
  }

  studentGrade(page, pagesize) {
    return this.client.get("/course/grade/student", { page, pagesize });
  }

  classList() {
    return this.client.get("/course/schedule/classList");
  }

  scheduleList(class_id) {
    return this.client.get("/course/schedule/scheduleList", { class_id });
  }

  classroomList(class_num) {
    return this.client.get("/course/schedule/classroomList", { class_num });
  }

  schedule(course_id, start_date, end_date, classroom, prefer) {
    return this.client.post("/course/schedule/schedule", {
      course_id,
      start_date,
      end_date,
      classroom,
      prefer,
    });
  }

  teacherScheduleDelete(teacher_schedule) {
    return this.client.delete("/course/schedule/teacherSchedule", {
      teacher_schedule,
    });
  }

  teacherScheduleList(teacher_schedule) {
    return this.client.get("/course/schedule/teacherSchedule", {
      teacher_schedule,
    });
  }

  gradeTeacher(class_id) {
    return this.client.get("/course/grade/teacher", { class_id });
  }

  updateTeacher(class_id, student_id, grade) {
    return this.client.put("/course/grade/teacher", {
      class_id,
      student_id,
      grade,
    });
  }
}

class AdminApi {
  constructor(client) {
    this.client = client;
  }

  gradeTimeGet() {
    return this.client.get("/admin/time/grade");
  }

  gradeTimePut(start_time, end_time) {
    return this.client.put("/admin/time/grade", { start_time, end_time });
  }

  scheduleTimeGet() {
    return this.client.get("/admin/time/schedule");
  }

  scheduleTimePut(start_time, end_time) {
    return this.client.put("/admin/time/schedule", { start_time, end_time });
  }

  selectTimeGet() {
    return this.client.get("/admin/time/select");
  }

  selectTimePut(start_time, end_time) {
    return this.client.put("/admin/time/select", { start_time, end_time });
  }
}

class ApiService {
  constructor(client) {
    this.client = client;
    this.user = new UserApi(client);
    this.teacher = new TeacherApi(client);
    this.student = new StudentApi(client);
    this.courseplan = new CoursePlanApi(client);
    this.courseclasser = new CourseClassApi(client);
    this.course = new CourseApi(client);
    this.admin = new AdminApi(client);
  }

  root() {
    return this.client.get("/");
  }
}

const client = new HttpClient(resolveBaseURL());

export const service = new ApiService(client);
