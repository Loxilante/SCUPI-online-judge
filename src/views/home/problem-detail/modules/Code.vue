<script setup lang="ts">
/* eslint-disable */
import { Problem } from './problem.d'
import { computed, defineProps, ref } from 'vue'
import { useMessage } from 'naive-ui'
import { runcode, codeSubmit } from '@/service/api/course'
//@ts-ignore
import { VMarkdownView } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'
//@ts-ignore
import aceEditor from '@/components/custom/aceEditor.vue';
const standard_input = ref("")
const standard_output = ref("")
const command_line_arguments = ref("")
const space_limit = ref("1000")
const time_limit = ref("1000")
const props = defineProps<{ item: Problem, imageList: any[], course_name: any; homework_name: any, id: any }>();
const valueRef = ref('main.cpp')
const panelsRef = ref({
  lang:'c_cpp',
  data:[{ label: 'main.cpp', codeAnserList: [] }]
})
const visible = ref(false)
const message = useMessage()
const dialogOperate = ref({
  type: "add",
  index: -1
})
const fileName = ref("")
const addableRef = computed(() => {
  return {
    disabled: panelsRef.value.data.length >= 10
  }
})
const emit = defineEmits(['getData']);
let mapping:any = {
    "c_cpp":"<-&cpp&->",
    "java":"<-&java&->"
}
const preTest = () => {
  let ret = mapping[panelsRef.value.lang]
  panelsRef.value.data.forEach((item) => {
    item.codeAnserList.forEach((data: any) => {
      ret += `<-&${item.label}&-><-&${data.question}&->`
    })
  })
  runcode({
    code: ret,
    "space_limit": Number(space_limit.value),
    "time_limit": Number(time_limit.value),
    "command_line_arguments": command_line_arguments.value,
    "standard_input": standard_input.value
  }).then(({ data }) => {
    standard_output.value = JSON.stringify(data)
  })
}
const handleSubmit = () => {
  let ret = mapping[panelsRef.value.lang]
  panelsRef.value.data.forEach((item) => {
    item.codeAnserList.forEach((data: any) => {
      ret += `<-&${item.label}&-><-&${data.question}&->`
    })
  })
  codeSubmit({
    content_answer: ret,
    id: props.id,
    course_name: props.course_name,
    homework_name: props.homework_name
  }).then(({ data }) => {
    message.success("submit success!")
    emit("getData")
  })
}
const closableRef = computed(() => {
  return panelsRef.value.data.length > 1
})
const handleAdd = () => {
  fileName.value = ''
  dialogOperate.value = {
    type: 'add',
    index: -1
  }
  visible.value = true
}
function onPositiveClick() {
  if (fileName.value == '') {
    message.error("fileName is empty")
    return
  }
  if (dialogOperate.value.type == 'add') {
    panelsRef.value.data.push({
      label: fileName.value,
      codeAnserList: []
    })
  } else {
    panelsRef.value.data[dialogOperate.value.index].label = fileName.value
  }
  valueRef.value = fileName.value
  visible.value = false

}
function onNegativeClick() {
  visible.value = false
}
const handleClose = (name: string) => {
  const { value: panels } = panelsRef
  const nameIndex = panels.data.findIndex((panel) => panel.label === name)
  if (!~nameIndex) return
  panels.data.splice(nameIndex, 1)
  if (name === valueRef.value) {
    valueRef.value = panels.data[Math.min(nameIndex, panels.data.length - 1)].label
  }
}

</script>
<template>
  <div class="code">
    <div class="left" :style="{ width: '500px' }">
      <VMarkdownView :content="props.item.stem" mode="light" />
      <div class="images">
        <img v-for="(img, index) in props.imageList" :key="index" class="img" :src="img.file" />
      </div>
      <div class="item" v-for="(item, index) in props.item.content_problem" :key="index">
        <VMarkdownView :content="item.question" mode="light" />
      </div>
    </div>
    <div class="right" :style="{ width: 'calc(100% - 500px)' }">
      <n-tabs @dblclick="(e: any) => {
      if(!(e.target.className as string).includes('n-tabs-tab__label')){
        return
      }
      fileName = e.target.innerText
      dialogOperate = {
        type: 'edit',
        index: panelsRef.data.findIndex((item) => item.label == fileName)
      }
      visible = true
    }" style="height:100%" v-model:value="valueRef" type="card" :addable="addableRef" :closable="closableRef"
        tab-style="min-width: 80px;" @close="handleClose" @add="handleAdd">
        <n-tab-pane style="height:100%" v-for="panel in panelsRef.data" :key="panel.label" :name="panel.label">
          <div class="editorItem">
            <aceEditor :just-for-code="true" @change="(mode:any)=>{
              panelsRef.lang = mode;
            }" :mode="panelsRef.lang" :idKey="panel" width="100%" height="100%" v-model:value="panel.codeAnserList">
            </aceEditor>
          </div>
        </n-tab-pane>
      </n-tabs>
      <div class="buttonGroup">
        <div class="button-flex">
          <NFormItem label-placement="left" label="Space Limit" class="button-input">
            <NInput v-model:value="space_limit" placeholder="= space_limit" />
          </NFormItem>
          <NFormItem label-placement="left" label="Time Limit" class="button-input">
            <NInput v-model:value="time_limit" placeholder="=time_limit" />
          </NFormItem>
          <NFormItem label-placement="left" label="Comm Args" class="button-input">
            <NInput v-model:value="command_line_arguments" placeholder="command_line_arguments" />
          </NFormItem>
          <NFormItem label-placement="left" label="Input" class="button-input">
            <NInput type="textarea" v-model:value="standard_input" placeholder="Please Enter Input" />
          </NFormItem>
          <NFormItem label-placement="left" label="Output" class="button-input">
            <NInput :disabled="true" type="textarea" v-model:value="standard_output" placeholder="" />
          </NFormItem>
        </div>
        <div class="submit-btns">
          <NButton class="submit-btn" @click="preTest" type="success">Pretest</NButton>
          <NButton @click="handleSubmit" type="primary">Submit</NButton>
        </div>
      </div>
    </div>
    <n-modal preset="dialog" title="Code FileName" @positive-click="onPositiveClick" @negative-click="onNegativeClick"
      positive-text="Confirm" negative-text="Cancel" v-model:show="visible">
      <div>
        <n-input v-model:value="fileName" placeholder="Please Input Code FileName" />
      </div>
    </n-modal>
  </div>
</template>
<style scoped>
.code {
  height: calc(100% - 130px);
  overflow-y: auto;
}

.left,
.right,
.editorItem,
.editorItem>div {
  height: 100%;
}

.left {
  width: 350px;
  margin-right: 20px;
  overflow-y: auto;
}

.code {
  display: flex;
}

.right {
  overflow-y: hidden;
}

.editorItem {
  margin-top: 12px;
}

.buttonGroup,
.button-flex {
  display: flex;
}

.button-flex {
  align-items: center;
}

.buttonGroup {
  align-items: center;
  position: fixed;
  padding-right: 20px;
  right: 0;
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  bottom: 0;
  z-index: 200;
  background-color: #fff;
  justify-content: flex-end;
  box-shadow: 1px 1px 12px rgba(0, 0, 0, .2);
}

.button-input {
  margin-right: 20px;
  width: 200px;
  display: flex;
  align-items: center;
}

.submit-btns {
  display: flex;
}

.submit-btn {
  margin-right: 64px;
}

.right :deep(.n-tabs-nav) {
  overflow-x: auto;
}

.right :deep(.n-tabs-nav-scroll-content) {
  display: flex;
  flex-wrap: nowrap;
}
</style>
