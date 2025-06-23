import type { CustomAxiosRequestConfig } from '@sa/axios';
import { BACKEND_ERROR_CODE, createFlatRequest, createRequest } from '@sa/axios';
import { localStg } from '@/utils/storage';
import { createProxyPattern, createServiceConfig } from '~/env.config';
import { fetchRefreshToken } from '@/service/api/auth';
import { getRefreshToken, getUserInfo } from '@/store/modules/auth/shared';
import { useAuthStore } from '@/store/modules/auth/index';
import whiteList from './whiteList';
type NewRequestConfig = CustomAxiosRequestConfig<'json'> & {
  roles?: string;
};

const { baseURL, otherBaseURL } = createServiceConfig(import.meta.env);

const isHttpProxy = import.meta.env.VITE_HTTP_PROXY === 'Y';

const originRequest = createFlatRequest<App.Service.Response>(
  {
    baseURL: isHttpProxy ? createProxyPattern() : baseURL,
    withCredentials: true,
    headers: {
      apifoxToken: 'XL299LiMEDZ0H5h3A29PxwQXdMJqWyY2'
    }
  },
  {
    async onRequest(config: any) {
      const { headers } = config;
      // set token
      const token = localStg.get('token');
      const Authentication = token ? `${token}` : null;
      Object.assign(headers, {
        Authorization: Authentication && !whiteList.includes(config.url) ? `Bearer ${Authentication}` : ''
      });

      return config;
    },
    isBackendSuccess() {
      return true;
    },
    async onBackendFail(_response: any) {
      // if (_response.data.status === 302) {
      //   window.$message?.error(_response.data.msg);
      //   resetStore();
      // }
    },
    transformBackendResponse(response: any) {
      return response.data;
    }
  }
);

function handleResponse<T>(
  config: NewRequestConfig,
  res: any,
  resolve: (
    value:
      | {
          data: T | null;
          error: any;
        }
      | PromiseLike<{
          data: T | null;
          error: any;
        }>
  ) => void
) {
  if (res.error) {
    const response = res.error.response;
    const { refreshToken, resetStore } = useAuthStore();
    if (response?.data.code === 'token_not_valid') {
      fetchRefreshToken(getRefreshToken()).then(({ data, error }) => {
        if (error) {
          resetStore();
        } else {
          refreshToken(data);
          request(config).then(newRes => {
            handleResponse(config, newRes, resolve);
          });
        }
      });
      return;
    }
    if (response?.data.error) {
      window.$message?.error(response?.data.error);
      resolve(res);
      return;
    }
    if (response?.data.detail) {
      window.$message?.error(response?.data.detail);
      return;
    }
    if (response.status === 400) {
      window.$message?.error('This field may not be blank.');
    } else if (response.status === 404) {
      window.$message?.error('404 Not Found');
    } else {
      resolve(res);
    }
  } else {
    resolve(res);
  }
}
export const levelMap: any = {
  level1: 'administrator',
  level2: 'administrator,teacher',
  level3: 'administrator,teacher,student'
};
export function request<T>(config: NewRequestConfig) {
  return new Promise<{ data: T | null; error: any }>(resolve => {
    const userInfo = getUserInfo();
    if (config.roles) {
      if (!levelMap[config.roles].includes(userInfo.roles.join(','))) {
        return;
      }
    }

    originRequest<T>(config).then(res => {
      handleResponse<T>(config, res, resolve);
    });
  });
}

export const demoRequest = createRequest<App.Service.DemoResponse>(
  {
    baseURL: isHttpProxy ? createProxyPattern('demo') : otherBaseURL.demo
  },
  {
    async onRequest(config) {
      const { headers } = config;

      // set token
      const token = localStg.get('token');
      const Authorization = token ? `${token}` : null;
      Object.assign(headers, { Authorization });

      return config;
    },
    isBackendSuccess(response) {
      // when the backend response code is "200", it means the request is success
      // you can change this logic by yourself
      return response.data.status === '200';
    },
    async onBackendFail(_response) {
      // when the backend response code is not "200", it means the request is fail
      // for example: the token is expired, refetch token and retry request
    },
    transformBackendResponse(response) {
      return response.data.result;
    },
    onError(error) {
      // when the request is fail, you can show error message

      let message = error.message;

      // show backend error message
      if (error.code === BACKEND_ERROR_CODE) {
        message = error.response?.data?.message || message;
      }

      window.$message?.error(message);
    }
  }
);
