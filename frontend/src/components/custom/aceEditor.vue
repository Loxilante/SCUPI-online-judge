<script lang="tsx" setup>
/* eslint-disable */
import { nextTick, onMounted, ref, watch, defineExpose } from 'vue';
import ace from 'ace-builds';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/mode-markdown';
import 'ace-builds/src-noconflict/ext-searchbox';
import 'ace-builds/src-noconflict/ext-language_tools';
import 'ace-builds/src-noconflict/snippets/javascript';
import 'ace-builds/src-noconflict/snippets/java';
import 'ace-builds/src-noconflict/snippets/c_cpp';
import 'ace-builds/src-noconflict/snippets/markdown';
const $emit = defineEmits(['update:value', 'change']);
const props = defineProps(['value', 'width', 'height', 'idKey', 'mode', 'disabled', 'onChange', 'editorType', 'disabledLang', 'justForCode']);
const language = ref(props.mode ? props.mode : 'c_cpp');
const editorRef: any = ref(null)
const createOptions = () => {
  let options: any[] = []
  if (props.justForCode) {
    options = [
      {
        label: 'Java',
        value: 'java'
      },
      {
        label: 'C/C++',
        value: 'c_cpp'
      }
    ]
  } else {
    options = [
      {
        label: 'markdown',
        value: 'markdown'
      }
    ]
  }
  return options
}
const options = ref(createOptions());
onMounted(() => {
  init(language.value);
});

watch(language, () => {
  nextTick(() => {
    props.onChange && props.onChange(language.value)
    init(language.value);
  });
});
watch(props.mode, () => {
  nextTick(() => {
    init(props.mode);
  });
});
const mapping: any = {
  "markdown": {
    id: 'editorM',
    mode: 'ace/mode/markdown'
  },
  "c_cpp": {
    id: 'editorC',
    mode: 'ace/mode/c_cpp'
  },
  "java": {
    id: 'editorJava',
    mode: 'ace/mode/java'
  },
}
const init = (lang: string, fromOuter?: string) => {
  let str = ""
  let curValue = props.value || fromOuter
  if (props.editorType != 'text') {
    if (curValue instanceof Array) {
      curValue.forEach((item: any) => {
        str += item.question;
      });
    }

  } else {
    str = curValue
  }
  initCommon(lang, str)
}
defineExpose({
  update(data: string) {
    init(props.mode, data)
  }
})
function initCommon(lang: string, str: string) {
  // https://github.com/ajaxorg/ace/wiki/Configuring-Ace
  const editor = editorRef.value = ace.edit(
    `${mapping[lang].id}${props.idKey ? props.idKey : ''}`,
    {
      mode: mapping[lang].mode
    }
  );
  if (props.disabled) {
    editor.setReadOnly(true);
  }
  editor.setValue(str);
  editor.on('change', () => {
    $emit('update:value', props.editorType != 'text' ? [
      {
        question: editor.getValue(),
        type: language.value
      }
    ] : editor.getValue());
  });
  editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true
  });
}
const changeLanguage = () => {
  $emit('change', language.value);
}
</script>

<template>
  <div
    :style="`width: ${props.width ? props.width : '600px'};margin-bottom:8px; height: ${props.height ? props.height : '400px'};position:relative;`">
    <NSelect :disabled="props.disabled || props.disabledLang" @change="changeLanguage" v-model:value="language"
      class="chooseLanguage" :options="options" placeholder="请选择语言" size="small">
    </NSelect>
    <div v-if="language == 'java'" :id="'editorJava' + (props.idKey ? props.idKey : '')"
      :style="`width: ${props.width ? props.width : '600px'}; height: ${props.height ? props.height : '400px'}`"></div>
    <div v-if="language == 'c_cpp'" :id="'editorC' + (props.idKey ? props.idKey : '')"
      :style="`width: ${props.width ? props.width : '600px'}; height: ${props.height ? props.height : '400px'}`"></div>
    <div v-if="language == 'markdown'" :id="'editorM' + (props.idKey ? props.idKey : '')"
      :style="`width: ${props.width ? props.width : '600px'}; height: ${props.height ? props.height : '400px'}`"></div>
  </div>
</template>

<style lang="scss" scoped>
.chooseLanguage {
  width: 150px;
  margin-bottom: 10px;
}

.popDisabled {
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 200;
}
</style>
