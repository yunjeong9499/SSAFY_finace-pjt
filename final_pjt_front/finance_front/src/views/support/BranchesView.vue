<template>
  <div class="d-flex px-12 pb-20">
    <div class="mb-20 pt-28">
      <h1 class="text-5xl font-bold mb-5">주변 은행 찾기</h1>
      <p class="text-xl text-gray-600 pt-2">
        현재 위치를 기반으로 가까운 은행과 ATM을 쉽게 찾아보세요.<br />
        <!-- 영업시간, 제공 서비스 등의 상세 정보도 확인할 수 있습니다. -->
      </p>
    </div>

    <div class="flex flex-column gap-4 pt-0 pb-28">
      <div class="basis-2/4 border-solid border border-gray-300 rounded py-6 px-6">
        <div class="flex items-center justify-between mb-1">
          <p class="text-xl font-bold">검색 필터</p>
          <Button
            icon="pi pi-compass"
            @click="searchByMyLocation"
            size="small"
            severity="secondary"
          ></Button>
        </div>
        <p class="text-base mb-6 text-zinc-500">원하는 조건으로 검색하세요</p>
        <div class="mb-5">
          <label for="region" class="block mb-1">광역시/도</label>
          <Dropdown id="region" v-model="selectedRegion" :options="regionOptions" />
        </div>
        <div class="mb-5">
          <label for="district" class="block mb-1">시/군/구</label>
          <Dropdown v-model="selectedDistrict" :options="districtOptions" />
        </div>
        <div class="mb-5">
          <label for="bank" class="block mb-1">은행</label>
          <Dropdown
            id="bank"
            v-model="selectedBank"
            :options="bankOptions"
            v-if="bankOptions.length"
          />
        </div>
        <Button @click="searchBanks" class="ml-auto w-full mt-14" :full="true" size="lg"
          >찾기</Button
        >
      </div>
      <div class="w-full min-h-[500px] max-h-[800px]">
        <div id="map" style="width: 100%; height: 100%"></div>
      </div>
    </div>

    <section class="py-0 bg-white font-sans text-black">
      <div class="max-w-7xl mx-auto px-4">
        <!-- 섹션 제목 -->
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold mb-2">은행 방문 전 알아두세요</h2>
          <p class="text-gray-600 text-base">은행 방문 시 필요한 정보와 팁을 확인하세요.</p>
        </div>

        <!-- 카드 3개 그리드 -->
        <div class="grid gap-6 md:grid-cols-3">
          <!-- 카드 1 -->
          <Card class="font-sans text-black border border-gray-300 rounded-lg shadow-sm p-6">
            <template #title>
              <div class="text-xl font-semibold text-black text-center">영업 시간 안내</div>
            </template>
            <template #content>
              <p class="text-base text-black">
                대부분의 은행은<br />
                평일 09:00부터 16:00까지 영업합니다.<br />
                주말과 공휴일에는 영업하지 않으니 참고하세요.
              </p>
            </template>
          </Card>

          <!-- 카드 2 -->
          <Card class="font-sans text-black border border-gray-300 rounded-lg shadow-sm p-6">
            <template #title>
              <div class="text-xl font-semibold text-black text-center">필요 서류</div>
            </template>
            <template #content>
              <p class="text-base text-black">
                계좌 개설, 대출 신청 등 은행 업무 시<br />
                신분증은 필수입니다.<br />
                업무에 따라 추가 서류가 필요할 수 있으니<br />
                미리 확인하세요.
              </p>
            </template>
          </Card>

          <!-- 카드 3 -->
          <Card class="font-sans text-black border border-gray-300 rounded-lg shadow-sm p-6">
            <template #title>
              <div class="text-xl font-semibold text-black text-center">ATM 이용 안내</div>
            </template>
            <template #content>
              <p class="text-base text-black">
                ATM은 대부분 24시간 이용 가능하며,<br />
                타행 ATM 이용 시 수수료가 발생할 수 있습니다.<br />
                은행별 수수료 정책을 확인하세요.
              </p>
            </template>
          </Card>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import mapData from '@/data/data.json'
import Dropdown from '@/components/common/Dropdown.vue'
import Button from 'primevue/button'
// import Button from '@/components/common/Button.vue'
import Card from 'primevue/card'

function transformMapInfo(mapInfo) {
  const regionOptions = mapInfo.map((region) => ({
    label: region.name,
    value: region.name,
    icon: '',
  }))

  const districtMap = {}
  for (const region of mapInfo) {
    districtMap[region.name] = region.countries.map((district) => ({
      label: district,
      value: district,
      icon: '',
    }))
  }

  return {
    regionOptions,
    districtMap,
  }
}

// 변환된 데이터 구조
const { regionOptions, districtMap } = transformMapInfo(mapData.mapInfo)

const districtOptions = ref([])
const bankOptions = ref([])

const selectedRegion = ref(null)
const selectedDistrict = ref(null)
const selectedBank = ref(null)

// 은행 데이터 변환
const rawBanks = mapData.bankInfo
bankOptions.value = rawBanks.map((bank) => ({
  label: bank,
  value: bank,
  icon: '',
}))

// 연동 로직
watch(selectedRegion, (newRegion) => {
  districtOptions.value = newRegion ? districtMap[newRegion] || [] : []
  selectedDistrict.value = null
  selectedBank.value = null
})

watch(selectedDistrict, () => {
  selectedBank.value = null
})

watch(selectedBank, (bank) => {
  console.log('선택한 은행:', bank)
})

// 지도 연동하기 기능
// env 확인
// const KAKAO_MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY
// const MOBILITY_API_KEY = import.meta.env.VITE_MOBILITY_API_KEY
// if (!KAKAO_MAP_API_KEY)
//   console.error('VITE_KAKAO_MAP_API_KEY is not defined. Check .env file and restart server.')
// if (!MOBILITY_API_KEY)
//   console.error('VITE_MOBILITY_API_KEY is not defined. Check .env file and restart server.')

const provinceData = ref([])
const districts = ref([])
const bankList = ref([])

const selectedProvince = ref('')
// const selectedDistrict = ref('')
// const selectedBank = ref('')
const showInfo = ref(false)

let map,
  ps,
  infowindow,
  markers = [],
  currentPolyline = null

function initMap() {
  map = new kakao.maps.Map(document.getElementById('map'), {
    center: new kakao.maps.LatLng(37.49818, 127.027386),
    level: 3,
  })
  ps = new kakao.maps.services.Places()
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
}

onMounted(() => {
  // 초기 데이터 세팅
  const json = mapData
  provinceData.value = json.mapInfo
  bankList.value = json.bankInfo

  if (window.kakao && window.kakao.maps) {
    initMap()
  } else {
    console.error(
      'kakao.maps is not defined. Ensure the SDK script is included in index.html and loaded before Vue.',
    )
  }
})

function onProvinceChange() {
  const found = provinceData.value.find((p) => p.name === selectedProvince.value)
  districts.value = found?.countries || []
  selectedDistrict.value = ''
}

function clearMarkers() {
  markers.forEach((m) => m.setMap(null))
  markers = []
}

function clearPolyline() {
  if (currentPolyline) {
    currentPolyline.setMap(null)
    currentPolyline = null
  }
}

function searchBanks() {
  if (!selectedRegion.value || !selectedDistrict.value || !selectedBank.value) {
    alert('모든 항목을 선택해주세요.')
    return
  }
  clearMarkers()
  clearPolyline()
  showInfo.value = false
  const keyword = `${selectedRegion.value} ${selectedDistrict.value} ${selectedBank.value}`
  // const keyword = `${selectedProvince.value} ${selectedDistrict.value} ${selectedBank.value}`
  ps.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds()
      data.forEach((place) => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        bounds.extend(position)
        const marker = new kakao.maps.Marker({ map, position })
        markers.push(marker)
        kakao.maps.event.addListener(marker, 'click', () => {
          infowindow.setContent(
            `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`,
          )
          infowindow.open(map, marker)
          // drawRouteTo(place.y, place.x) // 경로 표시 기능 삭제
        })
      })
      map.setBounds(bounds)
      showInfo.value = true
    } else {
      alert('검색 결과가 없습니다.')
    }
  })
}
function searchByMyLocation() {
  if (!navigator.geolocation) {
    alert('브라우저가 위치 정보를 지원하지 않습니다.')
    return
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude

      const locPosition = new kakao.maps.LatLng(lat, lng)
      map.setCenter(locPosition)

      clearMarkers()
      clearPolyline()
      showInfo.value = false

      const radius = 3000 // 3km 반경
      const keyword = selectedBank.value || '은행'

      ps.categorySearch(
        'BK9',
        (places, status) => {
          if (status === kakao.maps.services.Status.OK) {
            const bounds = new kakao.maps.LatLngBounds()
            places.forEach((place) => {
              const placePosition = new kakao.maps.LatLng(place.y, place.x)
              bounds.extend(placePosition)
              const marker = new kakao.maps.Marker({ map, position: placePosition })
              markers.push(marker)

              kakao.maps.event.addListener(marker, 'click', () => {
                infowindow.setContent(
                  `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`,
                )
                infowindow.open(map, marker)
              })
            })
            map.setBounds(bounds)
            showInfo.value = true
          } else {
            alert('주변 은행을 찾을 수 없습니다.')
          }
        },
        {
          location: locPosition,
          radius: radius,
          useMapBounds: false,
        },
      )
    },
    (error) => {
      console.error(error)
      alert('위치 정보를 가져올 수 없습니다.')
    },
  )
}
</script>

<style scoped>
#info-box {
  position: absolute;
  margin-bottom: 80px;
  top: 10px;
  left: 10px;
  z-index: 10;
  background-color: #f5f5f5;
  padding: 10px 15px;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
