<script setup lang="ts">
/* eslint-disable */
import { computed, defineComponent, reactive, ref, watch } from 'vue';
import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
// @ts-ignore
import Editor from '@/components/custom/aceEditor.vue';
// import {
//   addProblemByHomework,
//   updateProblemByHomework,
//   uploadImage
// } from '@/service/api/course';
// @ts-ignore
import List from './List.vue';
// @ts-ignore
import Choice from './Choice.vue'
//@ts-ignore
import { useResolve } from '@/hooks/problem/useResolve'

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
  /** the edit row data */
  rowData?: any;
  course_name?: any;
  title?: any;
  homework_name?: any;
}
const operateType = ref("add")

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

const visible = defineModel<boolean>('visible', {
  default: false
});
import { createCodeCase, queryCodeCase,removeCodeCase } from '@/service/api';
const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

type Model = {
  id?:any;
  "command_line_arguments": any,
  "standard_input": any,
  "standard_output": string,
  "time_limit": any,
  "space_limit": any,
  "score": any
};
const model: Model = reactive(createDefaultModel());
const valueRef = ref(1)
function createDefaultModel(): Model {
  imageList.value = [];
  return {
    "command_line_arguments": '',
    "standard_input": '',
    "standard_output": "",
    "time_limit": "",
    "space_limit": "",
    "score": ""
  };
}
const panelsRef = ref([{ label: 1, model: createDefaultModel() }])

type RuleKey = Extract<keyof Model, 'userName' | 'userStatus'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  userName: defaultRequiredRule,
  userStatus: defaultRequiredRule
};

function handleUpdateModelWhenEdit() {
  operateType.value = 'add'
  queryCodeCase({ course_name: props.course_name, homework_name: props.homework_name, id: props.rowData.id }).then(({data}) => {
    let panels:any[] = [];
    if(data && data.length > 0){
      operateType.value = 'edit'
      data.forEach((item:any,index:number)=>{
      panels.push({
        label:index+1,
        model:item
      })
    })
    panelsRef.value = panels;
    }
  })
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  let paramsWithId = panelsRef.value.filter((item:any)=>!!item.model.id).map((item) => item.model)
  let paramsWithoutId = panelsRef.value.filter((item:any)=>!item.model.id).map((item) => item.model)
  let notSubmit = true;
  if(paramsWithId.length > 0){
    createCodeCase({ course_name: props.course_name, homework_name: props.homework_name, params:paramsWithId, id: props.rowData.id,isUpdate:true}).then(({ error }) => {
      if (!error) {
        closeDrawer();
        if(notSubmit){
          notSubmit = false;
          emit('submitted');
        }

      }
    });
  }
  if(paramsWithoutId.length > 0){
    createCodeCase({ course_name: props.course_name, homework_name: props.homework_name, params:paramsWithoutId, id: props.rowData.id,isUpdate:false }).then(({ error }) => {
      if (!error) {
        closeDrawer();
        if(notSubmit){
          notSubmit = false;
          emit('submitted');
        }
      }
    });
  }

}
const addableRef = computed(() => {
  return {
    disabled: panelsRef.value.length >= 10
  }
})
const handleClose = (name: number) => {
  const { value: panels } = panelsRef
  const nameIndex = panels.findIndex((panel) => panel.label === name)
  if (!~nameIndex) return
  let item = panels.splice(nameIndex, 1)
  if(item && item[0].model.id){
    removeCodeCase({ course_name: props.course_name, homework_name: props.homework_name, id: props.rowData.id },item[0].model.id)
  }
  if (name === valueRef.value) {
    valueRef.value = panels[Math.min(nameIndex, panels.length - 1)].label
  }
}
const handleAdd = () => {
  let label = panelsRef.value[ panelsRef.value.length-1].label+1
  panelsRef.value.push({
    label,
    model: createDefaultModel()
  })
  valueRef.value = label
}
const closableRef = computed(() => {
  return panelsRef.value.length > 1
})
watch(visible, () => {
  if (visible.value) {
    handleUpdateModelWhenEdit();
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" title="Add .in and .out for coding problem" display-directive="show" :width="840">
    <NDrawerContent title="Add .in and .out for coding problem" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules" label-placement="left" :label-width="210">
        <n-tabs style="height:100%" v-model:value="valueRef" type="card" :addable="addableRef" :closable="closableRef"
          tab-style="min-width: 80px;" @close="handleClose" @add="handleAdd">
          <n-tab-pane style="height:100%" v-for="panel in panelsRef" :key="panel.label" :name="panel.label">
            <NFormItem label="Space Limit" path="space_limit">
              <NInput v-model:value="panel.model.space_limit" placeholder="Please Enter Space Limit" />
            </NFormItem>
            <NFormItem label="Time Limit" path="time_limit">
              <NInput v-model:value="panel.model.time_limit" placeholder="Please Enter Time Limit" />
            </NFormItem>
            <NFormItem label="Command Line Arguments" path="time_limit">
              <NInput v-model:value="panel.model.command_line_arguments" placeholder="Please Enter Command Line Arguments" />
            </NFormItem>
            <NFormItem label="Add .in" path="standard_input">
              <NInput type="textarea" v-model:value="panel.model.standard_input" placeholder="Please Enter Add .in" />
            </NFormItem>
            <NFormItem label="Add .out" path="standard_output">
              <NInput type="textarea" v-model:value="panel.model.standard_output" placeholder="Please Enter Add .out" />
            </NFormItem>
            <NFormItem label="score" path="stem">
              <NInput v-model:value="panel.model.score" placeholder="Please score" />
            </NFormItem>
          </n-tab-pane>
        </n-tabs>
      </NForm>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">Cancel</NButton>
          <NButton type="primary" @click="handleSubmit">
            {{ operateType === 'add' ? 'Create' : 'Update' }}
          </NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
