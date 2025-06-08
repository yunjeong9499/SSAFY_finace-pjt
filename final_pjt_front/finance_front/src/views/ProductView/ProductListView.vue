<template>
  <div class="pt-28 pb-20 px-4 max-w-7xl mx-auto">
    <h1 class="text-4xl font-bold text-center mb-2">금융 조회 상품 <span class="text-black">서비스</span></h1>
    <p class="text-center text-gray-500 mb-12">
      당신의 재정 목표와 상황에 맞는 최적의 금융 상품을 찾아보세요. 저희의 맞춤형 추천 서비스가 현명한 금융 결정을 도와드립니다.
    </p>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 예금 카드 -->
      <div class="border rounded-lg p-6 shadow hover:shadow-lg transition">
        <div class="flex items-center mb-4">
          <span class="text-3xl mr-2">🐷</span>
          <div>
            <h2 class="text-xl font-semibold">예금</h2>
            <p class="text-gray-500 text-sm pt-2">안정적인 수익을 원하는 분들을 위한 상품</p>
          </div>
        </div>
        <!-- <ul class="text-sm text-gray-600 mb-6 space-y-1">
          <li>금리: <strong class="text-black">연 3.5%</strong></li>
          <li>기간: <strong class="text-black">12개월</strong></li>
          <li>최소 금액: <strong class="text-black">100만원</strong></li>
        </ul> -->
        <div class="pt-8">
            <router-link
              to="/product/deposit"
              class="block w-full text-center bg-black text-white py-2 rounded hover:bg-gray-800 transition"
            >
              상세 정보 보기 →
            </router-link>
        </div>
      </div>

      <!-- 적금 카드 -->
      <div class="border rounded-lg p-6 shadow hover:shadow-lg transition">
        <div class="flex items-center mb-4">
          <span class="text-3xl mr-2">📦</span>
          <div>
            <h2 class="text-xl font-semibold">적금</h2>
            <p class="text-gray-500 text-sm pt-2">매월 일정액을 저축하여 목표를 달성하세요</p>
          </div>
        </div>
        <!-- <ul class="text-sm text-gray-600 mb-6 space-y-1">
          <li>금리: <strong class="text-black">연 4.0%</strong></li>
          <li>기간: <strong class="text-black">24개월</strong></li>
          <li>월 납입액: <strong class="text-black">10만원 이상</strong></li>
        </ul> -->
        <div class="pt-8">
            <router-link
              to="/product/saving"
              class="block w-full text-center bg-black text-white py-2 rounded hover:bg-gray-800 transition"
            >
              상세 정보 보기 →
            </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
