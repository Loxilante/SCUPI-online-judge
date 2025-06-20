<script setup lang="ts">
/* eslint-disable */
import { computed, ref } from 'vue';
import { useSvgIconRender } from '@sa/hooks';
import { useAuthStore } from '@/store/modules/auth';
import { useRouterPush } from '@/hooks/common/router';
import { $t } from '@/locales';
//@ts-ignore
import Operate from './operate.vue'
//@ts-ignore
import SvgIcon from '@/components/custom/svg-icon.vue';
import { useTabStore } from '@/store/modules/tab';

defineOptions({
  name: 'UserAvatar'
});
const drawerVisible = ref(false)
const authStore = useAuthStore();
const { routerPushByKey, toLogin } = useRouterPush();
const { SvgIconVNode } = useSvgIconRender(SvgIcon);
const { clearTabs,clearCacheTabs } = useTabStore()
function loginOrRegister() {
  toLogin();
}

const options = computed(() => {
  const opts: any[] = [
    {
      label: 'settings',
      key: 'home_settings',
      icon: SvgIconVNode({ icon: 'ant-design:setting-outlined', fontSize: 18 })
    },
    {
      type: 'divider',
      key: 'divider'
    },
    {
      label: 'Logout',
      key: 'logout',
      icon: SvgIconVNode({ icon: 'ph:sign-out', fontSize: 18 })
    }
  ];

  return opts;
});

function logout() {
  window.$dialog?.info({
    title: $t('common.tip'),
    content: $t('common.logoutConfirm'),
    positiveText: $t('common.confirm'),
    negativeText: $t('common.cancel'),
    onPositiveClick: () => {
      authStore.resetStore();
      setTimeout(()=>{
        clearTabs();
        clearCacheTabs();
      },300)
    }
  });
}

function handleDropdown(key: any) {
  if (key === 'logout') {
    logout();
  } else {
    routerPushByKey(key);
  }
}
</script>

<template>
  <div>
    <NButton v-if="!authStore.isLogin" quaternary @click="loginOrRegister">
    {{ $t('page.login.common.loginOrRegister') }}
  </NButton>
  <NDropdown v-else placement="bottom" trigger="click" :options="options" @select="handleDropdown">
    <div>
      <ButtonIcon>
        <SvgIcon icon="ph:user-circle" class="text-icon-large" />
        <span class="text-16px font-medium">{{ authStore.userInfo.first_name }}</span>
      </ButtonIcon>
    </div>
  </NDropdown>
  <Operate operate-type="edit" :rowData="{username:authStore.userInfo.username}" v-model:visible="drawerVisible"></Operate>
  </div>
</template>

<style scoped></style>
