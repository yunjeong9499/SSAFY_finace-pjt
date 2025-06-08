<template>
  <div class="py-16 px-6 text-center bg-white">
    <h2 class="text-2xl font-bold mb-10">주요 서비스 기능</h2>

    <div class="relative max-w-md mx-auto">
      <div class="flex flex-col items-center gap-4">
        <component :is="features[current].icon" class="w-16 h-16 text-blue-500" />
        <h3 class="text-xl font-semibold">{{ features[current].title }}</h3>
        <p class="text-gray-500 text-sm">{{ features[current].description }}</p>
      </div>

      <!-- 좌우 화살표 -->
      <div class="absolute left-0 top-1/2 -translate-y-1/2">
        <button @click="prev" class="rounded-full border p-2 hover:bg-gray-100">
          <ChevronLeft />
        </button>
      </div>
      <div class="absolute right-0 top-1/2 -translate-y-1/2">
        <button @click="next" class="rounded-full border p-2 hover:bg-gray-100">
          <ChevronRight />
        </button>
      </div>

      <!-- 인디케이터 -->
      <div class="flex justify-center mt-6 gap-2">
        <span
          v-for="(f, idx) in features"
          :key="idx"
          :class="[
            'w-2 h-2 rounded-full',
            idx === current ? 'bg-blue-500' : 'bg-gray-300'
          ]"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ChevronLeft, ChevronRight, BrainCircuit, MapPin, Bookmark, Bot, Newspaper } from 'lucide-vue-next'

const features = [
  {
    title: '맞춤 상품 추천',
    description: '나이, 직업, 관심사 기반 AI 예/적금 상품 추천',
    icon: BrainCircuit,
  },
  {
    title: '주변 은행 찾기',
    description: '내 위치 기반 가까운 은행 지점 검색',
    icon: MapPin,
  },
  {
    title: '상품 스크랩 기능',
    description: '관심 있는 상품을 저장하고 비교하기',
    icon: Bookmark,
  },
  {
    title: 'AI 챗봇 상담',
    description: '금융 관련 질문을 챗봇에게 바로!',
    icon: Bot,
  },
  {
    title: '금융 기사 추천',
    description: '재테크 기사 큐레이션 제공',
    icon: Newspaper,
  }
]

const current = ref(0)
const prev = () => current.value = (current.value - 1 + features.length) % features.length
const next = () => current.value = (current.value + 1) % features.length
</script>
