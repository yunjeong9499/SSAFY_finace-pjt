<template>
  <div class="container mx-auto pt-28 pb-20">
    <router-link :to="{ name: 'articles' }" class="text-sm text-gray-600 hover:underline">
      ← 기사 메인으로 돌아가기
    </router-link>
    <div class="prose max-w-none p-6" v-if="article">
      
      <h1>{{ article.title }}</h1>
      <p class="text-sm text-gray-500">{{ formatDate(article.created_at) }}</p>
      <img v-if="article.image" :src="article.image" class="w-full rounded mb-6" />
      <div v-html="renderedContent" class="prose prose-lg max-w-none" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'

const route = useRoute()
const article = ref({})
const renderedContent = computed(() => marked(article.value.content || ''))

console.log(article.value)
// onMounted(async () => {
//   const res = await axios.get(`/api/articles/${route.params.id}/`)
//   article.value = res.data
// })
onMounted(async () => {
  try {
    const res = await axios.get(`/api/articles/${route.params.id}/`)
    console.log(res.data)  // ✅ 응답 전체 확인
    article.value = res.data
  } catch (err) {
    console.error('기사 불러오기 실패', err)
  }
})
function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString()
}
</script>
