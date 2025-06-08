<template>
  <div class="container mx-auto pt-28 pb-20">
    <h1 class="text-5xl font-bold mb-5">적금 상품 비교</h1>
    <p class="text-xl text-muted-foreground text-gray-500">
      다양한 은행의 적금 상품을 비교해보세요. 최적의 금리와 조건을 찾아보세요!
    </p>

    <!-- 필터 및 정렬 UI -->
    <div class="flex flex-wrap gap-3 mb-4 items-center py-5">
      <InputText type="text" v-model="keyword" placeholder="상품명" />
      <Select
        v-model="selectedBank"
        :options="banksOption"
        optionLabel="name"
        placeholder="전체 은행"
        class="w-full md:w-56"
      ></Select>
      <Select
        v-model="selectedSortKey"
        :options="sortOption"
        optionLabel="name"
        placeholder="금리순"
        class="w-full md:w-56"
      ></Select>
      <Select
        v-model="selectedSortOrder"
        :options="orderOption"
        optionLabel="name"
        placeholder="내림차순"
        class="w-full md:w-56"
      ></Select>
      <div class="w-full">
        <label class="text-gray-600 text-sm">최소 금리</label>
        <div class="flex items-center pl-4">
          <Slider v-model="minRate" :min="0" :max="5" :step="0.1" class="w-full" />
          <span class="ml-8 text-2xl font-bold"> {{ minRate }}% </span>
        </div>
      </div>
      <div class="ml-auto flex items-center space-x-2">
        <Button
          label="카드"
          icon="pi pi-objects-column"
          @click="viewMode = 'card'"
          :severity="viewMode === 'card' ? 'primary' : 'secondary'"
        ></Button>
        <Button
          label="표"
          icon="pi pi-bars"
          @click="viewMode = 'table'"
          :severity="viewMode === 'table' ? 'primary' : 'secondary'"
        ></Button>
      </div>
    </div>

    <!-- 카드형 보기 -->
    <div v-if="viewMode === 'card'" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div
        v-for="item in filteredList"
        :key="item.id"
        class="border rounded-lg p-6 shadow-sm hover:shadow-md"
      >
        <router-link :to="{ name: 'saving-detail', params: { id: item.id } }">
          <h3 class="font-bold text-lg hover:underline">{{ item.name }}</h3>
        </router-link>
        <p class="text-sm text-gray-500">{{ item.bank.name }}</p>
        <p class="text-red-500 text-xl font-semibold mt-2">{{ getMaxRate(item) }}%</p>
        <p class="text-sm">최대 기간: {{ getMaxTerm(item) }}개월</p>
        <p class="text-sm">최고 금리: {{ getMaxRate(item) }}%</p>
        <div class="mt-3" v-if="isLogin">
          <button @click="toggleScrap(item)" class="bg-black text-white px-4 py-2 rounded w-full">
            {{ isScrapped(item) ? '스크랩됨' : '스크랩하기' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 표형 보기 -->
    <table v-else class="table-auto w-full border">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-2 py-1">상품명</th>
          <th class="border px-2 py-1">금리</th>
          <th class="border px-2 py-1">기간</th>
          <th class="border px-2 py-1" v-if="isLogin">스크랩</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredList" :key="item.id">
          <td class="border px-2 py-1">
            <router-link
              :to="{ name: 'saving-detail', params: { id: item.id } }"
              class="hover:underline"
            >
              {{ item.name }} </router-link
            ><br />
            <span class="text-sm text-gray-500">{{ item.bank.name }}</span>
          </td>
          <td class="border px-2 py-1 text-red-500 font-semibold">{{ getMaxRate(item) }}%</td>
          <td class="border px-2 py-1">{{ getMaxTerm(item) }}개월</td>
          <td class="border px-2 py-1 text-center" v-if="isLogin">
            <button @click="toggleScrap(item)" class="text-sm border rounded px-3 py-1">
              {{ isScrapped(item) ? '스크랩됨' : '스크랩하기' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'
import Slider from 'primevue/slider'
import Button from 'primevue/button'

// Pinia 스토어에서 스크랩 데이터 가져오기
const accountStore = useAccountStore()
const { scraps, isLogin } = storeToRefs(accountStore)

// 상품 데이터
const rawData = ref([])

// 필터/정렬 상태
const keyword = ref('')
// const sortKey = ref('rate')
const minRate = ref(0)
const viewMode = ref('card')
// const sortOrder = ref('desc')
const selectedBank = ref('')
const selectedSortKey = ref({ name: '금리순', code: 'rate' })
const selectedSortOrder = ref({ name: '내림차순', code: 'desc' })
const banksOption = ref([])
const sortOption = ref([
  { name: '금리순', code: 'rate' },
  { name: '기간순', code: 'term' },
  { name: '은행명순', code: 'bank' },
])

const orderOption = ref([
  { name: '내림차순', code: 'desc' },
  { name: '오름차순', code: 'asc' },
])

// 은행 목록 추출
const banks = computed(() => [...new Set(rawData.value.map((d) => d.bank.name))])

// 데이터 로딩
onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/products/savings/')
  rawData.value = res.data

  // 은행 셀렉션 컴포넌트 - 은행 리스트 설정
  banksOption.value = banks.value.map((d) => {
    return {
      name: d,
      code: d,
    }
  })
  await accountStore.fetchScraps()
})

// 필터/정렬된 리스트
const filteredList = computed(() => {
  let list = rawData.value

  if (keyword.value) {
    list = list.filter((item) => item.name.includes(keyword.value))
  }
  if (selectedBank.value.name) {
    list = list.filter((item) => item.bank.name === selectedBank.value.name)
  }
  list = list.filter((item) => getMaxRate(item) >= minRate.value)

  switch (selectedSortKey.value.code) {
    case 'rate':
      return list.slice().sort((a, b) => {
        const cmp = getMaxRate(b) - getMaxRate(a)
        return selectedSortOrder.value.code === 'asc' ? -cmp : cmp
      })
    case 'term':
      return list.slice().sort((a, b) => {
        const cmp = getMaxTerm(b) - getMaxTerm(a)
        return selectedSortOrder.value.code === 'asc' ? -cmp : cmp
      })
    case 'bank':
      return list.slice().sort((a, b) => {
        const cmp = a.bank.name.localeCompare(b.bank.name)
        return selectedSortOrder.value.code === 'asc' ? cmp : -cmp
      })
    default:
      return list
  }
})

// 최고 금리 반환
function getMaxRate(item) {
  return Math.max(...(item.options || []).map((opt) => opt.intr_rate2 || 0)).toFixed(2)
}

// 최고 금리 옵션(객체) 반환
function getMaxRateOption(item) {
  const options = item.options || []
  if (!options.length) return null
  const maxRate = Math.max(...options.map((opt) => opt.intr_rate2 || 0))
  return options.find((opt) => opt.intr_rate2 === maxRate)
}

// 최대 기간 반환
function getMaxTerm(item) {
  return Math.max(...(item.options || []).map((opt) => Number(opt.save_trm) || 0))
}

// 스크랩 여부 확인
function isScrapped(item) {
  return scraps.value.some((s) => s.saving?.id === item.id)
}

// 스크랩 추가/취소
async function toggleScrap(item) {
  const scrap = scraps.value.find((s) => s.saving?.id === item.id)
  if (scrap) {
    await axios.delete(`http://127.0.0.1:8000/api/products/scraps/${scrap.id}/`, {
      headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
    })
  } else {
    await axios.post(
      'http://127.0.0.1:8000/api/products/scraps/',
      {
        saving_id: item.id,
      },
      {
        headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
      },
    )
  }
  await accountStore.fetchScraps()
}
</script>
<style scoped></style>
