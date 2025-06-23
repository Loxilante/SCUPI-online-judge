import type { App } from 'vue';
import { createI18n } from 'vue-i18n';
// import { localStg } from '@/utils/storage';
import messages from './locale';

const i18n = createI18n({
  locale: 'en-US',
  fallbackLocale: 'en',
  messages,
  legacy: false
});

/**
 * Setup plugin i18n
 *
 * @param app
 */
export function setupI18n(app: App) {
  app.use(i18n);
}

export const $t = (i18n as any).global.t as any;

export function setLocale(locale: App.I18n.LangType) {
  i18n.global.locale.value = locale;
}
