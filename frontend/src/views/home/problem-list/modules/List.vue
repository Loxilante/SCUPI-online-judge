<script lang="ts" setup>
import { defineEmits, defineProps, onMounted, ref, watch } from 'vue';
const $emit = defineEmits(['update:value']);
const props = defineProps(['value']);
const defaultItem = {
  question: '',
  answer: ''
};
const data = ref([{ ...defaultItem }]);
onMounted(() => {
  data.value = props.value.length > 0 ? props.value : [{ ...defaultItem }];
});
const handleAdd = () => {
  data.value.push({ ...defaultItem });
  $emit('update:value', data.value);
};
const changeInput = () => {
  $emit('update:value', data.value);
};
const handleRemove = (index: number) => {
  data.value.splice(index, 1);
  $emit('update:value', data.value);
};
watch(
  () => props.value,
  () => {
    data.value = props.value.length > 0 ? props.value : [{ ...defaultItem }];
  }
);
</script>

<template>
  <div class="list">
    <div v-for="(item, index) in data" :key="index" class="item">
      <NInput
        v-model:value="item.question"
        class="question"
        type="textarea"
        placeholder="Please Input Question"
        @input="changeInput"
      />
      <NInput
        v-model:value="item.answer"
        class="answer"
        type="textarea"
        placeholder="Please Input Answer"
        @input="changeInput"
      />
      <div class="buttonGroup">
        <span @click="handleAdd">
          <SvgIcon class="icon" icon="gala:add" />
        </span>
        <span v-if="data.length > 1" @click="handleRemove(index)">
          <SvgIcon class="icon" icon="simple-line-icons:minus" />
        </span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
:deep(.icon) {
  font-size: 22px;
  color: #999;
  cursor: pointer;
  margin-left: 10px;
}

.item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;

  &:last-child {
    margin-bottom: 0;
  }
}

.question {
  width: 300px;
}

.answer {
  width: 200px;
  margin-left: 10px;
}

.buttonGroup {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 60px;
}
</style>
