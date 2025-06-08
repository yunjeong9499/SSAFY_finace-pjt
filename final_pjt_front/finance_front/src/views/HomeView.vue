<template>
  <div>
    <!-- Hero Section -->
    <!-- Hero Section -->
<div
  class="w-full h-screen bg-cover bg-center flex items-center justify-center relative"
  :style="{ backgroundImage: `url(${landingBg})` }"
>
  <div class="text-black text-center px-4">
    <h1 class="text-5xl font-bold">
      복잡한 금융, 이제 Faind로 쉽게 찾아보세요 <br />
    </h1>
    <p class="mt-2 text-2xl">
      당신의 금융 라이프가 달라집니다. 궁금한 내용은 드래그해보세요
    </p>
  </div>
</div>


    <!-- 캐러셀 -->
    <Carousel />
    
    <!-- Featured Articles Section -->
    <div class="pt-20 px-5 py-0 pb-20">
      <h1 class="text-4xl font-bold text-center mb-10">지금 알아야 할 머니 정보</h1>

      <div class="grid grid-cols-[25rem_1fr] gap-6 items-start">
        <!-- 왼쪽 고정 카드 -->
        <Card
          class="transition-transform transition-shadow duration-200 hover:-translate-y-1 hover:shadow-xl h-full overflow-hidden"
          style="width: 100%"
        >
          <template #header>
            <img alt="고정 이미지" :src="article_thumbnail" class="w-full h-48 object-cover" />
          </template>
          <template #title>예금과 적금, 그 차이와 특징</template>
          <template #subtitle>예적금의 뜻과 개념을 알아보자</template>
          <template #content>
            <p class="text-sm text-gray-700">
              예금과 적금, 뭐가 다를까? 내 상황에 딱 맞는 금융상품을 쉽게 알려드립니다!
            </p>
          </template>
          <template #footer>
            <div class="mt-4">
              <RouterLink to="/articles/9">
                <Button label="자세히 보기" class="w-full" />
              </RouterLink>
            </div>
          </template>
        </Card>

        <!-- 오른쪽 기사 카드 4개 -->
        <div class="grid grid-cols-1 gap-4">
          <RouterLink
            v-for="article in featuredArticles"
            :key="article.id"
            :to="`/articles/${article.id}`"
            class="block"
          >
            <Card class="hover:shadow-md transition">
              <template #title>
                <div class="font-semibold text-lg">{{ article.title }}</div>
              </template>
              <template #content>
                <p class="text-sm text-gray-600">{{ article.description }}</p>
              </template>
            </Card>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Carousel from '@/components/Carousel.vue'
import axios from 'axios'
import landingBg from '@/assets/imgs/img_landing.png'
import article_thumbnail from '@/assets/imgs/thumbnail.png'


// ✅ 홈에 표시할 기사 4개 
const featuredArticles = ref([
  { id: 1, title: 'ETF 투자 전략', description: 'ETF에 처음 투자하는 사람들을 위한 팁' },
  { id: 2, title: 'ISA 계좌 개설법', description: 'ISA 계좌로 절세 효과 누리는 법' },
  { id: 3, title: '공모주 청약 가이드', description: '공모주 투자의 장단점과 신청 방법' },
  { id: 4, title: '금융 앱 추천', description: '편리한 자산관리를 위한 금융 앱 소개' },
])
</script>

<style scoped></style>