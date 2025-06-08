<template>
  <div class="container mx-auto pt-28 pb-20">
    <div>
      <h1 class="text-5xl font-bold mb-5">금융 인사이트</h1>
  
      <!-- 🔍 검색 & 필터 -->
      <div class="flex flex-wrap gap-4 items-center mb-6">
        <input
          v-model="keyword"
          @keydown.enter="searchArticles"
          placeholder="제목 검색..."
          class="border px-4 py-2 rounded w-full md:w-1/3"
        />
        <select v-model="selectedCategory" class="border px-4 py-2 rounded">
          <option value="">전체 카테고리</option>
          <option value="strategy">투자 전략/팁</option>
          <option value="trend">경제·금융 트렌드</option>
          <option value="app">금융 앱/서비스 소개</option>
          <option value="glossary">용어/상식 사전</option>
        </select>
        <button @click="searchArticles" class="bg-black text-white px-4 py-2 const searchArticles = () => {
  currentPage.value = 1 // 검색 시 항상 1페이지로 리셋
} rounded hover:bg-gray-800">검색</button>
      </div>
      <!-- 📄 기사 카드 목록 -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="article in paginatedArticles"
          :key="article.id"
          class="bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow"
        >
          <img
            v-if="article.image"
            :src="article.image"
            alt="썸네일"
            class="w-full h-48 object-cover rounded-t-lg"
          />
          <div class="p-4">
            <!-- 🏷 카테고리 뱃지 -->
            <span
              class="text-xs font-medium px-2 py-1 rounded-full text-white"
              :class="categoryBadgeClass(article.article_type)"
            >
              {{ article.article_type_display }}
            </span>
  
            <p class="text-xs text-gray-400 mt-1">{{ formatDate(article.created_at) }}</p>
  
            <h2 class="text-lg font-semibold my-2 line-clamp-2">{{ article.title }}</h2>
  
            <router-link
              :to="`/articles/${article.id}`"
              class="text-sm text-blue-600 hover:underline"
            >
              자세히 보기 →
            </router-link>
          </div>
        </div>
      </div>
  
      <!-- 📌 페이지네이션 -->
      <div class="flex justify-center mt-10" v-if="totalPages > 1">
        <button
          class="px-3 py-1 border rounded mx-1"
          :class="currentPage === page ? 'bg-black text-white' : 'bg-white'"
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
  
      <div v-if="filteredArticles.length === 0" class="text-center text-gray-500 mt-20">
        해당 조건의 기사가 없습니다.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const articles = ref([])
const keyword = ref('')
const selectedCategory = ref('')
const currentPage = ref(1)
const perPage = 6

onMounted(async () => {
  const res = await axios.get('/api/articles/')
  articles.value = res.data
})

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const categoryBadgeClass = (type) => {
  return {
    strategy: 'bg-indigo-600',
    trend: 'bg-green-600',
    app: 'bg-yellow-500',
    glossary: 'bg-gray-600'
  }[type] || 'bg-gray-400'
}

// 🔍 필터된 기사 목록
const filteredArticles = computed(() => {
  return articles.value.filter((a) => {
    const matchKeyword = a.title.toLowerCase().includes(keyword.value.toLowerCase())
    const matchCategory = selectedCategory.value === '' || a.article_type === selectedCategory.value
    return matchKeyword && matchCategory
  })
})

// 📄 현재 페이지 기사 목록
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredArticles.value.slice(start, start + perPage)
})

const totalPages = computed(() => Math.ceil(filteredArticles.value.length / perPage))
const searchArticles = () => {
  currentPage.value = 1 // 검색 시 항상 1페이지로 리셋
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
