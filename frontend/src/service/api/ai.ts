import { request } from '../request';

/**
 * 获取当前登录用户的所有Token
 * @returns Token列表
 */
export function getTokens() {
  return request<any>({
    url: `/home/user/tokens/`,
    method: 'get'
  });
}

/**
 * 为当前登录用户添加一个新的Token
 * @param data 包含 platform, name, 和 token 的对象
 * @returns 新创建的Token对象
 */
export function addToken(data: any) {
  return request<any>({
    url: `/home/user/tokens/`,
    method: 'post',
    data: data
  });
}

/**
 * 更新一个指定的Token
 * @param data 包含要修改的Token的id，以及 password 和 new token
 * @returns 更新后的Token对象
 */
export function updateToken(data: any) {
  return request<any>({
    url: `/home/user/tokens/${data.id}/`,
    method: 'put',
    data: data
  });
}

/**
 * 删除一个指定的Token (建议补充的功能)
 * @param data 包含要删除的Token的id
 * @returns
 */
export function deleteToken(data: any) {
  return request<any>({
    url: `/home/user/tokens/${data.id}/`,
    method: 'delete',
    data: {
      password: data.password
    }
  });
}

/**
 * 获取一个题目的AI设置
 * @param data 包含 course_name, homework_name, 和 id
 * @returns
 */
export function getAISettings(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/ai/${data.id}/`,
    method: 'get'
  });
}

/**
 * 更新一个题目的AI设置
 * @param data 包含 URL 所需的 id 等信息，以及要更新的5个AI字段
 * @returns
 */
export function updateAISettings(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/ai/${data.id}/`,
    method: 'put',
    // 将整个data对象作为请求体发送。
    // 后端的序列化器会自动挑选它需要的字段进行更新。
    data: data
  });
}

/**
 * 清空一个题目的AI设置
 * @param data 包含 course_name, homework_name, 和 id
 * @returns
 */
export function deleteAISettings(data: any) {
  return request<any>({
    url: `/home/${data.course_name}/${data.homework_name}/ai/${data.id}/`,
    method: 'delete'
  });
}