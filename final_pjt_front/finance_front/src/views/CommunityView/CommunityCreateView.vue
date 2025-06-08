<template>
  <div class="container mx-auto pt-28">
    <div class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-xl">
        <h2 class="text-xl font-bold mb-2">새 게시글 작성</h2>
        <p class="text-gray-600 text-sm mb-4">금융 상품에 대한 질문이나 의견을 공유해보세요.</p>
        <label class="block mb-2 font-medium">제목</label>
        <input v-model="title" type="text" class="w-full border rounded px-3 py-2 mb-4" placeholder="게시글 제목을 입력하세요" />
  
        <label class="block mb-2 font-medium">내용</label>
        <textarea v-model="content" rows="5" class="w-full border rounded px-3 py-2 mb-4" placeholder="게시글 내용을 입력하세요"></textarea>
  
        <div class="text-right">
          <button @click="goToList" class="px-4 py-2 mr-2 rounded border">취소</button>
          <button @click="createPost" class="bg-black text-white px-4 py-2 rounded">게시하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const emit = defineEmits(['close', 'created'])
const title = ref('')
const content = ref('')

const createPost = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/community/posts/', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`
      }
    })
    emit('created')
    emit('close')
    router.push({ name: 'community' })
  } catch (error) {
    alert('게시글 등록 실패')
    console.error(error)
  }
}
const goToList = () => {
  router.push({ name: 'community' })
}
</script>