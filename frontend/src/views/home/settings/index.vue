<script setup lang="tsx">
import { ref, reactive, onMounted, computed, h } from 'vue';
import { NCard, NForm, NFormItem, NInput, NButton, NSpace, useMessage, NTabs, NTabPane, NDataTable, NPopconfirm, NDrawer, NDrawerContent, NFlex, NSelect } from 'naive-ui';
import type { DataTableColumns } from 'naive-ui';
import { fetchGetUserInfo, changeUserPwd } from '@/service/api/auth';
import { useAuthStore } from '@/store/modules/auth';
import { getTokens, addToken, updateToken, deleteToken } from '@/service/api';

type Token = {
    id: number;
    platform: string;
    name: string;
    token_display: string;
    created_time: string;
};

const platformOptions = [
  'ChatGPT', 'DeepSeek', 'Gemini', 'Claude', 'Grok', 'Doubao', 'KIMI', 'Qwen', 'Hunyuan'
].map(p => ({ label: p, value: p }))

const message = useMessage();
const authStore = useAuthStore();

const isAdminOrTeacher = computed(() => {
    const roles = authStore.userInfo.roles || [];
    return roles.includes('teacher') || roles.includes('administrator');
});

const displayInfo = ref({
    username: '',
    first_name: ''
});

const passwordForm = reactive({
    old_password: '',
    new_password: '',
    confirm_password: ''
});

async function handlePasswordChange() {
    if (!passwordForm.old_password || !passwordForm.new_password) {
        message.error('Old password and new password cannot be empty');
        return;
    }
    if (passwordForm.new_password !== passwordForm.confirm_password) {
        message.error('The new passwords entered do not match');
        return;
    }

    const { error } = await changeUserPwd({
        username: authStore.userInfo.username,
        old_password: passwordForm.old_password,
        new_password: passwordForm.new_password
    });

    if (!error) {
        message.success('Password successfully changed.')
        passwordForm.old_password = '';
        passwordForm.new_password = '';
        passwordForm.confirm_password = '';
    }
    else {
        message.error('Failed to change password. Please check if the old password is correct.')
    }
}

const tokenList = ref<Token[]>([]);
const tokenTableLoading = ref(false);
const addTokenForm = reactive({ platform: '', name: '', token: '' });

async function fetchTokenList() {
    if (!isAdminOrTeacher.value) return;
    tokenTableLoading.value = true;
    const { data, error } = await getTokens();
    if (!error && data) {
        tokenList.value = data;
    }
    tokenTableLoading.value = false;
}

async function handleAddNewToken() {
    if (!addTokenForm.platform || !addTokenForm.name || !addTokenForm.token) {
        message.error('Name, token, and platform should not be empty.');
        return;
    }

    const { error } = await addToken({ ...addTokenForm });
    if (!error) {
        message.success('New token added successfully.');
        addTokenForm.platform = '';
        addTokenForm.name = '';
        addTokenForm.token = '';
        fetchTokenList();
    }
    else {
        message.error('Failed to add new token.');
    }
}

const showEditDrawer = ref(false);
const editingToken = ref<Token | null>(null);
const editTokenForm = reactive({
    password: '',
    token: '',
    name: '',
    platform: ''
});

function openEditDrawer(token: Token) {
  editingToken.value = token;
  editTokenForm.password = '';
  editTokenForm.token = '';
  editTokenForm.name = token.name;
  editTokenForm.platform = token.platform;
  showEditDrawer.value = true;
}

async function handleUpdateToken() {
  if (!editingToken.value || !editTokenForm.password) {
    message.error('Password should not be empty.');
    return;
  }

  const payload: { id: number; password: string; name?: string; platform?: string; token?: string } = {
    id: editingToken.value.id,
    password: editTokenForm.password,
    name: editTokenForm.name,
    platform: editTokenForm.platform
  }

  if (editTokenForm.token && editTokenForm.token.trim() !== '') {
    payload.token = editTokenForm.token;
  }

  const { error } = await updateToken(payload);

  if (!error) {
    message.success('Token updated successfully.');
    showEditDrawer.value = false;
    fetchTokenList();
  }
  else {
    message.error('Failed to update. Please check the password.');
  }
}

async function handleDeleteToken() {
  if (!editingToken.value || !editTokenForm.password) {
    message.error('You need to enter your password to delete the token.');
    return;
  }
  const { error } = await deleteToken({
    id: editingToken.value.id,
    password: editTokenForm.password
  });

  if (!error) {
    message.success('Token deleted successfully.');
    showEditDrawer.value = false;
    fetchTokenList();
  } else {
    message.error('Failed to delete. Please check the password.');
  }
}

const createTokenTableColumns = (): DataTableColumns<Token> => [
  { title: 'Name', key: 'name' },
  { title: 'Token', key: 'token_display' },
  { title: 'Platform', key: 'platform' },
  { title: 'Created Time', key: 'created_time' },
  {
    title: 'Edit',
    key: 'actions',
    render(row) {
      return h(
        NButton,
        { size: 'small', type: 'primary', ghost: true, onClick: () => openEditDrawer(row) },
        { default: () => 'Edit' }
      );
    }
  }
];
const tokenTableColumns = createTokenTableColumns();

onMounted(() => {
  if (authStore.userInfo) {
    displayInfo.value.username = authStore.userInfo.username;
    displayInfo.value.first_name = authStore.userInfo.first_name;
  }
  if (isAdminOrTeacher.value) {
    fetchTokenList();
  }
});

</script>

<template>
  <div class="p-4">
    <NCard title="Account Information" class="mb-4">
      <NForm label-placement="left" label-width="120" class="w-full md:w-1/2">
        <NFormItem label="Student ID">
          <NInput :value="displayInfo.username" readonly />
        </NFormItem>
        <NFormItem label="Username">
          <NInput :value="displayInfo.first_name" readonly />
        </NFormItem>
      </NForm>
    </NCard>
    <NCard title="Settings">
      <NTabs type="line" animated>
        <NTabPane name="password" tab="Change Password">
          <NForm 
            :model="passwordForm"
            label-placement="left" 
            label-width="180" 
            class="w-full md:w-1/2 mt-4"
          >
            <NFormItem label="Current Password">
              <NInput 
                v-model:value="passwordForm.old_password"
                type="password"
                show-password-on="mousedown"
                placeholder="Enter current password" 
              />
            </NFormItem>
            <NFormItem label="New Password">
              <NInput 
                v-model:value="passwordForm.new_password"
                type="password"
                show-password-on="mousedown"
                placeholder="Enter new password"
              />
            </NFormItem>
            <NFormItem label="Confirm New Password">
              <NInput 
                v-model:value="passwordForm.confirm_password"
                type="password"
                show-password-on="mousedown"
                placeholder="Confirm new password" 
              />
            </NFormItem>
            <NFormItem :label-width="0">
              <NSpace>
                <NButton type="primary" @click="handlePasswordChange">
                  Confirm Change
                </NButton>
              </NSpace>
            </NFormItem>
          </NForm>
        </NTabPane>

        <NTabPane v-if="isAdminOrTeacher" name="tokens" tab="API Token Management">
          <NSpace vertical class="mt-4">
            <NDataTable
              :columns="tokenTableColumns"
              :data="tokenList"
              :loading="tokenTableLoading"
              :bordered="false"
              :single-line="false"
            />
            <NForm :model="addTokenForm" :show-label="false" layout="inline" class="mt-4 p-4 border rounded">
              <NFormItem path="name" class="flex-1">
                <NInput v-model:value="addTokenForm.name" placeholder="Custom Name (e.g., My Backup Key)" />
              </NFormItem>
              <NFormItem path="platform" class="flex-1">
                <NSelect v-model:value="addTokenForm.platform" :options="platformOptions" placeholder="Please select a platform" />
              </NFormItem>
              <NFormItem path="token" class="flex-2">
                <NInput v-model:value="addTokenForm.token" type="password" show-password-on="mousedown" placeholder="Paste your API Key here" />
              </NFormItem>
              <NFormItem>
                <NButton type="primary" @click="handleAddNewToken">Add New Token</NButton>
              </NFormItem>
            </NForm>
          </NSpace>
        </NTabPane>
      </NTabs>
    </NCard>

    <NDrawer v-model:show="showEditDrawer" :width="'50%'" placement="right">
      <NDrawerContent :title="`Edit Token: ${editingToken?.name}`" closable>
        <NForm :model="editTokenForm" label-placement="top">
          <NFormItem label="Confirm Your Login Password (Required)">
            <NInput 
              v-model:value="editTokenForm.password" 
              type="password" 
              show-password-on="mousedown"
              placeholder="Enter your login password for security verification" 
            />
          </NFormItem>
          
          <NFormItem label="Custom Name">
            <NInput v-model:value="editTokenForm.name" placeholder="Give your token an easy-to-recognize name" />
          </NFormItem>
          <NFormItem label="Platform">
            <NSelect v-model:value="editTokenForm.platform" :options="platformOptions" />
          </NFormItem>
          <NFormItem label="New Token Value (Enter here if you need to update)">
            <NInput 
              v-model:value="editTokenForm.token" 
              type="textarea" 
              :autosize="{minRows: 5, maxRows: 10}" 
              placeholder="Paste the new API Key here" 
            />
          </NFormItem>
        </NForm>
        
        <template #footer>
          <NFlex justify="space-between">
            <NPopconfirm @positive-click="handleDeleteToken">
              <template #trigger>
                <NButton type="error">Delete This Token</NButton>
              </template>
              After entering your password in the "Confirm Your Login Password" field, clicking this button will permanently delete this token. Are you sure?
            </NPopconfirm>
            
            <NButton type="primary" @click="handleUpdateToken">Submit Update</NButton>
          </NFlex>
        </template>
      </NDrawerContent>
    </NDrawer>
  </div>
</template>

<style scoped>
.p-4 { padding: 16px; }
.mb-4 { margin-bottom: 16px; }
.mt-4 { margin-top: 16px; }
.border { border: 1px solid #efeff5; }
.rounded { border-radius: 4px; }
.flex-1 { flex: 1 1 0%; }
.flex-2 { flex: 2 1 0%; }
.w-full { width: 100%; }
.md\:w-1\/2 { width: 50%; }
.justify-between { justify-content: space-between; }
</style>