<template>
  <div class="w-full bg-white py-20 flex justify-center"
       @mouseenter="pauseAutoplay"
       @mouseleave="resumeAutoplay">
    <div class="w-full max-w-[1420px] mx-auto px-6 sm:px-10">
      <Carousel
        ref="carousel"
        :itemsToShow="1"
        :wrapAround="true"
        :transition="500"
        :autoplay="autoplayValue"
        class="w-full"
      >
        <Slide v-for="(item, idx) in slides" :key="idx">
          <div class=" w-full max-w-[1150px] flex flex-col md:flex-row items-center md:gap-40 min-h-[500px]">
            <!-- 텍스트 영역 -->
            <div class="flex-1 flex flex-col justify-center items-start md:text-left text-center max-w-2xl pl-6">
              <h2 class="text-3xl md:text-4xl font-bold mb-4 whitespace-pre-line">
                {{ item.title }}
              </h2>
              <p class="text-lg md:text-xl text-gray-600 whitespace-pre-line leading-relaxed mb-10">
                {{ item.description }}
              </p>
              <!-- 버튼과 화살표 세로 정렬, 왼쪽 이동 -->
              <div class="flex flex-col gap-4 items-start mt-10 -translate-x-8">
                <button
                  class="px-8 py-3 border border-black rounded hover:bg-gray-100 text-lg font-medium"
                  @click="goToDetail(item.route)"
                >
                  자세히 보기
                </button>
                <div class="flex gap-4">
                  <!-- <button
                    @click="goPrev"
                    class="w-12 h-12 rounded-full border border-gray-300 flex items-center justify-center text-2xl hover:bg-gray-100"
                  >
                    &lt;
                  </button>
                  <button
                    @click="goNext"
                    class="w-12 h-12 rounded-full border border-gray-300 flex items-center justify-center text-2xl hover:bg-gray-100"
                  >
                    &gt;
                  </button> -->
                </div>
              </div>
            </div>
            <!-- 아이콘 영역 오른쪽 끝으로 -->
            <div class="flex-1 flex justify-end items-center mt-12 md:mt-0 ml-auto">
              <img :src="item.icon" alt="icon" class="w-[320px] md:w-[400px] object-contain drop-shadow-xl" />
            </div>
          </div>
        </Slide>
      </Carousel>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Carousel, Slide } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'
import { useRouter } from 'vue-router'

import bankIcon from '@/assets/images/bank_icon.png'
import chatbotIcon from '@/assets/images/chatbot_icon.png'
import stockIcon from '@/assets/images/stockchart_icon.png'
import recommendIcon from '@/assets/images/recommend_icon.png'
import textIcon from '@/assets/images/text_icon.png'

const router = useRouter()
const carousel = ref(null)
const autoplayValue = ref(2250) // 7초

function pauseAutoplay() {
  autoplayValue.value = 0
}
function resumeAutoplay() {
  autoplayValue.value = 2500
}
function goPrev() {
  carousel.value?.prev()
}
function goNext() {
  carousel.value?.next()
}
function goToDetail(route) {
  if (route) router.push(route)
}

const slides = [
  {
    title: '간편한 예적금 비교',
    icon: bankIcon,
    description: '여러 은행의 예적금 상품을 한눈에 비교해보세요.\n금리, 기간, 조건까지 쉽고 빠르게 확인할 수 있어요.',
    route: '/product/deposit',
  },
  {
    title: '관심 주식 종목 차트 확인',
    icon: stockIcon,
    description: '내가 선택한 주식의 차트를 실시간으로 확인하고,\n흐름을 한눈에 파악할 수 있어요.',
  },
  {
    title: 'AI 맞춤 예적금 추천',
    icon: recommendIcon,
    description: 'AI가 내 나이와 직업, 관심사를 분석해\n딱 맞는 예적금 상품을 추천해줘요.',
  },
  {
    title: '챗봇 서비스',
    icon: chatbotIcon,
    description: '모르는 게 있으면 챗봇에게 물어보세요.\n언제든지 친절하게 도와드릴게요.',
  },
  {
    title: 'AI가 설명!',
    icon: textIcon,
    description: '어려운 금융 용어, 드래그만 하면\nAI가 쉽게 풀어 설명해줘요.',
  },
]
</script>
 
<style scoped>
</style>