<script setup lang="ts">
/* eslint-disable */
import { Problem } from './problem.d'
import { defineProps, ref, defineExpose } from 'vue'
import { useMessage } from 'naive-ui'
//@ts-ignore
import aceEditor from '@/components/custom/aceEditor.vue';
//@ts-ignore
import { VMarkdownView } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'
import { nextTick,watch } from 'vue';
const props = defineProps<{ item: Problem,submitted:boolean, imageList: any[], course_name: any; homework_name: any, id: any,mode?:any }>();
const valueRef = ref('main')
const panelsRef = ref([{ label: 'main', codeAnserList: [] }])
const visible = ref(false)
const codeMapRef:any = ref({});
const message = useMessage()
const fileName = ref("")
const updatePanel = (panels?: any) => {
  if(panels){
    panelsRef.value = [...panels]
    valueRef.value = panelsRef.value[0].label
  }
  nextTick(()=>{
    panelsRef.value.forEach((item:any,index:number)=>{
      codeMapRef.value[index] && codeMapRef.value[index].update(item.codeAnserList)
    })
  })
}
defineExpose({
  updatePanel
})
const emit = defineEmits(['getData']);
function onPositiveClick() {
  if (fileName.value == '') {
    message.error("fileName is empty")
    return
  }
  panelsRef.value.push({
    label: fileName.value,
    codeAnserList: []
  })
  valueRef.value = fileName.value
  visible.value = false
}
function onNegativeClick() {
  visible.value = false
}
watch(valueRef,()=>{
  updatePanel()
})
</script>
<template>
  <div class="code">
    <div class="left" :style="{ width: '500px' }">
      <VMarkdownView :content="props.item.stem"></VMarkdownView>
      <div class="images">
        <img v-for="(img, index) in props.imageList" :key="index" class="img" :src="img.file" />
      </div>
      <div class="item" v-for="(item, index) in props.item.content_problem" :key="index">
        <VMarkdownView :content="item.question" mode="light" />
      </div>
    </div>
    <div class="right" :style="{ width: 'calc(100% - 500px)' }">
      <n-tabs style="height:100%" v-model:value="valueRef" type="card" tab-style="min-width: 80px;">
        <n-tab-pane style="height:100%" v-for="(panel,index) in panelsRef" :key="panel.label" :name="panel.label">
          <div class="editorItem">
            <aceEditor :ref="(el)=>{
              codeMapRef[index] = el;
            }" :mode="props.mode" :disabled="true" :idKey="panel" width="100%" height="calc(100% - 28px)">
            </aceEditor>
          </div>
        </n-tab-pane>
      </n-tabs>
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
  height: calc(100% - 140px);
  margin-top: 10px;
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
  width: 700px;
  display: flex;
  align-items: center;
}

.submit-btns {
  display: flex;
}

.submit-btn {
  margin-right: 8px;
}
</style>
