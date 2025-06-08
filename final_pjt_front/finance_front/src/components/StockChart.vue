<template>
  <div class="rounded-lg border bg-card shadow-sm mt-5 mb-5 p-6 transition-all">
    <div class="flex justify-between">
      <div class="flex flex-col">
        <h2 class="text-3xl font-medium">
          {{ stockName }}
        </h2>
        <span> {{ fetchedData[0]?.srtnCd }} </span>
      </div>
      <div class="flex flex-col">
        <p class="text-3xl font-bold" v-if="fetchedData[0]?.clpr">
          {{ Number(fetchedData[0]?.clpr).toLocaleString('ko-KR') }}원
        </p>
        <p
          class="ml-auto mr-0 text-xl"
          :class="{
            'text-red-500': diff > 0,
            'text-blue-500': diff < 0,
          }"
        >
          {{ diff > 0 ? '+' : '' }}
          {{ diff.toLocaleString('ko-KR') }}원
        </p>
      </div>
    </div>
    <div class="mt-5 flex justify-between items-center">
  <!-- 왼쪽: 기간 선택 -->
  <SelectButton
    v-model="mode"
    :options="options"
    optionLabel="name"
    optionValue="code"
  />

  <!-- 오른쪽: 그래프 타입 선택 -->
  <SelectButton
    v-model="chartType"
    :options="[
      { label: '꺾은선 그래프', value: 'line' },
      { label: '막대 그래프', value: 'bar' },
    ]"
    optionLabel="label"
    optionValue="value"
  />
</div>

    <Line v-if="chartType === 'line'" :data="chartData" :options="chartOptions" class="h-80" />
    <Bar v-else :data="chartData" :options="chartOptions" class="h-80"/>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Line, Bar } from 'vue-chartjs'
import { getPriceByUnit } from '@/api/stocksService'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  TimeScale,
} from 'chart.js'
import 'chartjs-adapter-date-fns'
import SelectButton from 'primevue/selectbutton'

const options = [
  { name: '월별', code: 'monthly' },
  { name: '주별', code: 'weekly' },
  { name: '일별', code: 'daily' },
]

const props = defineProps({
  stockName: {
    type: String,
    required: true,
  },
})

const route = useRouter()

// Chart.js 모듈 등록
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  TimeScale,
)
const mode = ref('monthly')
const fetchedData = ref([])

// 상태 선언
const chartData = ref({
  labels: [], // Date 객체 배열 또는 ISO 문자열 배열
  datasets: [
    {
      label: '종가',
      data: [], // 숫자 배열
      tension: 0.1,
      fill: false,
      borderColor: '#38bdf8',      // 하늘색 선 (ex. sky-400)
      backgroundColor: '#bae6fd',  // 점 색상 or 클릭 영역 배경
      pointBackgroundColor: '#38bdf8', // 점도 하늘색
    },
  ],
})

const chartOptions = ref({
  responsive: true,
  scales: {
    x: { type: 'time', time: { unit: 'day',  displayFormats: {day: 'M월 d일',}, } },
    y: { beginAtZero: false },
  },
})

const diff = computed(() => {
  const a = Number(fetchedData?.value?.[0]?.clpr ?? 0)
  const b = Number(fetchedData?.value?.[1]?.clpr ?? 0)
  return a - b
})

const chartType = ref('line') // 그래프 타입 선택 

async function fetchChart(name) {
  try {
    // [todo] 모든 하나의 차트에 모든 값을 보여줘야 하므로, 가능한 큰 수로 count를 임의로 설정하였음.
    const res = await getPriceByUnit({
      unit: mode.value,
      count: 10000,
      itmsNm: `${props.stockName}`,
    })
    fetchedData.value = res.items?.item
    const raw = res.items?.item || []
    // console.log('raw')
    // console.log(raw)
    const processed = raw
    // console.log(processed[0])

    // API 호출 후...
    const dates = processed.map((p) => p.basDt)
    const prices = processed.map((p) => p.clpr)
    // console.log(dates)
    // console.log(prices)
    chartData.value = {
      labels: dates,
      datasets: [
        {
          label: `${props.stockName} 종가`,
          data: prices,
          tension: 0.1,
          fill: false,
          borderColor: '#38bdf8',      // 하늘색 선 (ex. sky-400)
          backgroundColor: '#bae6fd',  // 점 색상 or 클릭 영역 배경
          pointBackgroundColor: '#38bdf8', // 점도 하늘색
        },
      ],
    }
    // console.log(chartData.value)
  } catch (e) {
    console.error(e)
  }
}

// 예: 마운트 시 데이터 채우기
onMounted(async () => {
  if (props.stockName) fetchChart(props.stockName)
})

// 모드 변경 시 재호출
watch(mode, fetchChart)

// prop이 바뀔 때마다 차트 재로딩
watch(
  () => props.stockName,
  (newName) => {
    if (newName) fetchChart(newName)
  },
)
</script>
