import { request } from '../request';

/**
 * 获取当前登录用户的所有APIKey
 * @returns APIKey列表
 */
export function getAPIKeys() {
  return request<any>({
    url: `/home/user/apikeys/`,
    method: 'get'
  });
}

/**
 * 为当前登录用户添加一个新的APIKey
 * @param data 包含 platform, name, 和 api_key 的对象
 * @returns 新创建的APIKey对象
 */
export function addAPIKey(data: any) {
  return request<any>({
    url: `/home/user/apikeys/`,
    method: 'post',
    data: data
  });
}

/**
 * 更新一个指定的APIKey
 * @param data 包含要修改的APIKey的id，以及 password 和 new api_key
 * @returns 更新后的APIKey对象
 */
export function updateAPIKey(data: any) {
  return request<any>({
    url: `/home/user/apikeys/${data.id}/`,
    method: 'put',
    data: data
  });
}
 
/**
 * 删除一个指定的APIKey (建议补充的功能)
 * @param data 包含要删除的APIKey的id
 * @returns
 */
export function deleteAPIKey(data: any) {
  return request<any>({
    url: `/home/user/apikeys/${data.id}/`,
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