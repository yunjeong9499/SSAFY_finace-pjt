<template>
  <div class="container mx-auto pt-28">
    <h2 class="text-xl font-bold mb-4">게시글 수정</h2>
    <input v-model="title" type="text" class="w-full border rounded px-3 py-2 mb-4" />
    <textarea v-model="content" rows="8" class="w-full border rounded px-3 py-2 mb-4"></textarea>

    <div class="text-right">
      <button @click="$router.back()" class="px-4 py-2 border rounded mr-2">취소</button>
      <button @click="updatePost" class="bg-green-500 text-white px-4 py-2 rounded">저장하기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const title = ref('')
const content = ref('')

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:8000/api/community/posts/${route.params.id}/`)
  title.value = res.data.title
  content.value = res.data.content
})

const updatePost = async () => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/community/posts/${route.params.id}/`, {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`
      }
    })
    router.push({ name: 'community-detail', params: { id: route.params.id } })
  } catch (error) {
    alert('수정 실패')
    console.error(error)
  }
}
</script>