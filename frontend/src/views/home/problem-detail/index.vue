<script setup lang="tsx">
/* eslint-disable */
import { onMounted, ref } from 'vue';
//@ts-ignore
import Code from './modules/Code.vue'
//@ts-ignore
import Description from './modules/Description.vue'
//@ts-ignore
import { useResolve } from '@/hooks/problem/useResolve'
import { getProblemDetail } from '@/service/api/course'
import { useRoute } from 'vue-router';
const route = useRoute();

const imageList: any = ref([]);
const model: any = ref({});
const { handleProblemDetail, getImageList } = useResolve();
const handleAgain = (tmp: any) => {
  if (tmp.type == 'text') {
    tmp.content_problem.forEach((it: any) => {
      let ques = it.question;
      let spQues = ques.split("，__")[0]
      it.question = spQues
      it.answer = ''
    })
  } else if (tmp.type == 'choice') {
    tmp.content_problem.forEach((it: any) => {
      it.checked = false
    })
  } else {
    tmp.content_problem.forEach((it: any) => {
      it.question = it.question.trimStart()
    })
  }
  return tmp
}
const getData = ()=>{
  getProblemDetail({ course_name: route.query.course_name, home_work: route.query.homework_name, id: route.query.problemId }).then((res) => {
    if (res.data && res.data.length) {
      model.value = {...handleAgain(handleProblemDetail(res.data[0])),score_get:res.data[0].score_get}
    }
  })
}
onMounted(() => {
  getData()
})
getImageList({ course_name: route.query.course_name, homework_name: route.query.homework_name, id: route.query.problemId }).then((images) => {
  imageList.value = images;
})
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard :title="`${model.title} Score:${model.score_get}/${model.score}`" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <Code @getData="getData" :course_name="route.query.course_name" :id="route.query.problemId" :homework_name="route.query.homework_name" v-if="model.type == 'programming'" :item="model" :imageList="imageList"></Code>
      <Description @getData="getData" :course_name="route.query.course_name" :id="route.query.problemId" :homework_name="route.query.homework_name" v-else :imageList="imageList" :item="model"></Description>
      <!-- <div class="submit">
        <NButton type="primary">submit</NButton>
      </div> -->
    </NCard>
  </div>
</template>

<style lang="scss" scoped>
:deep(.n-card-header__main){
    font-size: 30px;
    color: #6941c6 !important;
}
.top {
  background-color: #fff;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;

  h3 {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    display: flex;
    align-items: center;
  }
  .score {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #6941c6;
    height: 18px;
    margin-left: 8px;
    border-radius: 3px;
    font-weight: normal;
    padding: 8px;
    border: 1px solid #6941c6;
  }

  .des {
    font-size: 12px;
    color: #999;
  }

  .create_time {
    font-size: 12px;
    color: #6941c6;
  }

  .remainTime {
    margin-left: 10px;
    font-size: 12px;
    color: #db68cd;
  }
}
.flex-vertical-stretch :deep(.n-card__content){
  flex:auto;
  height: calc(100% - 50px);
}
.submit {
  display: flex;
  justify-content: flex-end
}
</style>
