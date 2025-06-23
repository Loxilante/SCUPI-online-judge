import type { Ref } from 'vue';
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { SetupStoreId } from '@/enum';
import type { Dict } from '@/typings/dict';
import { getDicList } from '@/service/api/dict';
export const useDictStore = defineStore(SetupStoreId.Dict, () => {
  const dicts: Ref<{
    [name in keyof Dict]?: {
      value: number;
      label: string;
      tag: 'default' | 'error' | 'success' | 'warning' | 'primary' | 'info';
    }[];
  }> = ref({});
  const init = (_dictKeys: (keyof Dict)[]) => {
    Object.values(_dictKeys).forEach((dictKey: keyof Dict) => {
      getDicList(dictKey).then(res => {
        if (res.error === null) {
          dicts.value[dictKey] = [...res.data];
        }
      });
    });
  };
  return {
    dicts,
    init
  };
});
