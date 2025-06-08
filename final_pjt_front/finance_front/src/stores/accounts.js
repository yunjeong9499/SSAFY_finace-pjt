import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
  // 상태 변수
  const token = ref(localStorage.getItem('access_token'))
  const userInfo = ref({})
  const scraps = ref([])
  const USER_API_URL = 'http://127.0.0.1:8000/api/auth'
  const router = useRouter()

  // Axios 기본 설정
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
  }

  // 계산 속성
  const isLogin = computed(() => !!token.value)

  // 액션 메서드
  const signUp = async (payload) => {
    try {
      await axios.post(`${USER_API_URL}/signup/`, payload, {
        headers: { 'Content-Type': 'application/json' }
      })
    } catch (error) {
      throw error.response?.data || error.message
    }
  }

  const logIn = async (payload) => {
    try {
      const res = await axios.post(`${USER_API_URL}/login/`, payload)
      token.value = res.data.key
      localStorage.setItem('access_token', token.value)
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
      router.push({ name: 'home' })
    } catch (error) {
      throw error.response?.data || error.message
    }
  }

  const logOut = () => {
    token.value = null
    userInfo.value = {}
    localStorage.removeItem('access_token')
    delete axios.defaults.headers.common['Authorization']
  }

  const userProfile = async () => {
    if (!token.value) throw new Error('토큰 없음')
    const res = await axios.get('http://127.0.0.1:8000/api/auth/user/')
    userInfo.value = res.data
    return res.data
  }

  const updateProfile = async (formData) => {
    try {
      const res = await axios.patch(`${USER_API_URL}/user/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      userInfo.value = res.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }

  const changePassword = async (payload) => {
    try {
      await axios.post(`${USER_API_URL}/password/change/`, {
        old_password: payload.oldpassword,
        new_password1: payload.newpassword1,
        new_password2: payload.newpassword2
      })
    } catch (error) {
      throw error.response?.data || error.message
    }
  }

  const deleteAccount = async () => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/auth/delete/`)
      logOut()
    } catch (error) {
      throw error.response?.data || error.message
    }
  }

  const fetchScraps = async () => {
    const res = await axios.get('http://127.0.0.1:8000/api/products/scraps/', {
      headers: { Authorization: `Token ${localStorage.getItem('access_token')}` }
    })
    scraps.value = res.data
  }
  const setScraps = (data) => {
    scraps.value = data
  }

  const removeScrap = async (scrapId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/products/scraps/${scrapId}/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      await fetchScraps() // 해제 후 목록 갱신
    } catch (error) {
      console.error('스크랩 해제 실패:', error.response?.data || error.message)
      alert('스크랩 해제 중 오류가 발생했습니다.')
    }
  }

  return {
    // 상태
    token,
    userInfo,
    scraps,
    
    // 계산 속성
    isLogin,
    
    // 액션
    signUp,
    logIn,
    logOut,
    userProfile,
    updateProfile,
    changePassword,
    deleteAccount,
    fetchScraps,
    setScraps,
    removeScrap
  }
}, { persist: true })

