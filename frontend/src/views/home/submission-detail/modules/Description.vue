<script setup lang="ts">
/* eslint-disable */
import { Problem } from './problem.d'
//@ts-ignore
import { VMarkdownView } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'
import { defineProps } from 'vue'
import { useResolve } from '@/hooks/problem/useResolve';
const emit = defineEmits(['getData']);
const { mapping } = useResolve();
const props = defineProps<{ item: Problem, imageList: any[], course_name: any; homework_name: any, id: any }>();
</script>
<template>
  <div class="code">
    <div style="height: 100%;">
      <VMarkdownView :content="props.item.stem" mode="light" />
      <div class="images">
        <img v-for="(img, index) in props.imageList" :key="index" class="img" :src="img.file" />
      </div>
      <div v-if="props.item.type == 'text'">
        <div class="item" v-for="(item, index) in props.item.content_problem" :key="index">
          <p class="item-span">{{ item.question }}，
            <NInput type="textarea" :disabled="true" v-model:value="item.answer" size="small" placeholder="Please Input Answer"
              class="input" />
          </p>
        </div>
      </div>
      <div v-if="props.item.type == 'choice'">
        <div class="item" v-for="(item, index) in props.item.content_problem" :key="index">
          <NCheckbox :disabled="true" v-model:checked="item.checked" class="item-span">{{mapping[index]}}. {{ item.question }}</NCheckbox>
        </div>
      </div>
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
  width:700px;
}
.item-span{
  display: flex;
}
.code {
  height: calc(100% - 120px);
  overflow-y: auto;
}
.img {
  display: block;
  width: 200px;
  margin-top: 10px;
  margin-bottom: 10px;
}
.submit-btns{
  display: flex;
  justify-content: flex-end;
}
</style>
