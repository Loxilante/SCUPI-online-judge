import { createApp } from 'vue';
import './plugins/assets';
import { levelMap } from '@/service/request/index';
import { setupDayjs, setupIconifyOffline, setupLoading, setupNProgress } from './plugins';
import { setupStore } from './store';
import { setupRouter } from './router';
import { setupI18n } from './locales';
import App from './App.vue';
import { getUserInfo } from './store/modules/auth/shared';

async function setupApp() {
  setupLoading();

  setupNProgress();

  setupIconifyOffline();

  setupDayjs();

  const app = createApp(App);
  app.directive('p', (el, binding) => {
    const userInfo = getUserInfo();
    const rolesStr = userInfo.roles.join(',');
    if (binding.value && !levelMap[binding.value].includes(rolesStr)) {
      el.parentNode && el.parentNode.removeChild(el);
    }
  });

  setupStore(app);

  await setupRouter(app);

  setupI18n(app);

  app.mount('#app');
}

setupApp();
