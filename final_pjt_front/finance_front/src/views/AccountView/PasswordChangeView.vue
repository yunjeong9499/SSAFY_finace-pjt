<template>
  <div class="max-w-md mx-auto pt-28 px-4">
    <h1 class="text-3xl font-bold text-center mb-8">비밀번호 변경</h1>

    <form @submit.prevent="onChangePassword" class="bg-white shadow-md rounded-lg p-8 space-y-6">
      <!-- 자물쇠 아이콘 -->
      <div class="flex justify-center">
        <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center">
          <span class="text-3xl">🔒</span>
        </div>
      </div>

      <!-- 현재 비밀번호 -->
      <div>
        <label for="oldpassword" class="block text-sm font-medium mb-1">현재 비밀번호</label>
        <input
          id="oldpassword"
          type="password"
          v-model="oldpassword"
          placeholder="현재 비밀번호를 입력하세요"
          class="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <!-- 새 비밀번호 -->
      <div>
        <label for="newpassword1" class="block text-sm font-medium mb-1">새 비밀번호</label>
        <input
          id="newpassword1"
          type="password"
          v-model="newpassword1"
          placeholder="새 비밀번호를 입력하세요"
          class="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <!-- 새 비밀번호 확인 -->
      <div>
        <label for="newpassword2" class="block text-sm font-medium mb-1">새 비밀번호 확인</label>
        <input
          id="newpassword2"
          type="password"
          v-model="newpassword2"
          placeholder="새 비밀번호를 다시 입력하세요"
          class="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <!-- 버튼 -->
      <div class="flex justify-between pt-4">
        <RouterLink
          to="/profile"
          class="px-4 py-2 border border-gray-400 rounded-md text-sm hover:bg-gray-100"
        >
          취소
        </RouterLink>
        <button
          type="submit"
          class="px-6 py-2 bg-black text-white rounded-md text-sm hover:bg-gray-800"
        >
          변경하기
        </button>
      </div>
    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'
import { useRouter } from 'vue-router'

const oldpassword = ref('')
const newpassword1 = ref('')
const newpassword2 = ref('')

const router = useRouter()
const accountStore = useAccountStore()

const onChangePassword = function () {
    const payload = {
        oldpassword: oldpassword.value,
        newpassword1: newpassword1.value,
        newpassword2: newpassword2.value
    }
    if (newpassword1.value !== newpassword2.value) {
        alert('새 비밀번호가 일치하지 않습니다.')
        return
    }
        console.log('payload:', payload)
        console.log({
            oldpassword: oldpassword.value,
            newpassword1: newpassword1.value,
            newpassword2: newpassword2.value
        })

        accountStore.changePassword(payload)
        alert('비밀번호 변경이 완료되었습니다!')
        router.push({ name: 'profile' })
}
</script>

<style scoped>

</style>