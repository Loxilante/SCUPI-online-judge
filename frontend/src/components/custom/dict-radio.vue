<script setup lang="ts">
import type { Dict } from '@/typings/dict.d';
import { useDictStore } from '@/store/modules/dict';
const { dicts } = useDictStore();
interface Props {
  dictType: keyof Dict;
}
const props = defineProps<Props>();
const model = defineModel<any>();
</script>

<template>
  <n-radio-group v-model:value="model">
    <n-radio v-for="(item, index) in dicts[props.dictType]" :key="index" :value="item.value" :name="item.label">
      {{ item.label }}
    </n-radio>
  </n-radio-group>
</template>

<style scoped></style>
