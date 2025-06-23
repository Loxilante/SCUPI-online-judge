<script setup lang="ts">
import type { Dict } from '@/typings/dict.d';
import { useDictStore } from '@/store/modules/dict';
const { dicts } = useDictStore();
interface Props {
  // eslint-disable-next-line vue/no-unused-properties
  dictType: keyof Dict;
}
const props = defineProps<Props>();
const model = defineModel<any>();
</script>

<template>
  <n-select
    v-model="model"
    :options="[{ label: '全部', value: '', tag: '' }, ...(dicts[props.dictType] || [])]"
  ></n-select>
</template>

<style scoped></style>
