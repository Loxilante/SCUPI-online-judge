<script setup lang="tsx">
/* eslint-disable */
import { ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { useBoolean } from '@sa/hooks';
import { getQuestionRecords } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from '@/views/home/submission-detail/modules/operate.vue';
import { NButton } from 'naive-ui';
const appStore = useAppStore();
const { bool: drawerVisible, setTrue: openDrawer } = useBoolean();
const route = useRoute();
const operateType = ref<OperateType>('add');

function handleEdit(row:any) {
  operateType.value = 'edit';
  editingData.value = row;
  openDrawer();
}
const { columns, filteredColumns, data, loading, getData } = useTable<
  any,
  typeof getQuestionRecords,
  'index' | 'operate'
>({
  apiFn: getQuestionRecords,
  transformer: res => {
    const list: any = res.data || [];
    return {
      data: list,
      pageNum: 1,
      pageSize: 10,
      total: list.length
    };
  },
  apiParams: { course_name: route.query.course_name, homework_name: route.query.homework_name, id: route.query.problemId },
  columns: () => [
    {
      key: 'first_name',
      title: 'Name',
      width: 100,
      align: 'center'
    },
    {
      key: 'username',
      title: 'ID',
      width: 150,
      align: 'center'
    },
    {
      key: 'score',
      title: 'Score',
      width: 60,
      align: 'center'
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      render: (row: any) => (
        <div class="flex-center justify-end gap-8px">
          <NButton onClick={()=>{
            handleEdit(row)
          }} type="primary" ghost size="small">
            {'Comment'}
          </NButton>
          <RouterLink to={`/home/submission-detail?course_name=${route.query.course_name}&homework_name=${route.query.homework_name}&problemId=${route.query.problemId}&username=${row.username}`}>
            <NButton type="primary" ghost size="small">
              {'Submission Detail'}
            </NButton>
          </RouterLink>
        </div>
      )
    }
  ]
});
const checkedRowKeys = ref<string[]>([]);

/** the editing row data */
const editingData = ref<any>(null);

watch((route as any).query.course_name, () => {
  getData();
});
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard title="Class Submissions" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <template #header-extra>
        <TableHeaderOperation v-model:columns="filteredColumns" :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading" @refresh="getData" />
      </template>
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="900" :loading="loading" :row-key="item => item.id"
        class="sm:h-full" />
      <MenuOperateDrawer v-model:visible="drawerVisible" :course_name="route.query.course_name"
        :operate-type="operateType" :row-data="editingData" @submitted="getData" />
    </NCard>
  </div>
</template>

<style scoped></style>
