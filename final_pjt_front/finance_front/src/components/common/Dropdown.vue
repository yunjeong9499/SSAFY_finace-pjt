<template>
  <div ref="dropdownRef" class="relative inline-block text-left w-full" @click.stop>
    <!-- Dropdown Button -->
    <button
      type="button"
      @click="toggle"
      class="inline-flex items-center justify-between w-full px-4 py-2 text-sm font-medium text-black dark:text-white bg-white dark:bg-[#1E2028] border border-gray-200 dark:border-gray-700 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-none"
    >
      {{ selectedLabel }}
      <svg
        class="w-4 h-4 ml-2"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <transition name="fade">
      <div
        v-show="isOpen"
        class="origin-top-left absolute left-0 mt-2 w-full rounded-md shadow-lg bg-white dark:bg-[#1E2028] ring-1 ring-black ring-opacity-5 z-10"
      >
        <div>
          <button
            v-for="option in options"
            :key="option.value"
            @click="select(option)"
            class="w-full flex items-center px-4 py-2 text-sm text-black dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <svg
              v-if="option.icon"
              class="w-4 h-4 mr-3"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                :d="option.icon"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
              />
            </svg>
            {{ option.label }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: String,
  options: {
    type: Array,
    required: true,
  },
})
const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const dropdownRef = ref(null)
const selectedLabel = ref('선택하세요')

watch(
  () => props.modelValue,
  (newVal) => {
    const match = props.options.find((opt) => opt.value === newVal)
    selectedLabel.value = match ? match.label : '선택하세요'
  },
  { immediate: true },
)

function toggle() {
  isOpen.value = !isOpen.value
}

function select(option) {
  emit('update:modelValue', option.value)
  isOpen.value = false
}

function onClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('click', onClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', onClickOutside)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
