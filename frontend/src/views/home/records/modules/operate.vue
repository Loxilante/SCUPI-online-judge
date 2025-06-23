<script setup lang="tsx">
/* eslint-disable */
import { computed, reactive, ref, watch } from 'vue';
//@ts-ignore
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
//@ts-ignore
import { $t } from '@/locales';
//@ts-ignore
import { createUser,updateUser } from '@/service/api/course';

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
const options = ref([{
  label:'全部',
  value:'',
},{
  label:'administrator',
  value:'administrator',
},{
  label:'teacher',
  value:'teacher',
},{
  label:'student',
  value:'student',
}]);

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: 'Add User',
    edit: 'Edit User'
  };
  return titles[props.operateType];
});
type Model = {
  "new_username": string;
  "new_user_password": string;
  "new_user_other_password": string;
  "new_user_email": string;
  "new_user_group": string;
  "new_user_first_name": string
};

const model: Model = reactive(createDefaultModel());

function createDefaultModel(): Model {
  return {
    "new_username": "",
    "new_user_password": "",
    "new_user_other_password": "",
    "new_user_email": "",
    "new_user_group": "",
    "new_user_first_name": ""
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
  }else{
    Object.assign(model,createDefaultModel(),{new_username:props.rowData.username})
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  if (props.operateType === 'add') {
    // request
    createUser(model).then(() => {
      (window as any).$message?.success($t('Add Success!'));
      closeDrawer();
      emit('submitted');
    });
  } else {
    // request
    updateUser(model).then(() => {
      (window as any).$message?.success($t('Update Success!'));
      closeDrawer();
      emit('submitted');
    });
  }
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
        <NFormItem v-if="operateType == 'add'" label="first name" path="first_name">
          <NInput v-model:value="model.new_user_first_name"
            placeholder="Please Input First Name" />
        </NFormItem>
        <NFormItem v-if="operateType == 'add'" label="username" path="username">
          <NInput v-model:value="model.new_username"
            placeholder="Please Input username" />
        </NFormItem>
        <NFormItem label="password" path="password">
          <NInput v-model:value="model.new_user_password" type="password"
            placeholder="Please Input password" />
        </NFormItem>
        <NFormItem v-if="operateType == 'edit'" label="NewPassword" path="password">
          <NInput v-model:value="model.new_user_other_password" type="password"
            placeholder="Please Input NewPassword" />
        </NFormItem>
        <NFormItem v-if="operateType == 'add'" label="User Email" path="email">
          <NInput v-model:value="model.new_user_email"
            placeholder="Please Input User Email" />
        </NFormItem>
        <NFormItem v-if="operateType == 'add'" label="User Group" path="group">
          <NSelect v-model:value="model.new_user_group" :options="options"
            placeholder="Please Input User Group" />
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
