<template>
  <div class="container flex items-center justify-center pt-28 pb-20">
    <div class="max-w-6xl w-full grid grid-cols-1 md:grid-cols-2 gap-12">
      <!-- 좌측 서비스 소개 -->
      <div class="space-y-6">
        <h1 class="text-4xl font-extrabold">로그인</h1>
        <p class="text-lg text-gray-600">파인드에 오신 것을 환영합니다.</p>
        <div class="bg-gray-100 p-6 rounded-lg space-y-4">
          <h2 class="text-xl font-bold">파인드 서비스</h2>
          <ul class="space-y-3">
            <li class="flex items-start">
              <div class="w-6 h-6 rounded-full bg-black text-white flex items-center justify-center font-bold text-sm mr-3">1</div>
              <p>AI 기반 맞춤형 예·적금 추천 서비스</p>
            </li>
            <li class="flex items-start">
              <div class="w-6 h-6 rounded-full bg-black text-white flex items-center justify-center font-bold text-sm mr-3">2</div>
              <p>주식 관심 종목 분석</p>
            </li>
            <li class="flex items-start">
              <div class="w-6 h-6 rounded-full bg-black text-white flex items-center justify-center font-bold text-sm mr-3">3</div>
              <p>금융 용어/상식 드래그 해설</p>
            </li>
          </ul>
        </div>
      </div>

      <!-- 우측 로그인 폼 -->
      <div class="bg-white p-8 shadow-md rounded-lg">
        <h2 class="text-2xl font-bold mb-6">계정 로그인</h2>
        <form @submit.prevent="logIn" class="space-y-4">
          <div>
            <label for="username" class="block mb-1 text-sm font-medium">아이디</label>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="아이디를 입력하세요"
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
          <div>
            <label for="password" class="block mb-1 text-sm font-medium">비밀번호</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="비밀번호를 입력하세요"
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
          <div class="pt-12">
            <button type="submit" class="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800">
              로그인
            </button>
          </div>
        </form>
        <div v-if="errorMessage" class="text-red-600 text-sm mt-2">
          {{ errorMessage }}
        </div>
        <p class="mt-4 text-center text-sm text-gray-600">
          아직 계정이 없으신가요?
          <router-link to="/signup" class="font-semibold hover:underline">회원가입</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const accountStore = useAccountStore()

const errorMessage = ref('')  // ✅ 실패 메시지 상태 추가

const logIn = async () => {
  const payload = {
    username: username.value,
    password: password.value
  }

  try {
    errorMessage.value = ''  // 이전 메시지 초기화
    await accountStore.logIn(payload)
    router.push({ name: 'home' })  // 로그인 성공 시 이동
  } catch (err) {
    errorMessage.value = '❌ 로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.'
    alert(errorMessage.value)
  }
}
</script>

<style scoped>
/* 필요시 추가적인 스타일링 가능 */
</style>
