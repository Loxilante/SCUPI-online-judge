<script setup lang="tsx">
/* eslint-disable */
import { computed, reactive, watch } from 'vue';
//@ts-ignore
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
//@ts-ignore
import { $t } from '@/locales';
//@ts-ignore
import { commentForQuestion } from '@/service/api/course';
import { useRoute } from 'vue-router';
const route = useRoute();
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
    add: 'Comment',
    edit: 'Comment'
  };
  return titles[props.operateType];
});
type Model = {
  "score": string;
  "comment": string;
};

const model: Model = reactive(createDefaultModel());

function createDefaultModel(): Model {
  return {
    "score": "",
    "comment": ""
  };
}

type RuleKey = Extract<keyof Model, 'userName' | 'userStatus'>;

const rules: Record<RuleKey, any> = {
  userName: defaultRequiredRule,
  userStatus: defaultRequiredRule
};

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  commentForQuestion({ course_name: route.query.course_name, homework_name: route.query.homework_name, id: route.query.problemId },{
    score:model.score,
    comment:model.comment,
    submission_id:props.rowData.id
  }).then(() => {
    (window as any).$message?.success($t('Update Success!'));
    closeDrawer();
    emit('submitted');
  });
}

watch(visible, () => {
  if (visible.value) {
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" :title="title" display-directive="show" :width="480">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules" label-placement="left" :label-width="120">
        <NFormItem label="Score" path="score">
          <NInput v-model:value="model.score" placeholder="Please Input score" />
        </NFormItem>
        <NFormItem label="Comment" path="comment">
          <NInput v-model:value="model.comment" placeholder="Please Input comment" />
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
