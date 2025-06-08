<template>
  <div class="container mx-auto pt-28 pb-20">
    <div class="container mx-auto p-2" v-if="post">
      <router-link :to="{ name: 'community' }" class="text-sm text-gray-600 hover:underline"> ← 커뮤니티로 돌아가기 </router-link>

      <div class="flex justify-between items-start mt-4">
        <div>
          <h2 class="text-3xl font-bold mb-1">{{ post.title }}</h2>
          <p class="text-gray-500 text-sm">{{ post.author_nickname }} • {{ formatDate(post.created_at) }}</p>
        </div>
        <!-- 게시글 작성자만 수정/삭제 버튼 노출 -->
        <div v-if="post.is_author">
          <router-link :to="{ name: 'community-edit', params: { id: post.id } }" class="text-sm text-blue-600"> ✎ 수정하기 </router-link>
          <button @click="deletePost(post.id)" class="text-sm text-red-600 ml-2">삭제하기</button>
        </div>
      </div>
      <div class="min-h-80">
        <p class="mt-6 text-base whitespace-pre-line">{{ post.content }}</p>
      </div>
      <!-- 댓글 목록 -->
      <div class="mt-10">
        <h3 class="text-lg font-bold mb-4">💬 댓글 {{ post.comment_count }}개</h3>

        <!-- 댓글 작성 -->
        <div v-if="isLogin" class="mb-4">
          <textarea v-model="newComment" class="w-full border rounded p-2" placeholder="댓글을 작성해보세요"></textarea>
          <div class="text-right mt-2">
            <button @click="submitComment" class="bg-black text-white px-4 py-1 rounded">댓글 작성</button>
          </div>
        </div>

        <div v-for="comment in comments" :key="comment.id" class="border rounded p-3 mb-2">
          <div class="flex justify-between items-center mb-1">
            <p class="text-sm text-gray-600">{{ comment.author_nickname }}</p>
            <p class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</p>
          </div>
          <p>{{ comment.content }}</p>
          <!-- 댓글 작성자만 삭제 버튼 노출 -->
          <div class="text-right mt-2" v-if="comment.is_author">
            <button @click="deleteComment(comment.id)" class="text-sm text-gray-500 hover:text-red-500">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { storeToRefs } from 'pinia'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const postId = route.params.id
const post = ref(null)
const comments = ref([])
const newComment = ref('')

const accountStore = useAccountStore()
const { isLogin } = storeToRefs(accountStore)

onMounted(async () => {
  await fetchPost()
  await fetchComments()
})

async function fetchPost() {
  try {
    const res = await axios.get(`/api/community/posts/${postId}/`)
    post.value = res.data
  } catch (err) {
    console.error('게시글 조회 실패:', err)
  }
}

async function fetchComments() {
  try {
    const res = await axios.get(`/api/community/posts/${postId}/comments/`)
    comments.value = res.data
  } catch (err) {
    console.error('댓글 조회 실패:', err)
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return
  try {
    await axios.post(
      `/api/community/posts/${postId}/comments/`,
      {
        content: newComment.value,
      },
      {
        headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
      },
    )
    newComment.value = ''
    await fetchComments()
    await fetchPost()
  } catch (err) {
    alert('댓글 작성 실패')
    console.error(err)
  }
}

async function deleteComment(commentId) {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await axios.delete(`/api/community/posts/${postId}/comments/${commentId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
    })
    await fetchComments()
    await fetchPost()
  } catch (err) {
    alert('댓글 삭제 실패')
    console.error(err)
  }
}

async function deletePost(postId) {
  if (!confirm('게시글을 삭제하시겠습니까?')) return
  try {
    await axios.delete(`/api/community/posts/${postId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
    })
    router.push({ name: 'community' })
  } catch (err) {
    alert('게시글 삭제 실패')
    console.error(err)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
