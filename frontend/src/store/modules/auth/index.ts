import { computed, reactive, ref } from 'vue';
import { defineStore } from 'pinia';
import { useLoading } from '@sa/hooks';
import { SetupStoreId } from '@/enum';
import { useRouterPush } from '@/hooks/common/router';
import { fetchGetUserInfo, fetchLogin } from '@/service/api';
import { localStg } from '@/utils/storage';
import { $t } from '@/locales';
import { useRouteStore } from '../route';
import { clearAuthStorage, getToken, getUserInfo } from './shared';

export const useAuthStore = defineStore(SetupStoreId.Auth, () => {
  const routeStore = useRouteStore();
  const { route, toLogin, redirectFromLogin } = useRouterPush(false);
  const { loading: loginLoading, startLoading, endLoading } = useLoading();
  const token = ref(getToken());

  const userInfo: any = reactive(getUserInfo());

  /** Is login */
  const isLogin = computed(() => Boolean(token.value));

  /** Reset auth store */
  async function resetStore() {
    const authStore = useAuthStore();

    clearAuthStorage();

    authStore.$reset();

    if (!route.value.meta.constant) {
      await toLogin();
    }

    routeStore.resetStore();
  }

  /**
   * Login
   *
   * @param userName User name
   * @param password Password
   */
  async function login(userName: string, password: string) {
    startLoading();

    const { data: loginToken, error } = await fetchLogin(userName, password);
    if (!error) {
      const pass = await loginByToken(loginToken, userName);

      if (pass) {
        await routeStore.initAuthRoute();

        await redirectFromLogin();

        if (routeStore.isInitAuthRoute) {
          window.$notification?.success({
            title: $t('page.login.common.loginSuccess'),
            content: $t('page.login.common.welcomeBack', { userName: userInfo.first_name }),
            duration: 4500
          });
        }
      }
    } else {
      resetStore();
    }

    endLoading();
  }

  async function loginByToken(loginToken: any, userName: string) {
    // 1. stored in the localStorage, the later requests need it in headers
    localStg.set('token', loginToken.access);
    localStg.set('refreshToken', loginToken.refresh);

    const { data, error } = await fetchGetUserInfo(userName);

    if (!error) {
      // 2. store user info
      localStg.set('userInfo', {
        ...data,
        roles: [loginToken.role]
      });

      // 3. update auth route
      token.value = loginToken.access;
      Object.assign(userInfo, {
        ...data,
        roles: [loginToken.role]
      });

      return true;
    }

    return false;
  }

  async function refreshToken(loginToken: any) {
    localStg.set('token', loginToken.access);
    token.value = loginToken.access;
  }

  return {
    token,
    userInfo,
    isLogin,
    loginLoading,
    resetStore,
    refreshToken,
    login
  };
});
