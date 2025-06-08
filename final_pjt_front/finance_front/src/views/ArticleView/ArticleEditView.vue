<template>
  <form @submit.prevent="submit">
    <input v-model="form.title" placeholder="제목" required class="p-inputtext" />
    <select v-model="form.article_type" class="p-dropdown">
      <option value="strategy">투자 전략/팁</option>
      <option value="trend">경제·금융 트렌드</option>
      <option value="app">금융 앱/서비스 소개</option>
      <option value="glossary">용어/상식 사전</option>
    </select>
    <input type="file" @change="onFileChange" />
    <Editor v-model="form.content" editorStyle="height: 320px" />
    <button type="submit" class="p-button p-component">수정</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const form = ref({
  title: '',
  article_type: 'strategy',
  content: '',
  image: null
})

onMounted(async () => {
  const res = await axios.get(`/api/articles/${route.params.id}/`)
  form.value.title = res.data.title
  form.value.article_type = res.data.article_type
  form.value.content = res.data.content
  // 기존 이미지는 별도 표시 가능
})

function onFileChange(e) {
  form.value.image = e.target.files[0]
}

async function submit() {
  const formData = new FormData()
  formData.append('title', form.value.title)
  formData.append('article_type', form.value.article_type)
  formData.append('content', form.value.content)
  if (form.value.image) {
    formData.append('image', form.value.image)
  }
  await axios.put(`/api/articles/${route.params.id}/update/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  // 성공 후 라우팅 등 처리
}
</script>
