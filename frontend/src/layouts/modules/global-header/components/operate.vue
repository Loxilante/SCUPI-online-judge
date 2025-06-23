<script setup lang="tsx">
/* eslint-disable */
import { computed, reactive, watch } from 'vue';
//@ts-ignore
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
//@ts-ignore
import { $t } from '@/locales';
//@ts-ignore
import { createUser, updateUser } from '@/service/api/course';

defineOptions({
  name: 'MenuOperateDrawer'
});

/**
 * the type of operation
 *
 * - add: add user
 * - edit: edit user
 */
export type OperateType = 'add' | 'edit';

interface Props {
  /** the type of operation */
  operateType: OperateType;
  /** the edit row data */
  rowData?: any;
}

const props = defineProps<Props>();

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: 'Add User',
    edit: 'Change Password'
  };
  return titles[props.operateType];
});
type Model = {
  "new_username": string;
  "new_user_password": string;
  "new_user_other_password": string;
};

const model: Model = reactive(createDefaultModel());

function createDefaultModel(): Model {
  return {
    "new_username": "",
    "new_user_password": "",
    "new_user_other_password": "",
  };
}

type RuleKey = Extract<keyof Model, 'userName' | 'userStatus'>;

const rules: Record<RuleKey, any> = {
  userName: defaultRequiredRule,
  userStatus: defaultRequiredRule
};

function handleUpdateModelWhenEdit() {
  if (props.operateType === 'add') {
    Object.assign(model, createDefaultModel());
    return;
  } else {
    Object.assign(model, createDefaultModel(), { new_username: props.rowData.username })
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  // request
  updateUser(model).then(() => {
    (window as any).$message?.success($t('Update Success!'));
    closeDrawer();
    emit('submitted');
  });
}

watch(visible, () => {
  if (visible.value) {
    handleUpdateModelWhenEdit();
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" :title="title" display-directive="show" :width="480">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules" label-placement="left" :label-width="120">
        <NFormItem label="Password" path="password">
          <NInput v-model:value="model.new_user_password" type="password" placeholder="Please Input password" />
        </NFormItem>
        <NFormItem label="New Password" path="password">
          <NInput v-model:value="model.new_user_other_password" type="password"
            placeholder="Please Input New Password" />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">Cancel</NButton>
          <NButton type="primary" @click="handleSubmit">{{ props.operateType == 'add' ? 'Create' : 'Update' }}</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
