import { localStg } from '@/utils/storage';

/** Get token */
export function getToken() {
  return localStg.get('token') || '';
}

export function getRefreshToken() {
  return localStg.get('refreshToken') || '';
}

/** Get user info */
export function getUserInfo() {
  const emptyInfo: any = {
    first_name: '',
    roles: [],
    email: '',
    username: ''
  };
  const userInfo = localStg.get('userInfo') || emptyInfo;
  return userInfo;
}

/** Clear auth storage */
export function clearAuthStorage() {
  localStg.remove('token');
  localStg.remove('refreshToken');
  localStg.remove('userInfo');
}
