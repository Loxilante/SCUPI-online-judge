<script setup lang="ts">
/* eslint-disable */
import { Problem } from './problem.d'
import { defineProps } from 'vue'
import { codeSubmit } from '@/service/api';
import { useMessage } from 'naive-ui';
import { useResolve } from '@/hooks/problem/useResolve';
//@ts-ignore
import { VMarkdownView } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'
const message = useMessage()
const { mapping } = useResolve();
const emit = defineEmits(['getData']);
const props = defineProps<{ item: Problem, imageList: any[], course_name: any; homework_name: any, id: any }>();
const handleSubmit = () => {
  let ret = ""
  props.item.content_problem.forEach((item, index: number) => {
    if (props.item.type == 'text') {
      ret += `<-&${item.answer}&->${index < props.item.content_problem.length - 1 ? '|' : ''}`
    } else {
      if (item.checked) { }
      ret += `<-&${item.checked ? item.question : 'incorrect'}&->${index < props.item.content_problem.length - 1 ? '|' : ''}`
    }
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
</script>
<template>
  <div style="height:100%;">
    <div class="code">
      <div>
        <VMarkdownView :content="props.item.stem" mode="light" />
        <div class="images">
          <img v-for="(img, index) in props.imageList" :key="index" class="img" :src="img.file" />
        </div>
        <div v-if="props.item.type == 'text'">
          <div class="item" v-for="(item, index) in props.item.content_problem" :key="index">
            <p class="item-span">{{ item.question }}，
              <NInput type="textarea" v-model:value="item.answer" size="small" placeholder="Please Input Answer" class="input" />
            </p>
          </div>
        </div>
        <div v-if="props.item.type == 'choice'">
          <div class="item" v-for="(item, index) in props.item.content_problem" :key="index">
            <NCheckbox v-model:checked="item.checked" class="item-span">{{ mapping[index] }}. {{ item.question }}
            </NCheckbox>
          </div>
        </div>
      </div>
    </div>
    <div class="submit-btns">
        <NButton @click="handleSubmit" type="primary">Submit</NButton>
    </div>
  </div>
</template>
<style scoped>
.stem {
  font-size: 18px;
}

.item-span {
  font-size: 14px;
  padding-bottom: 8px;
  color: #666;
}

.input {
  width: 700px;
}

.code {
  height: calc(100% - 40px);
  overflow-y: auto;
}

.img {
  display: block;
  width: 200px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.submit-btns {
  display: flex;
  justify-content: flex-end;
}
.item-span{
  display: flex;
}
</style>
