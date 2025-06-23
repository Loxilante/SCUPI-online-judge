<script setup lang="tsx">
/* eslint-disable */
import { ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { getHomeworkRecords } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from './modules/operate.vue';
import { NButton } from 'naive-ui';
const appStore = useAppStore();
const route = useRoute();
const { columns, filteredColumns, data, loading, getData } = useTable<
  any,
  typeof getHomeworkRecords,
  'index' | 'operate'
>({
  apiFn: getHomeworkRecords,
  transformer: res => {
    const list: any = res.data || [];
    return {
      data: list,
      pageNum: 1,
      pageSize: 10,
      total: list.length
    };
  },
  apiParams: { course_name: route.query.course_name, homework_name: route.query.homework_name },
  columns: () => [
    {
      key: 'first_name',
      title: 'Name',
      align: 'center'
    },
    {
      key: 'username',
      title: 'ID',
      align: 'center'
    },
    {
      key: 'score',
      title: 'Score',
      align: 'center'
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      render: (row: any) => (
        <div class="flex-center">
          <RouterLink  to={`/home/homework-records-detail?course_name=${route.query.course_name}&homework_name=${route.query.homework_name}&username=${row.username}&first_name=${row.first_name}`}>
            <NButton type="primary" ghost size="small">
              {'Detail'}
            </NButton>
          </RouterLink>
        </div>
      )
    }
  ]
});
const checkedRowKeys = ref<string[]>([]);

watch((route as any).query.course_name, () => {
  getData();
});
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard title="Course Records" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="filteredColumns"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          :disabledAdd="true"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="640"
        :loading="loading"
        :row-key="item => item.id"
        class="sm:h-full"
      />
    </NCard>
  </div>
</template>

<style scoped></style>
