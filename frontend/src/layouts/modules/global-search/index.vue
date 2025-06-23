<script setup lang="ts">
defineOptions({
  name: 'GlobalLogo'
});

interface Props {
  /** Whether to show the title */
  showTitle?: boolean;
}

withDefaults(defineProps<Props>(), {
  showTitle: true
});
</script>

<template>
  <div class="flex-center w-full nowrap-hidden">
    <NInput v-if="showTitle" class="search" placeholder="Search" />
  </div>
</template>

<style scoped>
.search {
  margin: 20px;
  margin-bottom: 0;
}
</style>
