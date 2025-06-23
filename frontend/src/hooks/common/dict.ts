import type { Ref } from 'vue';
import { ref } from 'vue';
import { getDicList } from '@/service/api/dict';
import type { Dict } from '@/typings/dict';

const useDict = (_dictKeys: (keyof Dict)[]) => {
  const dicts: Ref<{
    [name in keyof Dict]?: {
      name: string;
      code: string;
    }[];
  }> = ref({});
  return {
    dicts,
    init: () => {
      Object.values(_dictKeys).forEach((dictKey: keyof Dict) => {
        getDicList(dictKey).then(res => {
          if (res.error === null) {
            dicts.value[dictKey] = res.data;
          }
        });
      });
    }
  };
};

export default useDict;
