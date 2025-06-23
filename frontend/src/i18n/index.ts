const files = import.meta.glob('./locale/*.json');
const getModules = async () => {
  const modules: any = {};
  // eslint-disable-next-line guard-for-in
  for (const key in files) {
    // eslint-disable-next-line no-await-in-loop
    const res: any = await files[key]();
    const reg = /(.\/)(.*)(.json)$/;
    if (reg.test(key)) {
      const name = RegExp.$2;
      modules[name] = res.default;
    }
  }
  return modules;
};
const modules = await getModules();

const messages: any = {
  zh: {},
  en: {}
};
Object.values(modules).forEach((data: any) => {
  Object.keys(messages).forEach(key => {
    messages[key] = { ...messages[key], ...data[key] };
  });
});

// const languageMapping = {
//   'zh-CN': 'zh',
//   zh: 'zh',
//   en: 'en',
//   vi: 'vi'
// };

// const i18n = new VueI18n({
//   locale: sessionStorage.getItem('language') || languageMapping[navigator.language],
//   messages
// });
export default messages;
