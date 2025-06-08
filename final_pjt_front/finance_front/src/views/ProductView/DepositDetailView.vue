<!-- 툴팁 띄우기 위해 최상단에 sticky속성 필요해서(relative가 아닌 어떤 속성이든) 우선 삽입하였음. 추후 수정 필요. -->
<template>
  <div v-if="deposit" class="container mx-auto pt-28 pb-20 sticky">
    <router-link :to="{ name: 'products_deposit' }" class="text-sm text-gray-600 hover:underline">
      ← 예금 상품 목록으로 돌아가기
    </router-link>

    <div class="flex justify-between items-start mt-4">
      <div>
        <h2 class="text-3xl font-bold mb-1">{{ deposit.name }}</h2>
        <p class="text-gray-500 mb-4">{{ deposit.bank.name }}</p>
      </div>
      <div class="text-right">
        <p class="text-red-500 text-2xl font-bold">{{ getMaxRate(deposit) }}%</p>
        <p class="text-sm text-gray-500">연 기본금리</p>
        <button
          v-if="isLogin"
          @click="toggleScrap"
          class="mt-2 px-4 py-2 rounded bg-black text-white hover:bg-gray-800"
        >
          <span v-if="isScrapped">스크랩됨</span>
          <span v-else>스크랩하기</span>
        </button>
      </div>
    </div>

    <!-- 금리 차트 -->
    <div class="mt-6">
      <h3 class="font-semibold text-lg mb-2">📈 금리 차트</h3>
      <canvas id="rateChart" class="w-full max-w-2xl mx-auto"></canvas>
    </div>

    <!-- 금리 옵션 테이블 -->
    <div class="mt-6">
      <h3 class="font-semibold text-lg mb-2">📊 기간별 금리</h3>
      <table class="table-auto w-full border">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-2 py-1">기간 (개월)</th>
            <th class="border px-2 py-1">기본 금리</th>
            <th class="border px-2 py-1">최고 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="opt in deposit.options" :key="opt.id">
            <td class="border px-2 py-1">{{ opt.save_trm }}</td>
            <td class="border px-2 py-1">{{ opt.intr_rate.toFixed(2) }}%</td>
            <td class="border px-2 py-1">{{ opt.intr_rate2.toFixed(2) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 상품 기본 정보 -->
    <div class="bg-white border rounded-lg p-6 mt-6">
      <h3 class="text-lg font-semibold mb-4">ℹ️ 상품 기본 정보</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <p class="text-sm text-gray-500 mb-1">취급 은행</p>
          <p class="text-base">{{ deposit.bank.name }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 mb-1">금리 정보</p>
          <p class="text-base">
            세전 {{ getMaxRate(deposit) }}% / 세후 {{ (getMaxRate(deposit) * 0.845).toFixed(2) }}%
          </p>
        </div>
        <div>
          <p class="text-sm text-gray-500 mb-1">가입 기간</p>
          <p class="text-base">{{ getMaxTerm(deposit) }}개월</p>
        </div>
      </div>
    </div>

    <!-- 수익 시뮬레이션 -->
    <div class="border rounded-lg p-6 mt-6">
      <h3 class="font-semibold mb-4">수익 시뮬레이션</h3>
      <div class="mb-4">
        <label class="text-sm mr-2">예치 금액을 입력하세요:</label>
        <input
          v-model.number="principal"
          type="number"
          step="10000"
          class="border rounded px-2 py-1 w-48"
          placeholder="예: 1000000"
        />
      </div>
      <div class="grid grid-cols-3 text-center">
        <div>
          <p class="text-sm text-gray-500">원금</p>
          <p class="text-xl font-bold">{{ formatCurrency(principal) }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">예상 이자</p>
          <p class="text-xl font-bold text-green-600">
            +{{ formatCurrency(getEstimatedInterest()) }}
          </p>
        </div>
        <div>
          <p class="text-sm text-gray-500">만기 수령액</p>
          <p class="text-xl font-bold">{{ formatCurrency(principal + getEstimatedInterest()) }}</p>
        </div>
      </div>
      <p class="text-xs text-gray-400 mt-2">
        * 위 계산은 세전 기준이며, 실제 수령액은 세금 등을 고려하여 달라질 수 있습니다.
      </p>
    </div>

    <!-- 유의사항 -->
    <div class="border rounded-lg p-4 mt-6">
      <h3 class="font-semibold mb-2">유의사항</h3>
      <ul class="list-disc list-inside text-sm text-gray-600 space-y-1">
        <li>예금자보호법에 따라 예금보험공사가 보호합니다.</li>
        <li>중도해지 시 약정금리보다 낮은 금리가 적용될 수 있습니다.</li>
        <li>금리는 시장 상황에 따라 변동될 수 있습니다.</li>
        <li>자세한 내용은 상품설명서를 참고하시기 바랍니다.</li>
      </ul>
    </div>
  </div>
  <div v-else class="text-center py-20 text-gray-500">로딩 중...</div>
</template>

<script setup>
import {
  ref,
  onMounted,
  computed,
  nextTick,
  reactive,
  onBeforeUnmount,
  onUnmounted,
  watch,
} from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { storeToRefs } from 'pinia'
import { Chart, registerables } from 'chart.js'
import TextBlockTooltip from '@/components/TextBlockTooltip.vue'
Chart.register(...registerables)

const route = useRoute()
const deposit = ref(null)
const principal = ref(1000000)
const accountStore = useAccountStore()
const { scraps, isLogin } = storeToRefs(accountStore)

onMounted(async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/products/deposits/${route.params.id}/`)
    deposit.value = res.data
    if (isLogin.value) {
      await accountStore.fetchScraps()
    }
    await nextTick()
    drawChart()
  } catch (error) {
    console.error('예금 상세 정보 조회 실패:', error)
  }
})

function drawChart() {
  if (!deposit.value || !Array.isArray(deposit.value.options)) return
  const ctx = document.getElementById('rateChart')
  if (!ctx) return
  const labels = deposit.value.options.map((opt) => `${opt.save_trm}개월`)
  const data = deposit.value.options.map((opt) => opt.intr_rate2)
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: '최고 금리 (%)',
          data,
          backgroundColor: '#3b82f6',
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return value + '%'
            },
          },
        },
      },
    },
  })
}

const isScrapped = computed(() => {
  if (!deposit.value) return false
  return scraps.value.some((s) => s.deposit?.id === deposit.value.id)
})

async function toggleScrap() {
  if (!deposit.value) return
  const scrap = scraps.value.find((s) => s.deposit?.id === deposit.value.id)
  try {
    if (scrap) {
      await axios.delete(`http://127.0.0.1:8000/api/products/scraps/${scrap.id}/`, {
        headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
      })
    } else {
      await axios.post(
        'http://127.0.0.1:8000/api/products/scraps/',
        {
          deposit_id: deposit.value.id,
        },
        {
          headers: { Authorization: `Token ${localStorage.getItem('access_token')}` },
        },
      )
    }
    await accountStore.fetchScraps()
  } catch (error) {
    alert('스크랩 처리에 실패했습니다.')
    console.error(error)
  }
}

function getMaxRate(item) {
  return Math.max(...(item.options || []).map((opt) => opt.intr_rate2 || 0)).toFixed(2)
}
function getMaxTerm(item) {
  return Math.max(...(item.options || []).map((opt) => Number(opt.save_trm) || 0))
}
function getEstimatedInterest() {
  if (!deposit.value || !deposit.value.options?.length) return 0
  const options = deposit.value.options
  const maxRate = Math.max(...options.map((opt) => opt.intr_rate2 || 0))
  const maxOpt = options.find((opt) => opt.intr_rate2 === maxRate)
  if (!maxOpt) return 0
  const rate = maxRate / 100
  const months = Number(maxOpt.save_trm)
  return Math.round(principal.value * rate * (months / 12))
}
function formatCurrency(amount) {
  if (!Number.isFinite(amount)) return '-'
  return amount.toLocaleString('ko-KR', { style: 'currency', currency: 'KRW' })
}
</script>

<style scoped></style>
