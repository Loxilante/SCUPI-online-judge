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

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
    default: false
})

// 用于存储AI设置表单的数据
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

  // 将标识信息和表单数据合并到一个对象中
  const dataToSave = {
    course_name: props.course_name,
    homework_name: props.homework_name,
    id: props.rowData.id,
    ...aiFormData.value // 将5个AI字段合并进来
  };

  // 调用更新API，只传递一个data对象
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

// 关闭AI设置抽屉
const closeDrawer = () => {
  emit('update:visible', false);
};

// 当可见性变化时填充数据
const updateFormData = () => {
  if (props.rowData) {
    aiFormData.value.sample = props.rowData.sample || '';
    aiFormData.value.sample_explanation = props.rowData.sample_explanation || '';
    aiFormData.value.style_criteria = props.rowData.style_criteria || '';
    aiFormData.value.implement_criteria = props.rowData.implement_criteria || '';
    aiFormData.value.additional = props.rowData.additional || '';
  }
};

// 监听 visible 状态变化，更新表单数据
watch(visible, () => {
    if (visible.value) {
        if (props.rowData && props.rowData.id) {
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
            });
        }
    }
});
</script>

<template>
  <NDrawer v-model:show="visible" title="AI Settings" width="50%">
    <NDrawerContent :native-scrollbar="false" :show-footer="true" title="AI Settings" >
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
</style>
