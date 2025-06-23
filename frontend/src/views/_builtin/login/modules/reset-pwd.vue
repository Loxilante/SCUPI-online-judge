<script setup lang="ts">
import { computed, reactive } from 'vue';
import { $t } from '@/locales';
import { useRouterPush } from '@/hooks/common/router';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { useAuthStore } from '@/store/modules/auth';
import { changeUserPwd } from '@/service/api/auth';

defineOptions({
  name: 'PwdLogin'
});

const authStore = useAuthStore();
const { toLogin } = useRouterPush(false);
const { formRef, validate } = useNaiveForm();

interface FormModel {
  username: string;
  new_password: string;
  password: string;
}

const model: FormModel = reactive({
  username: '',
  new_password: '',
  password: ''
});

const rules = computed<Record<keyof FormModel, App.Global.FormRule[]>>(() => {
  const { formRules } = useFormRules(); // inside computed to make locale reactive

  return {
    username: formRules.mobile,
    new_password: formRules.pwd,
    password: formRules.pwd
  };
});

async function handleSubmit() {
  await validate();
  changeUserPwd({
    username: model.username,
    new_password: model.new_password,
    old_password: model.password
  }).then(() => {
    toLogin(undefined, '/home/editor');
  });
}
</script>

<template>
  <NForm ref="formRef" :model="model" :rules="rules" size="large" :show-label="false">
    <NFormItem path="userName">
      <NInput v-model:value="model.username" :placeholder="$t('page.login.common.userNamePlaceholder')" />
    </NFormItem>
    <NFormItem path="password">
      <NInput
        v-model:value="model.password"
        type="password"
        :placeholder="$t('page.login.common.passwordPlaceholder')"
      />
    </NFormItem>
    <NFormItem path="new_password">
      <NInput v-model:value="model.new_password" type="password" placeholder="Please Confirm Password" />
    </NFormItem>
    <NSpace vertical :size="24">
      <div class="flex-y-center justify-between">
        <!-- <NCheckbox>{{ $t('page.login.pwdLogin.rememberMe') }}</NCheckbox> -->
        <span></span>
        <NButton
          quaternary
          @click="
            () => {
              toLogin(undefined, '/home/editor');
            }
          "
        >
          Login
        </NButton>
      </div>
      <NButton type="primary" size="large" block round :loading="authStore.loginLoading" @click="handleSubmit">
        Sign In
      </NButton>
      <div
        class="flex-y-center justify-between gap-12px"
        style="display: flex; align-items: center; justify-content: center"
      >
        <span>
            SCUPI算法评分
            <a href="https://beian.miit.gov.cn/" style="color: #6941c6; margin-left: 6px">蜀ICP备2023034748号-3</a>
        </span>
      </div>
    </NSpace>
  </NForm>
</template>

<style scoped></style>
