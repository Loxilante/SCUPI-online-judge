<script setup lang="tsx">
/* eslint-disable */
import { onMounted, ref } from 'vue';
//@ts-ignore
import Code from './modules/Code.vue'
//@ts-ignore
import Text from './modules/Text.vue'
//@ts-ignore
import Description from './modules/Description.vue'
//@ts-ignore
import { useResolve } from '@/hooks/problem/useResolve'
import { getProblemDetail, viewSubmissionRecord, getCourseUsers, removeCommentForQuestion } from '@/service/api/course'
import { useRoute } from 'vue-router';
import moment from 'moment';
import { nextTick } from 'vue';
import { useAuthStore } from '@/store/modules/auth';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from './modules/operate.vue';
import { useBoolean } from '~/packages/hooks/src';
const route = useRoute();

const imageList: any = ref([]);
const model: any = ref({});
const modelList: any = ref([]);
const { bool: drawerVisible, setTrue: openDrawer } = useBoolean();
const codeRef = ref();
const selected = ref(0)
const users = ref([])
const submitted = ref(false)
const authStore = useAuthStore();
const curUsername = ref(route.query.username ? route.query.username : authStore.userInfo.username)
const { handleProblemDetail, getImageList } = useResolve();
const getData = () => {
  selected.value = 0
  getProblemDetail({ course_name: route.query.course_name, home_work: route.query.homework_name, id: route.query.problemId }).then((res) => {
    if (res.data && res.data.length) {
      let modelArr: any[] = []
      viewSubmissionRecord({ course_name: route.query.course_name, homework_name: route.query.homework_name, id: route.query.problemId, username: curUsername.value }).then((res2) => {
        if (res2.data.length > 0) {
          submitted.value = true
          res2.data.forEach((item: any, index: number) => {
            if (res.data[0].type !== 'programming') {
              modelArr.push({ ...item, value: index, label: 'submit time:' + moment(item.submit_time).format("YYYY-MM-DD HH:mm:ss"), ...handleProblemDetail({ ...res.data[0], non_programming_answer: item.content_answer }), totalScore: res.data[0].score, score: item.score || 0 })
            } else {
              modelArr.push({
                ...item,
                ...handleProblemDetail({ ...res.data[0], non_programming_answer: item.content_answer.replace("<-&cpp&-><-&main.cpp&->", "") }),
                totalScore: res.data[0].score,
                score: item.score || 0,
                value: index,
                label: 'submit time:' + moment(item.submit_time).format("YYYY-MM-DD HH:mm:ss")
              })
            }
          })
        } else {
          submitted.value = false
          res.data.forEach((item: any, index: number) => {
            modelArr.push({
              ...item,
              totalScore: item.score,
              ...handleProblemDetail({ ...item, non_programming_answer: "" }),
              value: index
            })
          })
        }
        modelList.value = modelArr
        model.value = modelArr[selected.value]
        setTimeout(() => {
          update()
        }, 400)
      })
    }
  })
}
onMounted(() => {
  getCourseUsers(route.query.course_name).then(({ data }) => {
    users.value = data.map((item: any) => (
      {
        label: item.first_name+' '+item.username,
        value: item.username
      }
    ))
  })
  getImageList({ course_name: route.query.course_name, homework_name: route.query.homework_name, id: route.query.problemId }).then((images) => {
    imageList.value = images;
  })
})
const operateType = ref<OperateType>('add');
const language = ref("")
const update = () => {
  if (!codeRef.value) return
  if(!submitted.value){
    codeRef.value.updatePanel([])
    return
  }
  let reg = /(<-&)(.*)(&->)/ig
  let regLang = /(<-&)(cpp|java)(&->)/ig
  let content_answer = model.value.content_answer || ""
  let langArr = content_answer.match(regLang)
  let mapping: any = {
    "java": "java",
    "cpp": "c_cpp"
  }
  let lang = ""
  if (langArr && langArr.length > 0) {
    lang = langArr[0].replace("<-&", "").replace("&->", "")
  }
  language.value = mapping[lang]
  let content1 = content_answer.replace(regLang, "")
  let titles = content1.match(reg).map((item: string) => item.replace("<-&", "").replace("&->", ""))
  let contents = content1.replace(reg, "$coding$").split("$coding$")
  contents.shift()
  contents = contents.map((item: string) => item.replace("<-&", "").replace("&->", ""))
  nextTick(() => {
    let panels: any = []
    contents.forEach((item: any, index: number) => {
      panels.push({
        label: titles[index],
        codeAnserList: [
          {
            type: mapping[lang],
            question: item
          }
        ]
      })
    })
    codeRef.value.updatePanel(panels)
  })
}
onMounted(() => {
  getData()
})
const handleEdit = () => {
  operateType.value = 'edit';
  openDrawer();
}
const handlePositiveClick = () => {
  removeCommentForQuestion({ course_name: route.query.course_name, homework_name: route.query.homework_name, id: route.query.problemId }, {
    delete_id: [model.value.id]
  }).then(() => {
    getData()
  })
}
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard :title="model.title" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <div class="header">
        <div class="header-cont">
          <span v-p="'level2'" style="display: inline-flex;width:30px;height:24px;align-items: center;" @click="() => {
      //@ts-ignore
      let ind = users.findIndex((item) => item.value == curUsername)
      if (ind == 0) return
      //@ts-ignore
      curUsername = users[ind - 1].value
      getData()
    }">
            <SvgIcon class="icons" icon="teenyicons:left-solid" style="color: #fff;margin-right: 5px;" />
          </span>
          <NSelect v-p="'level2'" @change="getData" v-model:value="curUsername" class="select" :options="users">
          </NSelect>
          <span v-p="'level2'" style="display: inline-flex;width:30px;height:24px;align-items: center;" @click="() => {
      //@ts-ignore
      let ind = users.findIndex((item) => item.value == curUsername)
      if (ind > users.length - 2) return
      //@ts-ignore
      curUsername = users[ind + 1].value
      getData()
    }">
            <SvgIcon class="icons" icon="teenyicons:right-solid" style="color: #fff;margin-right: 5px" />
          </span>
          <span v-if="submitted" class="score">Score:{{ model.score }}/{{ model.totalScore }}</span>
          <NSelect v-if="submitted" class="select" @change="(selectIndex) => {
      model = modelList[selectIndex]
      update()
    }" v-model:value="selected" :options="modelList"></NSelect>
          <NButton v-p="'level2'" v-if="submitted" @click="handleEdit" style="margin-left: 8px;" type="warning">Comment
          </NButton>
          <n-popconfirm v-if="submitted" positive-text="Ok" negative-text="Cancel"
            @positive-click="handlePositiveClick">
            <template #trigger>
              <n-button v-p="'level2'" style="margin-left: 8px;" type="error">Delete</n-button>
            </template>
            {{ $t('common.confirmDelete') }}
          </n-popconfirm>
        </div>
        <div class="header-comment">
          Comment：{{ model.comment }}
        </div>
      </div>
      <Code :submitted="submitted" :mode="language" :ref="el => codeRef = el" @getData="getData" :course_name="route.query.course_name"
        :id="route.query.problemId" :homework_name="route.query.homework_name" v-if="model.type == 'programming'"
        :item="model" :imageList="imageList"></Code>
      <Description :course_name="route.query.course_name" :id="route.query.problemId"
        :homework_name="route.query.homework_name" v-else :imageList="imageList" :item="model"></Description>
    </NCard>
    <MenuOperateDrawer v-model:visible="drawerVisible" :course_name="route.query.course_name"
      :operate-type="operateType" :row-data="model" @submitted="getData" />
  </div>
</template>

<style lang="scss" scoped>
.header {
  background-color: #7F56D9;
  border-radius: 5px;
  box-shadow: 1px 1px 12px rgba(0, 0, 0, .6);
  margin-bottom: 8px;
  padding: 10px;
}
.header-cont{
  display: flex;
  align-items: center;

  min-height: 70px;
}
.header-comment{
  color: #fff;
  white-space: pre-wrap;
}
.score {
  display: flex;
  width: 120px;
  font-weight: bold;
  font-size: 16px;
  color: #fff;
}

.flex-vertical-stretch :deep(.n-card__content) {
  flex: auto;
  height: calc(100% - 50px);
}

.select {
  width: 220px;
  background-color: transparent;
  color: #fff;
  margin-right: 8px;
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

.submit {
  display: flex;
  justify-content: flex-end
}
</style>
