import { request } from '../request';

/**
 * Login
 *
 * @param mobile User name
 * @param password Password
 */
export function fetchLogin(username: string, password: string) {
  return request<any>({
    url: '/login/',
    method: 'post',
    data: {
      username,
      password
    }
  });
}

/** Get user info */
export function fetchGetUserInfo(userName: string) {
  return request<any>({
    url: `/home/user/${userName}/`,
    method: 'get'
  });
}

/**
 * Refresh token
 *
 * @param refreshToken Refresh token
 */
export function fetchRefreshToken(refreshToken: string) {
  return request<any>({
    url: '/refresh/',
    method: 'post',
    data: {
      refresh: refreshToken
    }
  });
}

/**
 * @param data 修改密码
 * @returns
 */
export function changeUserPwd(data: { old_password: string; new_password: string; username: string }) {
  return request<any>({
    url: `/home/user/${data.username}/`,
    method: 'put',
    data: {
      old_password: data.old_password,
      new_password: data.new_password
    }
  });
}
