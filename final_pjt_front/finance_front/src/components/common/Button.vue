<template>
  <button :type="type" :class="computedClasses" :disabled="disabled" @click="$emit('click')">
    <!-- <button :type="type" :class="computedClasses" :disabled="disabled" @click="$emit('click')"> -->
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'button',
  },
  variant: {
    type: String,
    default: 'primary', // 기본값은 primary입니다. options: primary, secondary, danger
  },
  size: {
    type: String,
    default: 'md', // options: sm, md, lg
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  full: {
    type: Boolean,
    default: false,
  },
})

const baseClasses =
  'inline-flex items-center justify-center px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 focus:outline-none focus-visible:outline-none focus-visible:ring-0 focus-visible:ring-transparent'

// const baseClasses =
//   'inline-flex items-center justify-center px-4 py-2 rounded-md text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-200'

const variantClasses = {
  primary: 'bg-zinc-800 text-white hover:bg-zinc-950 focus:ring-zinc-500',
  secondary:
    'bg-gray-100 text-gray-800 hover:bg-gray-200 focus:ring-gray-300 border border-gray-200',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
}

const sizeClasses = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-5 py-3 text-base',
}

const computedClasses = computed(() => {
  return [
    baseClasses,
    variantClasses[props.variant],
    sizeClasses[props.size],
    props.full ? 'w-full' : '',
    props.disabled ? 'opacity-50 cursor-not-allowed' : '',
  ].join(' ')
})
</script>

<style scoped></style>
