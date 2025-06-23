<script setup lang="ts">
import { computed, reactive } from 'vue';
import { $t } from '@/locales';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { useAuthStore } from '@/store/modules/auth';
import { localStg } from '@/utils/storage';
defineOptions({
  name: 'PwdLogin'
});

const authStore = useAuthStore();
const { formRef, validate } = useNaiveForm();

interface FormModel {
  username: string;
  password: string;
  rememberMe: boolean;
}

const model: FormModel = reactive({
  username: localStg.get('rememberMe')?.username || '',
  password: localStg.get('rememberMe')?.password || '',
  rememberMe: true
});

const rules = computed<Record<keyof FormModel, App.Global.FormRule[]>>(() => {
  const { formRules } = useFormRules(); // inside computed to make locale reactive

  return {
    username: formRules.mobile,
    password: formRules.pwd,
    rememberMe: formRules.pwd
  };
});

async function handleSubmit() {
  await validate();
  if (model.rememberMe) {
    localStg.set('rememberMe', model as any);
  } else {
    localStg.remove('rememberMe');
  }
  await authStore.login(model.username, model.password);
}
</script>

<template>
  <NForm ref="formRef" :model="model" :rules="rules" size="large" :show-label="false">
    <NFormItem path="userName">
      <NInput v-model:value="model.username" :placeholder="$t('page.login.common.userNamePlaceholder')" />
    </NFormItem>
    <NFormItem path="newpassword">
      <NInput
        v-model:value="model.password"
        type="password"
        :placeholder="$t('page.login.common.passwordPlaceholder')"
      />
    </NFormItem>
    <NSpace vertical :size="24">
      <div class="flex-y-center justify-between">
        <NCheckbox v-model:checked="model.rememberMe">{{ $t('page.login.pwdLogin.rememberMe') }}</NCheckbox>
        <!--
 <NButton @click="()=>{
          $router.push({
            path:'/login/reset-pwd'
          })
        }" quaternary>{{ 'Change Password' }}</NButton>
-->
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
