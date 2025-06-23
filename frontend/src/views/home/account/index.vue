<script setup lang="tsx">
/* eslint-disable */
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { NButton, NPopconfirm } from 'naive-ui';
import { useBoolean } from '@sa/hooks';
import { getAllUsers } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable } from '@/hooks/common/table';
import { $t } from '@/locales';
import { removeUser } from '@/service/api/course';
//@ts-ignore
import MenuOperateDrawer, { type OperateType } from './modules/operate.vue';
const appStore = useAppStore();
const { bool: drawerVisible, setTrue: openDrawer } = useBoolean();
const route = useRoute();
const { columns, filteredColumns, data, loading, getData } = useTable<
  any,
  typeof getAllUsers,
  'index' | 'operate'
>({
  apiFn: getAllUsers,
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
      key: 'email',
      title: 'Email',
      align: 'center'
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      render: row => (
        <div class="flex-center justify-end gap-8px">
          <permission>
            <NButton type="primary" ghost size="small" onClick={() => handleEdit(row.username)}>
              {'Edit Password'}
            </NButton>
          </permission>

          <NPopconfirm onPositiveClick={() => handleDelete(row.username)}>
            {{
              default: () => $t('common.confirmDelete'),
              trigger: () => (
                <NButton type="error" ghost size="small">
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
  editingData.value = data.value.find((item: any) => item.username === name) || null;
  openDrawer();
}

watch((route as any).query.course_name, () => {
  getData();
});

async function handleDelete(username: string) {
  removeUser(username).then(() => {
    window.$message?.success($t('common.deleteSuccess'));
    getData();
  });
}
</script>

<template>
  <div class="flex-vertical-stretch gap-16px overflow-hidden <sm:overflow-auto">
    <NCard title="Account List" :bordered="false" size="small" class="card-wrapper sm:flex-1-hidden">
      <template #header-extra>
        <TableHeaderOperation v-model:columns="filteredColumns" :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading" @add="handleAdd" @refresh="getData" />
      </template>
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="640" :loading="loading" :row-key="item => item.id"
        class="sm:h-full" />
      <MenuOperateDrawer v-model:visible="drawerVisible" :course_name="route.query.course_name"
        :operate-type="operateType" :row-data="editingData" @submitted="getData" />
    </NCard>
  </div>
</template>

<style scoped></style>
