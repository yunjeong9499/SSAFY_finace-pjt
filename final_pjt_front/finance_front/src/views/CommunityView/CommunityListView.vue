<template>
  <div class="container mx-auto pt-28 pb-20">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-5xl font-bold mb-5">자유 게시판</h1>

      <router-link
        to="/community/create"
        class="bg-black hover:bg-gray-800 text-white px-4 py-2 rounded text-sm"
      >
        + 게시글 작성
      </router-link>
    </div>

    <p class="text-gray-600 text-lg mb-4">금융 상품에 대한 질문이나 의견을 공유해보세요.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-10 gap-x-4 py-5">
      <div
        v-for="post in posts"
        :key="post.id"
        class="border rounded-lg p-4 shadow-sm hover:shadow-md transition duration-300 flex flex-col justify-between h-60"
      >
        <div>
          <router-link :to="{ name: 'community-detail', params: { id: post.id } }">
            <h2 class="font-bold text-lg mb-1 hover:underline">{{ post.title }}</h2>
          </router-link>
          <p class="text-sm text-gray-500">
            {{ post.author_nickname }} • {{ formatDate(post.created_at) }}
          </p>
          <p class="text-sm mt-2 text-gray-700 line-clamp-3">{{ post.content }}</p>
        </div>
        <div class="text-sm text-gray-500 mt-4">
          💬 {{ post.comment_count }} 댓글
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/community/posts/')
    posts.value = res.data
  } catch (err) {
    console.error('게시글 불러오기 실패:', err)
  }
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
