/**
 * Create service config by current env
 *
 * @param env The current env
 */
export function createServiceConfig(env: Env.ImportMeta) {
  const mockURL = 'https://ojapi.loxilante.uno';

  const serviceConfigMap: App.Service.ServiceConfigMap = {
    dev: {
      baseURL: mockURL,
      otherBaseURL: {
        demo: mockURL
      }
    },
    test: {
      baseURL: mockURL,
      otherBaseURL: {
        demo: mockURL
      }
    },
    prod: {
      baseURL: mockURL,
      otherBaseURL: {
        demo: mockURL
      }
    }
  };

  const { VITE_SERVICE_ENV = 'dev' } = env;

  return serviceConfigMap[VITE_SERVICE_ENV];
}

/**
 * Get proxy pattern of service url
 *
 * @param key If not set, will use the default key
 */
export function createProxyPattern(key?: App.Service.OtherBaseURLKey) {
  if (!key) {
    return '/pro-api/pro-api';
  }

  return `/proxy-${key}`;
}
