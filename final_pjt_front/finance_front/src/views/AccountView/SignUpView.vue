<template>
  <div class="container flex items-center justify-center pt-28 pb-20">
    <div class="max-w-6xl w-full grid grid-cols-1 md:grid-cols-2 gap-12">
      
      <!-- 왼쪽 소개 -->
      <div class="space-y-6">
        <h1 class="text-4xl font-extrabold">회원가입</h1>
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

      <!-- 오른쪽 폼 -->
      <div class="bg-white p-8 shadow-md rounded-lg">
        <!-- 단계 표시 -->
        <div class="flex justify-between items-center mb-6">
          <div class="flex items-center space-x-2">
            <div class="w-6 h-6 rounded-full bg-black text-white text-center text-sm font-bold">1</div>
            <div class="w-40 h-1 bg-black" :class="{ 'bg-gray-200': currentStep === 1 }"></div>
            <div class="w-6 h-6 rounded-full" :class="currentStep === 2 ? 'bg-black text-white' : 'bg-gray-200 text-gray-500'">2</div>
          </div>
          <span class="text-sm text-gray-500">단계 {{ currentStep }} / 2</span>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- STEP 1 -->
          <template v-if="currentStep === 1">
            <div>
              <label class="block mb-1 text-sm font-medium">아이디</label>
              <input v-model="form.username" type="text" placeholder="아이디를 입력하세요"
                     class="w-full border border-gray-300 rounded-md px-4 py-2" />
            </div>
            <div>
              <label class="block mb-1 text-sm font-medium">이메일</label>
              <input v-model="form.email" type="email" placeholder="이메일을 입력하세요"
                    class="w-full border border-gray-300 rounded-md px-4 py-2" />
            </div>
            <div>
              <label class="block mb-1 text-sm font-medium">비밀번호</label>
              <input v-model="form.password1" type="password" placeholder="비밀번호를 입력하세요"
                     class="w-full border border-gray-300 rounded-md px-4 py-2" />
            </div>
            <div>
              <label class="block mb-1 text-sm font-medium">비밀번호 확인</label>
              <input v-model="form.password2" type="password" placeholder="비밀번호를 다시 입력하세요"
                     class="w-full border border-gray-300 rounded-md px-4 py-2" />
            </div>
            <button type="button" @click="nextStep"
                    class="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800">
              다음
            </button>
          </template>

          <!-- STEP 2 -->
          <template v-else>
            <div>
              <label class="block mb-1 text-sm font-medium">이름</label>
              <input v-model="form.name" type="text" placeholder="이름을 입력하세요"
                     class="w-full border border-gray-300 rounded-md px-4 py-2" />
            </div>
            <div>
              <label class="block mb-1 text-sm font-medium">닉네임</label>
              <input v-model="form.nickname" type="text" placeholder="닉네임을 입력하세요"
                     class="w-full border border-gray-300 rounded-md px-4 py-2" />
            </div>
            <div>
              <label class="block mb-1 text-sm font-medium">프로필 이미지</label>
              <div class="flex items-center space-x-4">
                <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center">
                  <span class="text-3xl">👤</span>
                </div>
                <input type="file" @change="handleFileUpload"
                       class="border border-gray-300 px-3 py-1 rounded-md" />
              </div>
            </div>
            <div class="flex justify-between mt-6">
              <button type="button" @click="prevStep"
                      class="border border-gray-400 text-gray-700 px-4 py-2 rounded-md">
                이전
              </button>
              <button type="submit" class="bg-black text-white px-6 py-2 rounded-md hover:bg-gray-800">
                가입 완료
              </button>
            </div>
          </template>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'
import { useRouter } from 'vue-router'

const router = useRouter()

const currentStep = ref(1)
const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  name: '',
  nickname: '',
  profileImage: null,
})

const nextStep = () => {
    if (!form.value.username || !form.value.email || !form.value.password1 || form.value.password1 !== form.value.password2) {
      alert('아이디, 이메일, 비밀번호를 확인해주세요.')
      return
    }
    currentStep.value = 2
}

const prevStep = () => {
  currentStep.value = 1
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  form.value.profileImage = file
}

const accountStore = useAccountStore()

const handleSubmit = () => {
  const payload = { ...form.value }
  accountStore.signUp(payload)
  alert('🎉 회원가입이 완료되었습니다!')

    // 예: 로그인 페이지로 이동
    router.push({ name: 'home' }) 
}
</script>

<style scoped>
</style>
