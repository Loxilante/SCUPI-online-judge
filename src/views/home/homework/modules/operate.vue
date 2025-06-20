<script setup lang="tsx">
import { computed, reactive, watch } from 'vue';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { addHomeworkToCourse, updateHomeworkToCourse } from '@/service/api/course';

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
  course_name?: any;
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
    add: 'Add Homework',
    edit: 'Edit Homework'
  };
  return titles[props.operateType];
});
type Model = {
  name: string;
  description: string;
  due_date: any;
};

const model: Model = reactive(createDefaultModel());

function createDefaultModel(): Model {
  return {
    name: '',
    description: '',
    due_date: null,
  };
}

type RuleKey = Extract<keyof Model, 'userName' | 'userStatus'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  userName: defaultRequiredRule,
  userStatus: defaultRequiredRule
};

function handleUpdateModelWhenEdit() {
  if (props.operateType === 'add') {
    Object.assign(model, createDefaultModel());
    return;
  }

  if (props.operateType === 'edit' && props.rowData) {
    const modelDef: any = createDefaultModel();
    Object.keys(modelDef).forEach(key => {
      modelDef[key] = props.rowData[key];
    });
    Object.assign(model, modelDef);
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  if (props.operateType === 'add') {
    // request
    addHomeworkToCourse(props.course_name, {
      ...model,
      due_date: new Date(model.due_date),
    }).then(({ error }) => {
      if (!error) {
        window.$message?.success($t('Add Success!'));
        closeDrawer();
        emit('submitted');
      }
    });
  } else {
    // request
    updateHomeworkToCourse(props.course_name, {
      ...model,
      due_date: new Date(model.due_date),
    }).then(({ error }) => {
      if (!error) {
        window.$message?.success($t('Update Success!'));
        closeDrawer();
        emit('submitted');
      }
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
      <NForm ref="formRef" :model="model" :rules="rules" label-placement="left" :label-width="130">
        <NFormItem label="Homework Name" path="name">
          <NInput v-model:value="model.name" placeholder="Please Enter Problem Name" />
        </NFormItem>
        <NFormItem label="Description" path="description">
          <NInput v-model:value="model.description" placeholder="Please Enter Description" />
        </NFormItem>
        <NFormItem label="Due Date" path="due_date">
          <NDatePicker v-model:value="model.due_date" placeholder="Please Enter Due Date" />
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
