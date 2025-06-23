<script setup lang="tsx">
/* eslint-disable */
import { ref } from 'vue';
import { NButton, NPopconfirm } from 'naive-ui';
import { useBoolean } from '@sa/hooks';
import { RouterLink } from 'vue-router';
import { getCourseList } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
import { removeCourse } from '@/service/api/course';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from './modules/operate.vue';
const appStore = useAppStore();
const { bool: drawerVisible, setTrue: openDrawer } = useBoolean();

const { columns, filteredColumns, data, loading, getData } = useTable<any, typeof getCourseList, 'index' | 'operate'>({
  apiFn: getCourseList,
  transformer: res => {
    const list: any = res.data || [];
    return {
      data: list,
      pageNum: 1,
      pageSize: 10,
      total: list.length
    };
  },
  columns: () => [
    // {
    //   type: 'selection',
    //   align: 'center',
    //   width: 48
    // },
    {
      key: 'course_name',
      title: 'Course Name',
      align: 'center',
      render: row => {
        return (
          <RouterLink to={`/home/homework?course_name=${encodeURIComponent(row.course_name)}`}>
            {row.course_name}
          </RouterLink>
        );
      }
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      p: "level1",
      render: row => (
        <div class="flex-center justify-end gap-8px">
          <NButton v-p="level1" type="primary" ghost size="small" onClick={() => handleEdit(row.course_name)}>
            {$t('common.edit')}
          </NButton>
          <NPopconfirm onPositiveClick={() => handleDelete(row.course_name)}>
            {{
              default: () => $t('common.confirmDelete'),
              trigger: () => (
                <NButton v-p="level1" type="error" ghost size="small">
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

function handleEdit(course_name: string) {
  operateType.value = 'edit';
  editingData.value = data.value.find((item: any) => item.course_name === course_name) || null;
  openDrawer();
}

async function handleDelete(course_name: string) {
  removeCourse(course_name).then(() => {
    window.$message?.success($t('common.deleteSuccess'));
    getData();
  });
}
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard title="Course List" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <template #header-extra>
        <TableHeaderOperation
          p="level1"
          v-model:columns="filteredColumns"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          @add="handleAdd"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns as any"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="640"
        :loading="loading"
        :row-key="(item: any) => item.id"
        class="sm:h-full"
      />
      <MenuOperateDrawer
        v-model:visible="drawerVisible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getData"
      />
    </NCard>
  </div>
</template>

<style scoped></style>
