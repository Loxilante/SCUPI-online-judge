/* eslint-disable */
import { request } from '../request';
export function getCourseList() {
  return request<any>({
    url: '/home/',
    method: 'get'
  });
}

/**
 * 根据班级获取作业
 *
 * @param data
 * @returns
 */
export function getHomeworkByCourse(data: { coursename: any }) {
  return request<any>({
    url: `/home/${data.coursename}/`,
    method: 'get'
  });
}

/**
 * 为某班级添加作业
 *
 * @param data
 * @returns
 */
export function addHomeworkToCourse(
  coursename: string,
  data: {
    name: string;
    description: string;
    due_date: any;
  }
) {
  return request<any>({
    url: `/home/${coursename}/`,
    method: 'post',
    data
  });
}

/**
 * 修改作业
 *
 * @param coursename
 * @param data
 * @returns
 */
export function updateHomeworkToCourse(
  coursename: string,
  data: {
    name: string;
    description: string;
    due_date: any;
  }
) {
  return request<any>({
    url: `/home/${coursename}/`,
    method: 'put',
    data
  });
}

/**
 * 删除作业
 *
 * @param coursename
 * @param data
 * @returns
 */
export function removeHomeworkToCourse(coursename: string, name: string) {
  return request<any>({
    url: `/home/${coursename}/`,
    method: 'DELETE',
    data: {
      name
    }
  });
}

/**
 * 添加班级
 *
 * @param data
 * @returns
 */
export function addCourse(data: { course_name: string; students_list: string[] }) {
  return request<any>({
    url: '/home/',
    method: 'post',
    data
  });
}

/**
 * 修改班级
 *
 * @param course_name
 * @returns
 */
export function updateCourse(
  course_name: string,
  data: {
    course_name: string;
    students_list: string[];
  }
) {
  return request<any>({
    url: `/home/${course_name}/member/`,
    method: 'put',
    data: {
      course_name: data.course_name,
      students_list: data.students_list
    }
  });
}

export function removeCourse(course_name: string) {
  return request<any>({
    url: `/home/`,
    method: 'delete',
    data: {
      course_name
    }
  });
}

export function getStudentList() {
  return request<any>({
    url: '/home/user/',
    method: 'get',
    roles:'level2'
  });
}

export function getStudentListByCourseName(course_name: string) {
  return request<any>({
    url: `/home/${course_name}/member/`,
    method: 'get'
  });
}

/**
 * 根据作业得到题目列表
 *
 * @param course_name
 * @param home_work
 * @returns
 */
export function getProblemByHomework(data: { course_name: any; home_work: any }) {
  return request<any>({
    url: `/home/${data.course_name}/${data.home_work}/`,
    method: 'get'
  });
}

export function addProblemByHomework(data: { course_name: any; home_work: any }, item: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.home_work}/`,
    method: 'post',
    data: item
  });
}

export function updateProblemByHomework(data: { course_name: any; home_work: any }, item: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.home_work}/`,
    method: 'put',
    data: item
  });
}

export function removeQuestion(course_name: any, home_work: any, id: any) {
  return request<any>({
    url: `/home/${course_name}/${home_work}`,
    method: 'delete',
    data: {
      delete_id: [id]
    }
  });
}

export function uploadImage(data: { course_name: any; home_work: any; id: any; image: any }) {
  const formData = new FormData();
  formData.append('image', data.image);
  formData.append('problem', data.id);
  formData.append('name', data.image.name);
  return request<any>({
    url: `/home/${data.course_name}/${data.home_work}/image/${data.id}/`,
    method: 'post',
    data: formData
  });
}

export function removeImage(data: { course_name: any; home_work: any; id: any; image_id: any }) {
  return request<any>({
    url: `/home/${data.course_name}/${data.home_work}/image/${data.id}/`,
    method: 'delete',
    data: {
      image_id: [data.image_id]
    }
  });
}

export function viewImage(course_name: any, home_work: any, id: any) {
  return request<any>({
    url: `/home/${course_name}/${home_work}/image/${id}/`,
    method: 'get'
  });
}

export function getProblemDetail(data: { course_name: any; home_work: any; id: any }) {
  return request<any>({
    url: `/home/${data.course_name}/${data.home_work}/`,
    method: 'get',
    params: {
      problem_id: data.id
    }
  });
}
/**
 * 运行代码接口
 *
 * @param data
 * @returns
 */
export function runcode(data: any) {
  return request<any>({
    url: `/runcode/`,
    method: 'post',
    data
  });
}

/**
 * 代码提交接口
 *
 * @param data
 * @returns
 */
export function codeSubmit(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/submit/`,
    method: 'post',
    data: {
      id: data.id,
      content_answer: data.content_answer
    }
  });
}

export function createCodeCase(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/programming/${data.id}/`,
    method: data.isUpdate ? 'put' : 'post',
    data: data.params
  });
}

export function queryCodeCase(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/programming/${data.id}/`,
    method: 'get'
  });
}

export function removeCodeCase(data: any, delete_id: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/programming/${data.id}/`,
    method: 'delete',
    data: { delete_id: [delete_id] }
  });
}

export function viewSubmissionRecord(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/${data.id}/${data.username}/`,
    method: 'get'
  });
}

export function getAllUsers(data: any) {
  return request<any>({
    url: `/home/user/`,
    method: 'get',
    roles:'level2'
  });
}

export function getCourseUsers(courseName: any) {
  return request<any>({
    url: `/home/${courseName}/member/`,
    method: 'get',
    roles:'level2'
  });
}


export function createUser(data: any) {
  return request<any>({
    url: `/home/user/`,
    method: 'post',
    data
  });
}

export function queryUser(username: string) {
  return request<any>({
    url: `/home/user/${username}/`,
    method: 'get'
  });
}

export function updateUser(data: any) {
  return request<any>({
    url: `/home/user/${data.new_username}/`,
    method: 'put',
    data:{
      old_password:data.new_user_password,
      new_password:data.new_user_other_password
    }
  });
}

export function removeUser(username:string) {
  return request<any>({
    url: `/home/user/`,
    method: 'delete',
    data:{
      delete_username:username
    }
  });
}

export function getQuestionRecords(data:any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/${data.id}/all/`,
    method: 'get'
  });
}

export function getHomeworkRecords(data:any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/getstuscore/all/`,
    method: 'get'
  });
}

export function getHomeworkByStudenetIdRecords(data:any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/getscore/${data.username}/`,
    method: 'get'
  });
}


export function commentForQuestion(data:any,params:any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/${data.id}/`,
    method: 'put',
    data:params
  });
}


export function removeCommentForQuestion(data:any,params:any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/${data.id}/`,
    method: 'delete',
    data:params
  });
}
