<template>
  <div class="container mx-auto pt-28">
    <h1 class="text-4xl font-bold mb-4">주식 현재가</h1>
    <div class="text-gray-500 mb-12"></div>
    <div class="rounded-lg border bg-card shadow-sm p-6 flex gap-2 mb-2">
      <div className="relative flex-1">
        <h2 class="text-3xl font-semibold mb-2 text-gray-600">주식 종목 검색</h2>
        <p class="text-ml text-gray-500 mb-4">보유 자산을 입력하여 구매 가능한 주식 수를 계산하세요</p>
        <form @submit.prevent="onSubmit" class="flex w-full mb-8">
          <InputText
            type="text"
            v-model="stockName"
            class="flex-1 mr-2 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
          ></InputText>
          <Button
            type="submit"
            label="검색"
            class="flex-shrink-0 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
          ></Button>
        </form>
        <div className="border-t pt-4">
          <div className="mb-3">
            <h3 className="text-sm text-gray-600 mb-2">
              검색 결과
              <span v-if="pageInfo.totalRecords > 0"> ({{ pageInfo.totalRecords }}개) </span>
            </h3>
            <div
              v-for="(stock, idx) in stocksList"
              :key="idx"
              :class="[
                'group flex items-center justify-between p-2 cursor-pointer rounded-md',
                searchKeyword === stock.itmsNm ? 'bg-gray-100' : 'hover:bg-gray-50',
              ]"
              @click="fetchChart(stock)"
            >
              <div class="flex items-center gap-3">
                <div
                  :class="[
                    'w-2 h-2 rounded-full transition-colors',
                    searchKeyword === stock.itmsNm ? 'bg-zinc-950' : 'bg-gray-300',
                  ]"
                ></div>

                <div>
                  <span
                    :class="[
                      'font-medium text-sm transition-colors',
                      searchKeyword === stock.itmsNm ? 'text-primary' : 'ring-red-500',
                    ]"
                  >
                    {{ stock.itmsNm }}
                  </span>
                  <span
                    :class="[
                      'text-xs ml-2',
                      searchKeyword === stock.itmsNm ? 'text-primary/70' : 'text-muted-foreground',
                    ]"
                  >
                    {{ stock.srtnCd }}
                  </span>
                </div>
              </div>
            </div>

            
            <Paginator
            :first="(pageInfo.page - 1) * pageInfo.rows"
            :rows="pageInfo.rows"
            :totalRecords="pageInfo.totalRecords"
            :pageLinkSize="5"
            @page="onPageChange"
            class="mt-4"
            />
        </div>
    </div>
</div>
</div>
<div ref="chartRef" class="mt-16">
    <StockChart v-if="searchKeyword" :stock-name="searchKeyword" />
</div>
<!-- 매수 가능 계산기 -->
  <Card v-if="selectedPrice" class="mt-16">
    <template #title >
        <h2 class="text-3xl font-semibold mb-2 text-gray-600">투자 계산기</h2>       
              </template>
              <template #content>
                <p class="text-ml text-gray-500 mb-4">
                  보유 자산을 입력하여 구매 가능한 주식 수를 계산하세요
                </p>

                <label class="block text-sm font-medium text-gray-700 mb-1">보유 자산 (원)</label>
                <div class="flex items-center mb-4">
                  <span class="px-3 py-2 border border-r-0 border-gray-300 bg-gray-50 text-gray-500 rounded-l-md">
                    ₩
                  </span>
                  <input
                    v-model.number="myCash"
                    type="number"
                    step="100000"
                    placeholder="0"
                    class="w-1/2 border border-gray-300 px-3 py-2 rounded-r-md focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>

                <div v-if="myCash" class="space-y-2">
                  <div class="bg-green-50 px-4 py-2 rounded-md text-green-800 font-semibold">
                    구매 가능 주식 수: {{ possibleShares }}주
                  </div>
                  <div class="bg-blue-50 px-4 py-2 rounded-md text-blue-700">
                    투자 금액: ₩{{ (selectedPrice * possibleShares).toLocaleString() }}
                  </div>
                  <div class="bg-gray-100 px-4 py-2 rounded-md text-gray-700">
                    잔여 금액: ₩{{ (myCash - selectedPrice * possibleShares).toLocaleString() }}
                  </div>

                  <!-- <div class="border border-gray-300 rounded-md p-4 mt-8">
                    <div><strong>종목:</strong> {{ searchKeyword }}</div><br>
                    <div><strong>주당 가격:</strong> ₩{{ selectedPrice.toLocaleString() }}</div><br>
                    <div><strong>보유 자산:</strong> ₩{{ myCash.toLocaleString() }}</div><br>
                    <div><strong>구매 가능:</strong> {{ possibleShares }}주</div>
                  </div> -->
                  <div class="mt-2 flex justify-end">
                      <Button label="초기화" class="mt-4 bg-gray-200 text-black" @click="resetCalculator" />
                  </div>
                </div>
              </template>
            </Card>
            </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import StockChart from '@/components/StockChart.vue'
import { fetchData, getStocksList } from '@/api/stocksService'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Paginator from 'primevue/paginator'

const pageInfo = ref({
  page: 1,
  rows: 3,
  totalRecords: 0,
})

const stocksList = ref([])
const stockName = ref('')
const searchKeyword = ref('')
const selectedPrice = ref(null)
const myCash = ref(0)

const onSubmit = function () {
  fetchStocksList()
}
const chartRef = ref(null)

async function fetchChart(stock) {
  searchKeyword.value = stock.itmsNm
  selectedPrice.value = parseFloat(stock.clpr)
  console.log('선택된 종가:', selectedPrice.value)
  nextTick(() => {
    if (chartRef.value) {
      chartRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

async function onPageChange(event) {
  pageInfo.value.page = event.page + 1
  pageInfo.value.rows = event.rows
  await fetchStocksList()
}

async function fetchStocksList() {
  try {
    const { page, rows } = pageInfo.value
    const res = await getStocksList({
      basDt: '20250522',
      likeItmsNm: stockName.value,
      pageNo: page,
      numOfRows: rows,
    })

    stocksList.value = res?.items?.item
    pageInfo.value.totalRecords = res.totalCount
  } catch (e) {
    console.error(e)
  }
}
const possibleShares = computed(() => {
  if (!selectedPrice.value || !myCash.value) return 0
  return Math.floor(myCash.value / selectedPrice.value)
})

function resetCalculator() {
  myCash.value = 0
  selectedPrice.value = null
  searchKeyword.value = ''
}
</script>

<style scoped>
body {
  padding-top: 64px;
}
</style>