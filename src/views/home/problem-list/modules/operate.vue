<script setup lang="ts">
/* eslint-disable */
import { computed, defineComponent, reactive, ref, watch } from 'vue';
import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
// @ts-ignore
import Editor from '@/components/custom/aceEditor.vue';
// @ts-ignore
import { VMarkdownEditor } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'
import {
  addProblemByHomework,
  removeImage,
  updateProblemByHomework,
  uploadImage
} from '@/service/api/course';
import { getTokens } from '@/service/api/ai';
// @ts-ignore
import List from './List.vue';
// @ts-ignore
import Choice from './Choice.vue'
//@ts-ignore
import { useResolve } from '@/hooks/problem/useResolve'
import { nextTick } from 'vue';

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
  homework_name?: any;
}

const props = defineProps<Props>();
defineComponent({
  components: {
    ArchiveIcon
  }
});

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();
const imageList: any = ref([]);
const { resolveContentProblem,handleProblemDetail,getImageList } = useResolve();
const options = ref([
  {
    label: 'text',
    value: 'text'
  },
  {
    label: 'programming',
    value: 'programming'
  },
  {
    label: 'choice',
    value: 'choice'
  }
]);

const userTokenOptions = ref([]);

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: 'Add Problem',
    edit: 'Edit Problem'
  };
  return titles[props.operateType];
});

type Model = {
  title: string;
  content_problem: any;
  score: any;
  type: string;
  stem: string;
  response_limit: any;
  non_programming_answer: string;
  allow_ai: boolean;
  selected_token: number | null;
  stylescore: number | null;
  implescore: number | null;
  sample: string;
  sample_explanation: string;
  style_criteria: string;
  implement_criteria: string;
  additional: string;
};

const model: Model = reactive(createDefaultModel());
const id = ref(-1);

function createDefaultModel(): Model {
  imageList.value = [];
  return {
    title: '',
    content_problem: [],
    score: '',
    type: 'text',
    stem: '',
    response_limit: '',
    non_programming_answer: '',
    allow_ai: false,
    selected_token: null,
    implescore: null,
    stylescore: null,
    sample: '',
    sample_explanation: '',
    style_criteria: '',
    implement_criteria: '',
    additional: '',
  };
}

type RuleKey = Extract<keyof Model, 'userName' | 'userStatus'>;
const markdownStem = ref()
const rules: Record<RuleKey, App.Global.FormRule> = {
  userName: defaultRequiredRule,
  userStatus: defaultRequiredRule
};

function handleUpdateModelWhenEdit() {
  if (props.operateType === 'add') {
    Object.assign(model, createDefaultModel());
    nextTick(()=>{
        markdownStem.value.update(model.stem)
    })
    return;
  }

  if (props.operateType === 'edit' && props.rowData) {
    const modelDef: any = handleProblemDetail(props.rowData)
    modelDef.allow_ai = Boolean(modelDef.allow_ai)
    Object.assign(model, modelDef);
    id.value = props.rowData.id;
    nextTick(()=>{
        markdownStem.value.update(model.stem)
    })
    getImageList({course_name:props.course_name,homework_name:props.homework_name,id:id.value}).then((images)=>{
      imageList.value = images;
    })
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  const resolveItem = resolveContentProblem(model.type, model.content_problem,model.stem);
  if (props.operateType === 'add') {
    // request
    addProblemByHomework({ course_name: props.course_name, home_work: props.homework_name }, [
      {
        ...model,
        content_problem: resolveItem?.content_problem,
        non_programming_answer: resolveItem?.non_programming_answer
      }
    ]).then(async ({ error, data }) => {
      if (!error) {
        window.$message?.success($t('Add Success!'));
        if (imageList.value.length > 0) {
          uploadImage({
            course_name: props.course_name,
            home_work: props.homework_name,
            id: data[0].id,
            image: imageList.value[0].file
          });
        }
        closeDrawer();
        emit('submitted');
      }
    });
  } else {
    updateProblemByHomework({ course_name: props.course_name, home_work: props.homework_name }, [
      {
        ...model,
        content_problem: resolveItem?.content_problem,
        non_programming_answer: resolveItem?.non_programming_answer,
        id: id.value
      }
    ]).then(async ({ error }) => {
      if (!error) {
        window.$message?.success($t('Update Success!'));
        let result:any = imageList.value.filter((item:any)=>item.status==='pending')
        if (result.length > 0) {
          uploadImage({
            course_name: props.course_name,
            home_work: props.homework_name,
            id: id.value,
            image: result[0].file
          });
        }

        closeDrawer();
        emit('submitted');
      }
    });
  }
}
// const handleUploadImage = (data:any)=>{

// }
const handleRemove = (data: any) => {
  if (data.file.id) {
    removeImage({
      course_name: props.course_name,
      home_work: props.homework_name,
      id: id.value,
      image_id: data.file.id
    });
  }
};
const handleUploadChange = (data: { fileList: any[] }) => {
  imageList.value = data.fileList;
};
watch(visible, () => {
  if (visible.value) {
    handleUpdateModelWhenEdit();
    restoreValidation();

    getTokens().then(({ data, error }) => {
      if (!error && data) {
        // 将从API返回的数据格式化为 NSelect 需要的 { label, value } 格式
        userTokenOptions.value = data.map(token => ({
          label: `${token.platform} - ${token.name || 'Default'}`, // 例如 "DeepSeek - 我的备用Key"
          value: token.id // value 应该是 token 的唯一ID
        }));
      }
    });
  } else {
    userTokenOptions.value = [];
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" :title="title" display-directive="show" :width="840">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules" label-placement="left" :label-width="190">
        <NFormItem label="Problem Type" path="type">
          <NSelect
            v-model:value="model.type"
            :disabled="operateType === 'edit'"
            :options="options"
            placeholder="Please Select Problem Type"
          />
        </NFormItem>
        <NFormItem label="Problem Title" path="name">
          <NInput v-model:value="model.title" placeholder="Please Enter Problem Title" />
        </NFormItem>
        <NFormItem label="Problem Stem" path="stem">
          <div style="height:400px;overflow-y: hidden">
            <Editor :disabledLang="true" ref="markdownStem" locale="en" mode="markdown" editor-type="text" v-model:value="model.stem" />
          </div>
        </NFormItem>
        <NFormItem v-if="model.type !== 'programming'" label="Problem Content" path="description">
          <List v-if="model.type === 'text'" v-model:value="model.content_problem"></List>
          <Choice v-else v-model:value="model.content_problem"></Choice>
        </NFormItem>
        <NFormItem label="Upload Images" path="name">
          <n-upload
            v-model:file-list="imageList"
            multiple
            directory-dnd
            :max="5"
            @remove="handleRemove"
            @change="handleUploadChange"
          >
            <n-upload-dragger>
              <div style="margin-bottom: 12px">
                <n-icon size="48" :depth="3">
                  <ArchiveIcon />
                </n-icon>
              </div>
              <n-text style="font-size: 16px">
                <span style="color: #6941c6">Click to upload</span>
                or drag and drop
              </n-text>
            </n-upload-dragger>
          </n-upload>
        </NFormItem>
        <NFormItem label="Score" path="name">
          <NInput v-model:value="model.score" placeholder="Please Enter Score" />
        </NFormItem>
        <NFormItem label="Response Limit" path="response_limit">
          <NInput v-model:value="model.response_limit" placeholder="Please Enter Response Limit" />
        </NFormItem>
        <NFormItem v-if="model.type !== 'choice'" label="Allow AI" path="allow_ai">
          <NCheckbox v-model:checked="model.allow_ai" placeholder="Please Enter allow_ai" />
        </NFormItem>
        <NFormItem v-if="model.allow_ai" label="Select AI Token" path="selected_token">
          <NSelect v-model:value="model.selected_token" :options="userTokenOptions" placeholder="Please select a token" clearable/>
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">Cancel</NButton>
          <NButton type="primary" @click="handleSubmit">
            {{ props.operateType === 'add' ? 'Create' : 'Update' }}
          </NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
