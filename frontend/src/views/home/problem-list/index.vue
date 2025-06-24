<script setup lang="tsx">
/* eslint-disable */
import { onMounted, onUnmounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { NButton, NPopconfirm } from 'naive-ui';
import { useBoolean } from '@sa/hooks';
import moment from 'moment';
import { getHomeworkByCourse, getProblemByHomework } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
import { removeQuestion } from '@/service/api/course';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from './modules/operate.vue';
//@ts-ignore
import caseDialog from './modules/case-dialog.vue'
import aiDialog from './modules/ai-dialog.vue'
const appStore = useAppStore();
const { bool: drawerVisible, setTrue: openDrawer } = useBoolean();
const { bool: caseDrawerVisible, setTrue: caseOpenDrawer } = useBoolean();
const { bool: aiDrawerVisible, setTrue: aiOpenDrawer } = useBoolean();
const route = useRoute();
const homeworkDetail = ref({
  created_time: '',
  description: '',
  due_date: '',
  name: '',
  score_get: 0,
  sum_score: 0
});
const remainTime = ref('');

const aiFormData = ref({
  sample: '',
  sample_explanation: '',
  style_criteria: '',
  implement_criteria: '',
  additional: ''
});
const AIOpenDrawer = (row: any) => {
  editingData.value = row;
  aiFormData.value = {
    sample: row.sample || '',
    sample_explanation: row.sample_explanation || '',
    style_criteria: row.style_criteria || '',
    implement_criteria: row.implement_criteria || '',
    additional: row.additional || ''
  };
  aiOpenDrawer();
  console.log(aiDrawerVisible.value);
};

const { columns, filteredColumns, data, loading, getData } = useTable<
  any,
  typeof getProblemByHomework,
  'index' | 'operate'
>({
  apiFn: getProblemByHomework,
  transformer: res => {
    const list: any = res.data || [];
    return {
      data: list,
      pageNum: 1,
      pageSize: 10,
      total: list.length
    };
  },
  apiParams: { course_name: route.query.course_name, home_work: route.query.homework_name },
  columns: () => [
    {
      key: 'title',
      title: 'Title',
      width:150,
      render: row => {
        return (
          <RouterLink to={`/home/problem-detail?course_name=${route.query.course_name}&homework_name=${route.query.homework_name}&problemId=${row.id}`}>
            {row.title}
          </RouterLink>
        );
      },
      align: 'center'
    },
    {
      key: 'type',
      width:60,
      title: 'Type',
      align: 'center'
    },
    {
      key: 'response_limit',
      width:60,
      title: 'Response Limit',
      align: 'center'
    },
    {
      key: 'score_get',
      width:50,
      title: 'Score Get',
      render:(row)=>{
        return `${row.score_get}/${row.score}`
      },
      align: 'center'
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 300,
      render: row => (
        <div class="flex-center gap-8px">
          <RouterLink v-p="level2" to={`/home/records?course_name=${route.query.course_name}&homework_name=${route.query.homework_name}&problemId=${row.id}`}>
              <NButton type="primary" ghost size="small">
                {'Course Records'}
              </NButton>
          </RouterLink>
          <NButton v-p="level2" type="primary" ghost size="small" onClick={() => handleEdit(row.id)}>
            {$t('common.edit')}
          </NButton>
          <RouterLink to={`/home/submission-detail?course_name=${route.query.course_name}&homework_name=${route.query.homework_name}&problemId=${row.id}`}>
            <NButton type="primary" ghost size="small" onClick={() => {
            }}>
              {'Submission History'}
            </NButton>
          </RouterLink>
          {row.type == 'programming' && <NButton v-p="level2" type="primary" ghost size="small" onClick={() => {
            editingData.value = data.value.find((item: any) => item.title === row.title) || null;
            caseOpenDrawer();
          }}>
            {'Case'}
          </NButton>}
          {row.allow_ai && (
            <NButton v-p="level2" type="success" ghost size="small" onClick={() => {
              AIOpenDrawer(row);
            }}>
              {'AI'}
            </NButton>
          )}
          <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
            {{
              default: () => $t('common.confirmDelete'),
              trigger: () => (
                <NButton v-p="level2" type="error" ghost size="small">
                  {$t('common.delete')}
                </NButton>
              )
            }}
          </NPopconfirm>
        </div>
      )
    }
  ]
});

const operateType = ref<OperateType>('add');
let interval: any;

function handleAdd() {
  operateType.value = 'add';
  openDrawer();
}

const checkedRowKeys = ref<string[]>([]);

/** the editing row data */
const editingData = ref<any>(null);

function handleEdit(id: string) {
  operateType.value = 'edit';
  editingData.value = data.value.find((item: any) => item.id === id) || null;
  openDrawer();
}
onMounted(() => {
  getHomeworkByCourse({
    coursename: route.query.course_name
  }).then(res => {
    if (!res.error) {
      res.data.forEach((item: any) => {
        if (item.name === route.query.homework_name) {
          homeworkDetail.value = item;
          interval = setInterval(() => {
            const remain = Number(new Date(homeworkDetail.value.due_date)) - Number(new Date());
            // 计算时间
            const seconds = Math.floor((remain / 1000) % 60);
            const minutes = Math.floor((remain / 1000 / 60) % 60);
            const hours = Math.floor((remain / (1000 * 60 * 60)) % 24);
            const days = Math.floor(remain / (1000 * 60 * 60 * 24));
            remainTime.value = `${days}days ${hours}h ${minutes}m ${seconds}s`;
          }, 1000);
        }
      });
    }
  });
});
onUnmounted(() => {
  clearInterval(interval);
  interval = null;
});
const formatDate = (date: any) => moment(date).format('YYYY-MM-DD');
// watch(selected_coursename, () => {
//   _getCourseList();
// });

async function handleDelete(id: string) {
  removeQuestion(route.query.course_name, route.query.homework_name, id).then(() => {
    window.$message?.success($t('common.deleteSuccess'));
    getData();
  });
}
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <div class="top">
      <div>
        <h3>
          {{ homeworkDetail.name }}
          <span class="score">{{homeworkDetail.score_get}}/{{ homeworkDetail.sum_score }} score</span>
          <span class="remainTime">{{ remainTime }}</span>
        </h3>
        <p class="des">
          Start
          <span class="create_time">{{ formatDate(homeworkDetail.created_time) }}</span>
          End
          <span class="create_time">{{ formatDate(homeworkDetail.due_date) }}</span>
        </p>
        <span class="des">{{ homeworkDetail.description }}</span>
      </div>
      <TableHeaderOperation p="level2" v-model:columns="filteredColumns" :disabled-delete="checkedRowKeys.length === 0"
        :loading="loading" @add="handleAdd" @refresh="getData" />
    </div>
    <NCard :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="1210" :loading="loading" :row-key="item => item.id"
        class="sm:h-full" />
      <MenuOperateDrawer v-model:visible="drawerVisible" :homework_name="route.query.homework_name"
        :course_name="route.query.course_name" :operate-type="operateType" :row-data="editingData"
        @submitted="getData" />
      <caseDialog v-model:visible="caseDrawerVisible" :homework_name="route.query.homework_name"
        :course_name="route.query.course_name" :operate-type="operateType" :row-data="editingData"
        @submitted="getData" />
      <aiDialog v-model:visible="aiDrawerVisible" :homework_name="route.query.homework_name"
        :course_name="route.query.course_name" :operate-type="operateType" :row-data="editingData"
        @submitted="getData" />
    </NCard>
  </div>
</template>

<style lang="scss" scoped>
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
</style>
