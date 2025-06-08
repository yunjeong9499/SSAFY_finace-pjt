import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios' // ← 꼭 추가!

export const useChatbotStore = defineStore('chatbot', () => {
  // state
  const isOpen = ref(false)
  const chatStage = ref('welcome')
  const messages = ref([])
  const userInput = ref('')
  const form = ref({ age: '', job: '', interest: '' })
  const formDetails = ref({ purpose: '', period: '', amount: '' })
  // const formDetails = ref()
  const isLoading = ref(false)

  // actions
  function openChatbot() {
    isOpen.value = true
    if (chatStage.value == 'dict') {
      return
    }
    chatStage.value = 'welcome'
    messages.value = [{ role: 'assistant', content: '안녕하세요. 무엇을 도와드릴까요?' }]
  }
  function closeChatbot() {
    isOpen.value = false
  }
  function goBack() {
    chatStage.value = 'welcome'
    userInput.value = ''
  }
  function selectRecommendation() {
    chatStage.value = 'recommend-form'
  }
  function selectFreePrompt() {
    chatStage.value = 'free'
    messages.value = [
      { role: 'assistant', content: '무엇이든 물어보세요! 예: 적금과 예금의 차이는?' },
    ]
  }
  const postPrompt = async (param) => {
    isLoading.value = true // 시작 시 로딩 ON
    // messages.value.push({ role: 'user', content: `${age} ${job}, 관심사: ${interest}` })
    try {
      console.log('param: ', param)
      const { data } = await axios.post('http://localhost:8000/api/chat/', param)
      console.log(data)
      isLoading.value = false
      messages.value.push({ role: 'assistant', content: data.reply, mode: data.mode })
      chatStage.value = 'chat'
    } catch {
      messages.value.push({ role: 'assistant', content: '❗ 추천 중 오류가 발생했습니다.!' })
    }
    form.value = { age: '', job: '', interest: '' }
  }

  // … sendPrompt, sendFreePrompt 등 기존 로직도 여기로 옮겨주세요

  return {
    // state
    isOpen,
    chatStage,
    messages,
    userInput,
    form,
    isLoading,
    formDetails,
    // actions
    openChatbot,
    closeChatbot,
    goBack,
    selectRecommendation,
    selectFreePrompt,
    postPrompt,
    // (sendPrompt, sendFreePrompt 등)
  }
})
