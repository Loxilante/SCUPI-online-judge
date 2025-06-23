<script setup lang="ts">
/* eslint-disable */
import { computed } from 'vue';
import type { Component } from 'vue';
import { getColorPalette, mixColor } from '@sa/utils';
import { $t } from '@/locales';
import { useThemeStore } from '@/store/modules/theme';
import { loginModuleRecord } from '@/constants/app';
//@ts-ignore
import PwdLogin from './modules/pwd-login.vue';
//@ts-ignore
import ResetPwd from './modules/reset-pwd.vue';

interface Props {
  /** The login module */
  module?: UnionKey.LoginModule;
}

const props = withDefaults(defineProps<Props>(), {
  module: 'pwd-login'
});
const themeStore = useThemeStore();

interface LoginModule {
  key: UnionKey.LoginModule;
  label: string;
  component: Component;
}

const modules: LoginModule[] = [
  { key: 'pwd-login', label: loginModuleRecord['pwd-login'], component: PwdLogin },
  { key: 'reset-pwd', label: loginModuleRecord['reset-pwd'], component: ResetPwd }
];

const activeModule = computed(() => {
  const findItem = modules.find(item => item.key === props.module);
  return findItem || modules[0];
});

const bgThemeColor = computed(() =>
  themeStore.darkMode ? getColorPalette(themeStore.themeColor, 7) : themeStore.themeColor
);

const bgColor = computed(() => {
  const COLOR_WHITE = '#ffffff';

  const ratio = themeStore.darkMode ? 0.5 : 0.2;

  return mixColor(COLOR_WHITE, themeStore.themeColor, ratio);
});
</script>

<template>
  <div class="relative flex-center wh-full overflow-hidden" :style="{ backgroundColor: bgColor }">
    <WaveBg :theme-color="bgThemeColor" />
    <NCard :bordered="false" class="relative w-auto rd-12px z-4">
      <div class="w-400px <sm:w-300px">
        <header class="flex-y-center justify-between">
          <!-- <SystemLogo class="text-64px text-primary <sm:text-48px" /> -->
          <h3 class="text-28px font-500 text-primary <sm:text-22px">
            {{ props.module == 'reset-pwd' ? 'Change Your Password' : 'Login To Your Account' }}
          </h3>
          <div class="i-flex-vertical">
            <!-- <ThemeSchemaSwitch
              :theme-schema="themeStore.themeScheme"
              :show-tooltip="false"
              class="text-20px <sm:text-18px"
              @switch="themeStore.toggleThemeScheme"
            /> -->
            <!--
 <LangSwitch
              :lang="appStore.locale"
              :lang-options="appStore.localeOptions"
              :show-tooltip="false"
              @change-lang="appStore.changeLocale"
            />
-->
          </div>
        </header>
        <main class="pt-24px">
          <h3 class="text-18px text-primary font-medium">{{ $t(activeModule.label) }}</h3>
          <div class="pt-24px">
            <Transition :name="themeStore.page.animateMode" mode="out-in" appear>
              <component :is="activeModule.component" />
            </Transition>
          </div>
        </main>
      </div>
    </NCard>
  </div>
</template>

<style scoped></style>
