<template>
  <div
    v-if="visible"
    :style="{
      position: 'absolute',
      left: `${left}px`,
      top: `${top}px`,
      zIndex: 1000,
    }"
    class="custom-tooltip"
    @mousedown.prevent
  >
    <Button icon="pi pi-globe" size="small" class="p-button-text" @click="emit('translate')" />
  </div>
  <div
    v-if="visibleParagraph"
    :style="{
      position: 'absolute',
      left: `${left}px`,
      top: `${top}px`,
      zIndex: 1000,
    }"
  >
    <p>번역 문단</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, watch, ref } from 'vue'
import Button from 'primevue/button'

const props = defineProps({
  visible: Boolean,
  left: Number,
  top: Number,
  visibleParagraph: Boolean,
})
const emit = defineEmits(['translate', 'save'])
</script>

<style scoped>
.custom-tooltip {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  padding: 8px 12px;
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
