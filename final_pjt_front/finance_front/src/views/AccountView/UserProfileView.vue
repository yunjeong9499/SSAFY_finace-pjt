<template>
  <div class="max-w-7xl mx-auto pt-28">
    <!-- 상단 헤더 -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
      <h1 class="text-3xl font-bold mb-4 md:mb-0">내 프로필</h1>
      <div class="flex gap-2">
        <RouterLink :to="{ name: 'changepassword'}" class="border px-4 py-2 rounded text-sm hover:bg-gray-100">
          비밀번호 변경
        </RouterLink>
        <RouterLink :to="{ name: 'profileEdit'}" class="bg-black text-white px-4 py-2 rounded text-sm hover:bg-gray-800">
          프로필 편집
        </RouterLink>
        <button @click="deleteAccount" class="text-red-500 text-sm hover:underline">
          회원 탈퇴
        </button>
      </div>
    </div>
    

    <!-- 메인 레이아웃 -->
    <div class="flex flex-col md:flex-row gap-8">
      <!-- 좌측 프로필 카드 -->
      <div class="w-full md:w-1/3 bg-white border rounded-lg p-6 text-center">
        <div class="w-24 h-24 mx-auto rounded-full bg-gray-100 overflow-hidden mb-4">
          <img
            v-if="userInfo.profile_image"
            :src="userInfo.profile_image"
            alt="프로필 이미지"
            class="w-full h-full object-cover"
          />
        </div>
        <p class="text-xl font-semibold">{{ userInfo.nickname || '닉네임 없음' }}</p>
        <p class="text-gray-500">{{ userInfo.name || '이름 없음' }}</p>
        <div class="mt-4 text-left text-sm space-y-1">
          <p><strong>아이디:</strong> {{ userInfo.username }}</p>
          <p><strong>이메일:</strong> {{ userInfo.email }}</p>
        </div>
      </div>

      <!-- 우측 콘텐츠 -->
      <div class="w-full md:w-2/3">
        <!-- 탭 -->
        <div class="flex border-b mb-4 text-sm font-medium">
          <button
            :class="[tab === 'deposit' ? 'border-black text-black' : 'text-gray-400 hover:text-black', 'pb-2 mr-6 border-b-2']"
            @click="tab = 'deposit'"
          >
            스크랩한 예금 상품
          </button>
          <button
            :class="[tab === 'saving' ? 'border-black text-black' : 'text-gray-400 hover:text-black', 'pb-2 border-b-2']"
            @click="tab = 'saving'"
          >
            스크랩한 적금 상품
          </button>
        </div>

        <!-- 스크랩 리스트 -->
        <div v-if="!isLoading">
          <ul v-if="filteredScraps.length > 0" class="space-y-4">
            <li v-for="scrap in filteredScraps" :key="scrap.id" class="p-4 border rounded-lg">
              <template v-if="tab === 'deposit' && scrap.deposit">
                <h3 class="font-bold text-lg">[예금] {{ scrap.deposit.name }} - {{ scrap.deposit.bank.name }}</h3>
                <div v-if="scrap.deposit.options?.length" class="text-sm text-green-700 mt-1">
                  최고 금리: {{ getMaxRate(scrap.deposit.options) }}% /
                  기간: {{ getTerm(scrap.deposit.options) }}개월
                </div>
                <div class="mt-2 flex gap-3">
                  <RouterLink
                    :to="{ name: 'deposit-detail', params: { id: scrap.deposit.id }}"
                    class="text-sm px-3 py-1 border rounded hover:bg-gray-100"
                  >
                    상세보기
                  </RouterLink>
                  <button
                    @click="unscrap(scrap.id)"
                    class="text-sm px-3 py-1 border border-red-500 text-red-600 rounded hover:bg-red-50"
                  >
                    스크랩 해제
                  </button>
                </div>
              </template>

              <template v-if="tab === 'saving' && scrap.saving">
                <h3 class="font-bold text-lg">[적금] {{ scrap.saving.name }} - {{ scrap.saving.bank.name }}</h3>
                <div v-if="scrap.saving.options?.length" class="text-sm text-green-700 mt-1">
                  최고 금리: {{ getMaxRate(scrap.saving.options) }}% /
                  기간: {{ getTerm(scrap.saving.options) }}개월
                </div>
                <div class="mt-2 flex gap-3">
                  <RouterLink
                    :to="{ name: 'saving-detail', params: { id: scrap.saving.id }}"
                    class="text-sm px-3 py-1 border rounded hover:bg-gray-100"
                  >
                    상세보기
                  </RouterLink>
                  <button
                    @click="unscrap(scrap.id)"
                    class="text-sm px-3 py-1 border border-red-500 text-red-600 rounded hover:bg-red-50"
                  >
                    스크랩 해제
                  </button>
                </div>
              </template>
            </li>
          </ul>
          <div v-else class="text-gray-500">스크랩한 상품이 없습니다.</div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import { storeToRefs } from 'pinia'

const router = useRouter()
const accountStore = useAccountStore()
const { userInfo, scraps } = storeToRefs(accountStore)

const isLoading = ref(true)
const tab = ref('deposit') // 'deposit' or 'saving'

onMounted(async () => {
  try {
    await accountStore.userProfile()
    await accountStore.fetchScraps()
  } catch (error) {
    console.error('프로필 조회 오류:', error)
  } finally {
    isLoading.value = false
  }
})

const filteredScraps = computed(() => {
  return scraps.value.filter(scrap =>
    tab.value === 'deposit' ? scrap.deposit : scrap.saving
  )
})

const getMaxRate = (options) => {
  return Math.max(...options.map(opt => opt.intr_rate2 || 0))
}

const getTerm = (options) => {
  const maxRate = getMaxRate(options)
  const opt = options.find(o => o.intr_rate2 === maxRate)
  return opt?.save_trm || '-'
}

const deleteAccount = async () => {
  if (confirm('정말로 회원 탈퇴하시겠습니까?')) {
    await accountStore.deleteAccount()
    router.push({ name: 'home' })
  }
}

const unscrap = async (scrapId) => {
  try {
    await accountStore.removeScrap(scrapId)
    await accountStore.fetchScraps()
  } catch (error) {
    alert('스크랩 해제 중 오류가 발생했습니다.')
    console.error(error)
  }
}

const activeTabClass = 'border-b-2 border-black pb-2 text-black'
const inactiveTabClass = 'text-gray-400 hover:text-black pb-2'
</script>

