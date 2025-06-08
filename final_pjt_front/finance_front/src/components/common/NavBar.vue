<template>
  <nav class="bg-white border-b border-gray-200 relative z-50 p-2">
    <!-- 로고 -->
    <div class="flex items-center h-16 max-w-7xl mx-auto px-4">
  <router-link to="/" class="text-4xl text-black italic font-bold" style="font-family: 'Libre Bodoni', serif;">
    Faind
  </router-link>

      <!-- 상위 메뉴 -->
      <div class="flex-1 flex justify-center">
        <ul class="flex gap-12 h-full items-center relative">
          <li
            v-for="item in menuItems"
            :key="item.label"
            class="relative group"
          >
            <span class="font-medium text-base px-2 py-2 cursor-pointer hover:text-gray-700 whitespace-nowrap">
              {{ item.label }}
            </span>

            <!-- 드롭다운 -->
            <ul
              v-if="item.children && item.children.length"
              class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 bg-white border border-gray-200 rounded shadow-md opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity duration-150 z-50 min-w-[140px]"
            >
              <li v-for="child in item.children" :key="child.label">
                <router-link
                  :to="child.route || '#'"
                  class="block py-2 px-4 text-gray-700 hover:bg-gray-100 text-sm text-center"
                >
                  {{ child.label }}
                </router-link>
              </li>
            </ul>
          </li>
        </ul>
      </div>

      <!-- 우측 버튼 -->
      <div class="flex gap-2">
        <template v-if="!account.isLogin">
          <button class="border rounded px-4 py-2 text-black-700 font-medium hover:bg-gray-100" @click="goLogin">
            로그인
          </button>
          <button class="bg-black text-white rounded px-4 py-2 font-medium hover:bg-gray-800" @click="goSignup">
            회원가입
          </button>
        </template>
        <template v-else>
          <button class="border rounded px-4 py-2 text-black-700 font-medium hover:bg-gray-100" @click="goProfile">
            마이페이지
          </button>
          <button class="bg-black text-white rounded px-4 py-2 font-medium hover:bg-gray-800" @click="handleLogout">
            로그아웃
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const account = useAccountStore()

const goLogin = () => router.push({ name: 'login' })
const goSignup = () => router.push({ name: 'signup' })
const goProfile = () => router.push({ name: 'profile' })
const handleLogout = () => {
  account.logOut()
  router.push({ name: 'home' })
}

const menuItems = [
  {
    label: '금융 상품 조회',
    children: [
      { label: '예금', route: '/product/deposit' },
      { label: '적금', route: '/product/saving' },
    ]
  },
  {
    label: '주식 종목 검색',
    children: [
      { label: '국내 주식', route: '/stocks' },
    ]
  },
  {
    label: '재태크피드',
    children: [
      { label: '자유게시판', route: '/community' },
      { label: '금융 인사이트', route: '/articles' },
    ]
  },
  {
    label: '고객지원',
    children: [
      { label: '서비스 소개', route: '/support/description' },
      { label: '주변 은행 찾기', route: '/support/branches' },
    ]
  }
]
</script>
