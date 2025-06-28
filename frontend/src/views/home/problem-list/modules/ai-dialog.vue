<script setup lang="ts">
/* eslint-disable */
import { defineProps, defineEmits, ref, watch } from 'vue';
import { NDrawer, NDrawerContent, NForm, NFormItem, NInput, NButton, NSpace } from 'naive-ui';
import { getAISettings, updateAISettings, deleteAISettings } from '@/service/api/ai';

interface Props {
  rowData?: any;
  course_name?: any;
  title?: any;
  homework_name?: any;
}

interface Emits {
  (e: 'submitted'): void;
  (e: 'update:visible', val: boolean): void;
}

const isLoading = ref(false);
const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
    default: false
})

// store form data for AI settings
const aiFormData = ref({
  sample: '',
  sample_explanation: '',
  style_criteria: '',
  implement_criteria: '',
  additional: ''
});

const saveAISettings = () => {
  if (!props.rowData || !props.rowData.id) {
    window.$message?.error('Error: No problem ID.');
    return;
  }

  // merge identity information with form data into one object
  const dataToSave = {
    course_name: props.course_name,
    homework_name: props.homework_name,
    id: props.rowData.id,
    ...aiFormData.value // merge 5 AI fields in
  };

  // call update API with one object
  updateAISettings(dataToSave).then(({ error }) => {
    if (!error) {
      window.$message?.success('Update Success!');
      emit('submitted');
      emit('update:visible', false);
    } else {
      window.$message?.error('Unable to update, please try again.');
    }
  });
};

// close AI settings drawer
const closeDrawer = () => {
  emit('update:visible', false);
};

// fill data when visibility changes
const updateFormData = () => {
  if (props.rowData) {
    aiFormData.value.sample = props.rowData.sample || '';
    aiFormData.value.sample_explanation = props.rowData.sample_explanation || '';
    aiFormData.value.style_criteria = props.rowData.style_criteria || '';
    aiFormData.value.implement_criteria = props.rowData.implement_criteria || '';
    aiFormData.value.additional = props.rowData.additional || '';
  }
};

// watch for changes in 'visible'
watch(visible, () => {
  if (visible.value) {
    if (props.rowData && props.rowData.id) {
      isLoading.value = 
      getAISettings({
        course_name: props.course_name,
        homework_name: props.homework_name,
        id: props.rowData.id
      }).then(({ data, error }) => {
        if (!error && data) {
          aiFormData.value.sample = data.sample || '';
          aiFormData.value.sample_explanation = data.sample_explanation || '';
          aiFormData.value.style_criteria = data.style_criteria || '';
          aiFormData.value.implement_criteria = data.implement_criteria || '';
          aiFormData.value.additional = data.additional || '';
        }
      }).finally(() => {
        isLoading.value = false;
      });
    }
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" title="AI Settings" width="50%">
    <NDrawerContent :native-scrollbar="false" :show-footer="true" title="AI Settings" :content-style="{ position: 'relative' }">

      <template v-if="!isLoading">
        <NForm :model="aiFormData" label-placement="top" label-width="150px">
          <NFormItem label="Sample" path="sample">
            <NInput v-model:value="aiFormData.sample" placeholder="Please Enter Sample" type = "textarea" :autosize="{ minRows: 1, maxRows: 7 }"/>
          </NFormItem>
          <NFormItem label="Sample Explanation" path="sample_explanation">
            <NInput v-model:value="aiFormData.sample_explanation" placeholder="Please Enter Sample Explanation" type = "textarea" :autosize="{ minRows: 1, maxRows: 7 }"/>
          </NFormItem>
          <NFormItem label="Style Criteria" path="style_criteria">
            <NInput v-model:value="aiFormData.style_criteria" placeholder="Please Enter Style Criteria" type = "textarea" :autosize="{ minRows: 1, maxRows: 7 }"/>
          </NFormItem>
          <NFormItem label="Implement Criteria" path="implement_criteria">
            <NInput v-model:value="aiFormData.implement_criteria" placeholder="Please Enter Implement Criteria" type = "textarea" :autosize="{ minRows: 1, maxRows: 7 }"/>
          </NFormItem>
          <NFormItem label="Additional" path="additional">
            <NInput v-model:value="aiFormData.additional" placeholder="Please Enter Additional Implementations" type = "textarea" :autosize="{ minRows: 1, maxRows: 7 }"/>
          </NFormItem>
        </NForm>
      </template>
      <template v-else>
        <div class="loading-container">
          <n-spin size="large" />
        </div>
      </template>

      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">Cancel</NButton>
          <NButton type="primary" @click="saveAISettings">Save</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped>
.n-drawer {
  padding: 20px;
}

.n-input {
  width: 100%;
}

.loading-container, .empty-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.loading-container p {
  margin-top: 20px;
  color: #999;
}
</style>
