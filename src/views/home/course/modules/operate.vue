<script setup lang="tsx">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { addCourse, getStudentList, getStudentListByCourseName, updateCourse } from '@/service/api/course';

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
const options = ref([]);
const origin_course_name = ref('');

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: 'Add Course',
    edit: 'Edit Course'
  };
  return titles[props.operateType];
});
onMounted(() => {
  getStudentList().then(res => {
    if (!res.error) {
      options.value = res.data.map((item: any) => ({
        label: `${item.first_name} ${item.username}`,
        value: item.username
      }));
    }
  });
});
type Model = {
  course_name: string;
  students_list: string[];
};

const model: Model = reactive(createDefaultModel());

function createDefaultModel(): Model {
  return {
    course_name: '',
    students_list: []
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
    getStudentListByCourseName(props.rowData.course_name).then(({ data, error }) => {
      if (!error) {
        origin_course_name.value = props.rowData.course_name;
        Object.assign(model, props.rowData, { students_list: data.map((item: any) => item.username) });
      }
    });
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  if (props.operateType === 'add') {
    // request
    addCourse(model).then(() => {
      window.$message?.success($t('Add Success!'));
      closeDrawer();
      emit('submitted');
    });
  } else {
    // request
    updateCourse(origin_course_name.value, model).then(() => {
      window.$message?.success($t('Update Success!'));
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
        <NFormItem label="Course Name" path="course_name">
          <NInput
            v-model:value="model.course_name"
            :disabled="operateType == 'add' ? false : true"
            :placeholder="$t('page.manage.menu.form.menuName')"
          />
        </NFormItem>
        <NFormItem label="Students List" path="students_list">
          <n-select v-model:value="model.students_list" :multiple="true" :options="options"></n-select>
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
