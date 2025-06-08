<template>
  <div class="max-w-3xl mx-auto pt-28">
    <!-- 🔙 프로필로 돌아가기 -->
    <div class="mb-4">
      <router-link
        :to="{ name: 'profile' }"
        class="text-sm text-gray-600 hover:text-black flex items-center space-x-1"
      >
        <span>←</span>
        <span>프로필로 돌아가기</span>
      </router-link>
    </div>
    
    <!-- 제목 -->
    <h1 class="text-3xl font-extrabold mb-6">프로필 편집</h1>

  
    <form @submit.prevent="onSubmit" class="bg-white rounded-lg shadow-md p-8 space-y-6">
      <!-- 프로필 이미지 -->
      <div class="flex items-center space-x-6">
        <div class="w-24 h-24 rounded-full bg-gray-100 overflow-hidden flex justify-center items-center">
          <img
            v-if="previewImage || user.profile_image"
            :src="previewImage || 'http://127.0.0.1:8000' + user.profile_image"
            alt="Profile"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-4xl text-gray-400">👤</span>
        </div>
        <div>
          <label
            class="inline-flex items-center px-4 py-2 bg-white border rounded-md shadow-sm text-sm font-medium cursor-pointer hover:bg-gray-50"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828L18 10.828M16 5l2 2M4 20h4l10-10a2 2 0 00-2.828-2.828L4 17.172V20z"
              />
            </svg>
            이미지 변경
            <input type="file" class="hidden" @change="onFileChange" />
          </label>
        </div>
      </div>

      <!-- 이름 -->
      <div>
        <label class="block mb-1 font-medium">이름</label>
        <input
          v-model="user.name"
          type="text"
          class="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <!-- 닉네임 -->
      <div>
        <label class="block mb-1 font-medium">닉네임</label>
        <input
          v-model="user.nickname"
          type="text"
          class="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <!-- 아이디 (읽기 전용) -->
      <div>
        <label class="block mb-1 font-medium">아이디</label>
        <input
          type="text"
          :value="user.username"
          disabled
          class="w-full bg-gray-100 text-gray-600 border border-gray-300 rounded-md px-4 py-2 cursor-not-allowed"
        />
        <small class="text-sm text-gray-500">아이디는 변경할 수 없습니다.</small>
      </div>

      <!-- 이메일 (읽기 전용) -->
      <div>
        <label class="block mb-1 font-medium">이메일</label>
        <input
          type="email"
          :value="user.email"
          disabled
          class="w-full bg-gray-100 text-gray-600 border border-gray-300 rounded-md px-4 py-2 cursor-not-allowed"
        />
        <small class="text-sm text-gray-500">이메일은 변경할 수 없습니다.</small>
      </div>

      <!-- 버튼 -->
      <div class="flex justify-end space-x-3">
        <button
          type="button"
          class="px-4 py-2 border border-gray-400 rounded-md text-gray-700 hover:bg-gray-100"
          @click="syncUserInfo"
        >
          취소
        </button>
        <button
          type="submit"
          class="px-6 py-2 bg-black text-white rounded-md hover:bg-gray-800"
        >
          저장하기
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()
const router = useRouter()

const user = ref({
  name: '',
  nickname: '',
  username: '',
  email: '',
  profile_image: ''
})

const profileImage = ref(null)
const previewImage = ref(null)

onMounted(async () => {
  await accountStore.userProfile()
  syncUserInfo()
})

watch(
  () => accountStore.userInfo,
  () => syncUserInfo(),
  { deep: true }
)

const syncUserInfo = () => {
  const info = accountStore.userInfo
  user.value.name = info.name || ''
  user.value.nickname = info.nickname || ''
  user.value.username = info.username || ''
  user.value.email = info.email || ''
  user.value.profile_image = info.profile_image || ''
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  profileImage.value = file
  if (file) {
    const reader = new FileReader()
    reader.onload = (event) => {
      previewImage.value = event.target.result
    }
    reader.readAsDataURL(file)
  }
}

const onSubmit = async () => {
  const formData = new FormData()
  formData.append('name', user.value.name)
  formData.append('nickname', user.value.nickname)
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }
  await accountStore.updateProfile(formData)
  alert('프로필이 수정되었습니다!')
  router.push({ name: 'profile' }) 
}
</script>
