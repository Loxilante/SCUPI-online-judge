<script setup lang="tsx">
/* eslint-disable */
import { ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { NButton, NPopconfirm } from 'naive-ui';
import { useBoolean } from '@sa/hooks';
import moment from 'moment';
import { getHomeworkByCourse } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
import { removeHomeworkToCourse } from '@/service/api/course';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from './modules/operate.vue';
const appStore = useAppStore();
const { bool: drawerVisible, setTrue: openDrawer } = useBoolean();
const route = useRoute();
const { columns, filteredColumns, data, loading, getData } = useTable<
  any,
  typeof getHomeworkByCourse,
  'index' | 'operate'
>({
  apiFn: getHomeworkByCourse,
  transformer: res => {
    const list: any = res.data || [];
    return {
      data: list,
      pageNum: 1,
      pageSize: 10,
      total: list.length
    };
  },
  apiParams: { coursename: route.query.course_name },
  columns: () => [
    {
      key: 'name',
      title: 'Homework Name',
      width:150,
      render: row => {
        return (
          <RouterLink to={`/home/problem-list?course_name=${route.query.course_name}&homework_name=${row.name}`}>
            {row.name}
          </RouterLink>
        );
      },
      align: 'center'
    },
    {
      key: 'created_time',
      title: 'Created Time',
      width:100,
      render: row => moment(row.created_time).format('YYYY-MM-DD'),
      align: 'center'
    },
    {
      key: 'due_date',
      title: 'Due Date',
      width:100,
      render: row => moment(row.due_date).format('YYYY-MM-DD'),
      align: 'center'
    },
    {
      key: 'score',
      title: 'Score',
      align: 'center',
      width:50,
      render:(row:any)=>{
        return `${row.score_get}/${row.sum_score}`
      }
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      p: 'level2',
      render: row => (
        <div class="flex-center justify-end gap-8px">
          <RouterLink v-p="level2" to={`/home/homework-records?course_name=${route.query.course_name}&homework_name=${row.name}`}>
            <NButton type="primary" ghost size="small">
              {'Course Records'}
            </NButton>
          </RouterLink>
          <NButton v-p="level2" type="primary" ghost size="small" onClick={() => handleEdit(row.name)}>
            {$t('common.edit')}
          </NButton>
          <NPopconfirm onPositiveClick={() => handleDelete(row.name)}>
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

function handleAdd() {
  operateType.value = 'add';
  openDrawer();
}
const checkedRowKeys = ref<string[]>([]);

/** the editing row data */
const editingData = ref<any>(null);

function handleEdit(name: string) {
  operateType.value = 'edit';
  editingData.value = data.value.find((item: any) => item.name === name) || null;
  editingData.value.created_time = Number(new Date(editingData.value.created_time));
  editingData.value.due_date = Number(new Date(editingData.value.due_date));
  openDrawer();
}

watch((route as any).query.course_name, () => {
  getData();
});

async function handleDelete(name: string) {
  removeHomeworkToCourse((route as any).query.course_name, name).then(() => {
    window.$message?.success($t('common.deleteSuccess'));
    getData();
  });
}
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard title="Homework List" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <template #header-extra>
        <TableHeaderOperation p="level2" v-model:columns="filteredColumns" :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading" @add="handleAdd" @refresh="getData" />
      </template>
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="1240" :loading="loading" :row-key="item => item.id"
        class="sm:h-full" />
      <MenuOperateDrawer v-model:visible="drawerVisible" :course_name="route.query.course_name"
        :operate-type="operateType" :row-data="editingData" @submitted="getData" />
    </NCard>
  </div>
</template>

<style scoped></style>
