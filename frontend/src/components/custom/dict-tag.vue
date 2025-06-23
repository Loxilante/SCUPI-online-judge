<script setup lang="ts">
import { computed } from 'vue';
import { NTag } from 'naive-ui';
import type { Dict } from '@/typings/dict.d';
import { useDictStore } from '@/store/modules/dict';
const { dicts } = useDictStore();
interface Props {
  dictType: keyof Dict;
  code: number;
  hideTagDef?: boolean;
}
const props = defineProps<Props>();
const item = computed(() => {
  return dicts[props.dictType]?.find(data => data.value === props.code);
});
</script>

<template>
  <span>
    <NTag v-show="!hideTagDef" :type="item?.tag">{{ item?.label }}</NTag>
    <i v-show="hideTagDef" style="font-style: normal">{{ item?.label }}</i>
  </span>
</template>

<style scoped></style>
