import type { Dict } from '@/typings/dict';
import { request } from '../request';

export function getDicList(dictKey: keyof Dict) {
  return request<any>({
    url: `dicts/${dictKey}`,
    method: 'GET'
  });
}
