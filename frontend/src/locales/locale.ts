import messages2 from '@/i18n/index';
import zhCN from './langs/zh-cn';
import enUS from './langs/en-us';

const locales: Record<App.I18n.LangType, App.I18n.Schema> = {
  'zh-CN': { ...zhCN, ...messages2.zh },
  'en-US': { ...enUS, ...messages2.en }
};

export default locales;
