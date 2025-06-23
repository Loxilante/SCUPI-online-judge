<script setup lang="tsx">
/* eslint-disable */
import { ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { getHomeworkByStudenetIdRecords } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
import { NButton } from 'naive-ui';
const appStore = useAppStore();
const route = useRoute();
const { columns, filteredColumns, data, loading, getData } = useTable<
  any,
  typeof getHomeworkByStudenetIdRecords,
  'index' | 'operate'
>({
  apiFn: getHomeworkByStudenetIdRecords,
  transformer: res => {
    const list: any = res.data || [];
    return {
      data: list,
      pageNum: 1,
      pageSize: 10,
      total: list.length
    };
  },
  apiParams: { course_name: route.query.course_name, homework_name: route.query.homework_name,username:route.query.username },
  columns: () => [
    {
      key: 'title',
      title: 'Title',
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
        <div class="flex-center justify-end gap-8px">
          <RouterLink to={`/home/submission-detail?course_name=${route.query.course_name}&homework_name=${route.query.homework_name}&problemId=${row.problem_id}&username=${route.query.username}`}>
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

watch((route as any).query.course_name, () => {
  getData();
});
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard :title="`Student Detail ${route.query.first_name}`" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
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
