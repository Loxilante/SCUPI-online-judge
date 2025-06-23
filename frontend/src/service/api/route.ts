import routes from '@/constants/routes';
import { request } from '../request';

/** get user routes */
export async function fetchGetUserRoutes() {
  return routes;
}

/**
 * whether the route is exist
 *
 * @param routeName route name
 */
export function fetchIsRouteExist(routeName: string) {
  return Promise.resolve(true); // request<boolean>({ url: '/route/isRouteExist', params: { routeName } });
}
