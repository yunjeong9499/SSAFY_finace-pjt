<template>
  <div v-if="isAdmin" class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
    <!-- 왼쪽: 기사 작성 -->
    <div>
      <h2 class="text-2xl font-bold mb-4">기사 작성</h2>

      <input
        v-model="form.title"
        placeholder="제목"
        class="border p-2 w-full mb-4"
      />

      <select v-model="form.article_type" class="border p-2 w-full mb-4">
        <option value="strategy">투자 전략/팁</option>
        <option value="trend">경제·금융 트렌드</option>
        <option value="app">금융 앱/서비스 소개</option>
        <option value="glossary">용어/상식 사전</option>
      </select>

      <!-- 이미지 업로드 -->
      <input
        type="file"
        @change="onImageUpload"
        accept="image/*"
        class="mb-4"
      />

      <!-- 마크다운 작성 -->
      <textarea
        v-model="form.content"
        rows="12"
        placeholder="Markdown 형식으로 본문을 작성하세요."
        class="border p-2 w-full font-mono mb-4"
      />

      <button @click="submit" class="bg-black text-white px-4 py-2 rounded">
        기사 저장
      </button>
    </div>

    <!-- 오른쪽: 실시간 프리뷰 -->
    <div>
      <h2 class="text-2xl font-bold mb-4">미리보기</h2>
      <div class="prose max-w-none border p-4 rounded bg-white" v-html="renderedContent" />
    </div>
  </div>

  <div v-else class="text-center text-gray-500 py-20 text-lg">
    ⚠️ 관리자만 접근할 수 있습니다.
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'

const router = useRouter()
const accountStore = useAccountStore()
const isAdmin = computed(() => accountStore.profile?.is_superuser)

const form = ref({
  title: '',
  article_type: 'strategy',
  content: '',
  image: null
})

const renderedContent = computed(() => marked(form.value.content || ''))

// 이미지 업로드 시 → 서버에 업로드 후 Markdown 링크 추가
const onImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('image', file)

  try {
    const res = await axios.post('/api/articles/upload-image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    const imageUrl = res.data.url
    form.value.content += `\n\n![이미지 설명](${imageUrl})\n`
    alert('이미지가 업로드되었습니다.')
  } catch (err) {
    alert('이미지 업로드 실패')
    console.error(err)
  }
}

// 기사 저장
const submit = async () => {
  try {
    const formData = new FormData()
    formData.append('title', form.value.title)
    formData.append('article_type', form.value.article_type)
    formData.append('content', form.value.content)
    if (form.value.image) {
      formData.append('image', form.value.image)
    }

    await axios.post('/api/articles/create/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    alert('기사 저장 완료!')
    router.push({ name: 'articles' })
  } catch (err) {
    alert('저장 실패')
    console.error(err)
  }
}
</script>

<style scoped>
/* Tailwind Typography 플러그인 사용 중이라면 별도 스타일은 없어도 됩니다 */
</style>
