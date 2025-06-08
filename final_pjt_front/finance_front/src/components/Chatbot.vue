<template>
  <div class="recommend-chat-float">
    <transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0 translate-y-5"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-5"
    >
      <div v-if="isOpen" class="chatbot-container z-10">
        <div class="flex items-center justify-between bg-black text-white font-bold py-3 px-4">
          <!-- 왼쪽 그룹: 뒤로가기 + 제목 -->
          <div class="flex items-center space-x-2">
            <button
              type="button"
              @click="goBack"
              class="text-white text-xl bg-transparent border-none pr-2"
            >
              <i class="pi pi-chevron-left"></i>
            </button>
            <span>스크래미</span>
          </div>

          <!-- 오른쪽: 닫기 버튼 -->
          <button
            type="button"
            @click="chatbot.closeChatbot()"
            class="text-white text-xl bg-transparent border-none p-0"
          >
            <i class="pi pi-times"></i>
          </button>
        </div>

        <!-- 메시지 영역 -->
        <div class="chatbot-body space-y-3 text-sm" ref="chatBody">
          <div v-if="chatStage === 'welcome'" class="flex items-start space-x-2">
            <!-- 1) 좌측 챗봇 아이콘 -->
            <img :src="chatbotIcon" alt="챗봇 아이콘" class="w-8 h-8 rounded-full flex-shrink-0" />
            <div class="w-full">
              <p class="bubble-assistant">안녕하세요. 무엇을 도와드릴까요?</p>
              <div class="flex gap-2 mt-2">
                <button
                  @click="selectRecommendation"
                  class="flex items-center gap-2 border rounded-full px-3 py-2 hover:bg-gray-100"
                >
                  💡 상품 추천받기
                </button>
                <button
                  @click="selectFreePrompt"
                  class="flex items-center gap-2 border rounded-full px-3 py-2 hover:bg-gray-100"
                >
                  📝 질문하기
                </button>
              </div>
            </div>
          </div>

          <div
            v-else-if="chatStage === 'recommend-form'"
            class="flex flex-col h-full space-y-2 justify-between"
          >
            <div>
              <!-- 연령대 -->
              <Select
                v-model="form.age"
                placeholder="연령대 선택하기"
                :options="ageOptionsObj"
                optionLabel="label"
                optionValue="value"
                class="w-full mb-2"
                appendTo="self"
              ></Select>
              <!-- 직업 -->
              <Select
                v-model="form.job"
                placeholder="직업 선택하기"
                :options="jobOptionsObj"
                optionLabel="label"
                optionValue="value"
                class="w-full mb-2"
                appendTo="self"
              ></Select>
              <!-- 관심사 -->
              <Select
                v-model="form.interest"
                placeholder="관심사 선택하기"
                :options="interestOptionsObj"
                optionLabel="label"
                optionValue="value"
                class="w-full mb-2"
                appendTo="self"
              ></Select>
              <!-- 로딩 중일 때 skeleton -->
              <div v-if="isLoading" class="flex mb-4">
                <!-- <Skeleton size="5rem"></Skeleton> -->
                <!-- <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton> -->
                <div>
                  <Skeleton width="18rem" height="5rem" class="mb-2"></Skeleton>
                  <Skeleton width="15rem" class="mb-2"></Skeleton>
                  <Skeleton width="5rem" class="mb-2"></Skeleton>
                </div>
              </div>
            </div>
            <Button @click="sendPrompt" class="mt-auto bg-black text-white w-full h-12 rounded">
              <span>추천받기</span>
            </Button>
          </div>

          <div v-else>
            <div v-for="(msg, i) in messages" :key="i" class="mb-4">
              <div v-if="msg.role === 'user'" class="text-right">
                <span class="bubble-user">{{ msg.content }}</span>
              </div>

              <div v-else class="flex items-start space-x-2">
                <!-- 1) 좌측 챗봇 아이콘 -->
                <img
                  :src="chatbotIcon"
                  alt="챗봇 아이콘"
                  class="w-8 h-8 rounded-full flex-shrink-0"
                />

                <!-- 2) 내용 (카드형 or 일반 텍스트) -->
                <div class="text-left flex-1">
                  <!-- 📦 카드 형식 응답인 경우 -->
                  <template v-if="'mode' in msg && msg.mode == 'recommend-form'">
                    <div v-for="(card, idx) in parseCards(msg.content)" :key="idx">
                      <div
                        class="border rounded-lg p-3 mb-2 bg-gray-50 shadow cursor-pointer hover:bg-gray-100"
                        @click="goToDetail(card)"
                      >
                        <p class="font-bold text-sm mb-1">{{ card.title }}</p>
                        <p
                          class="text-xs text-gray-700 whitespace-pre-line"
                          v-html="highlightImportant(card.description)"
                        ></p>
                      </div>
                    </div>

                    <Button
                      v-if="!isCompletedSurvey"
                      size="small"
                      @click="surveyDetail"
                      :disabled="isCompletedSurvey"
                      >추가 설문하기</Button
                    >
                    <div
                      v-else-if="chatStage === 'recommend-form'"
                      class="flex flex-col h-full space-y-2 justify-between"
                    >
                      <div>
                        <!-- 연령대 -->
                        <Select
                          v-model="form.age"
                          placeholder="연령대 선택하기"
                          :options="ageOptionsObj"
                          optionLabel="label"
                          optionValue="value"
                          class="w-full mb-2"
                          appendTo="self"
                        ></Select>
                        <!-- 직업 -->
                        <Select
                          v-model="form.job"
                          placeholder="직업 선택하기"
                          :options="jobOptionsObj"
                          optionLabel="label"
                          optionValue="value"
                          class="w-full mb-2"
                          appendTo="self"
                        ></Select>
                        <!-- 관심사 -->
                        <Select
                          v-model="form.interest"
                          placeholder="관심사 선택하기"
                          :options="interestOptionsObj"
                          optionLabel="label"
                          optionValue="value"
                          class="w-full mb-2"
                          appendTo="self"
                        ></Select>
                      </div>
                      <Button
                        @click="sendPrompt"
                        class="mt-auto bg-black text-white w-full h-12 rounded"
                        >추천받기</Button
                      >
                    </div>

                    <div
                      v-if="chatStage == 'recommend-form-detail'"
                      class="flex flex-col h-full space-y-2 justify-between mt-8"
                    >
                      <!-- 5번 질문 -->
                      <div>
                        <p class="font-semibold mb-2">추가 설문을 진행해주세요</p>
                        <!-- <p class="font-semibold">🎯 5. 예적금을 드는 목적은 무엇인가요?</p> -->
                        <Select
                          v-model="formDetails.purpose"
                          :options="purposeOptionsObj"
                          optionLabel="label"
                          optionValue="value"
                          placeholder="목적 선택"
                          class="w-full mb-2"
                          appendTo="self"
                        ></Select>

                        <!-- 6번 질문 -->
                        <!-- <p class="font-semibold">
                            ⏱️ 6. 자금을 어느 정도 기간 동안 모으고 싶나요?
                          </p> -->
                        <Select
                          v-model="formDetails.period"
                          :options="periodOptionsObj"
                          optionLabel="label"
                          optionValue="value"
                          placeholder="기간 선택"
                          class="w-full mb-2"
                          appendTo="self"
                        ></Select>

                        <!-- 7번 질문 -->
                        <!-- <p class="font-semibold">💸 7. 매달 저축 가능한 금액은 얼마나 되나요?</p> -->
                        <Select
                          v-model="formDetails.amount"
                          :options="amountOptionsObj"
                          optionLabel="label"
                          optionValue="value"
                          placeholder="금액 선택"
                          class="w-full mb-2"
                          appendTo="self"
                        ></Select>
                      </div>

                      <Button v-if="!isCompletedSurvey" @click="submitSurvey">완료</Button>
                    </div>
                  </template>
                  <!-- 💬 일반 텍스트 응답인 경우 -->
                  <template v-else>
                    <span
                      class="bubble-assistant whitespace-pre-line"
                      v-html="highlightBold(msg.content)"
                    ></span>
                  </template>
                </div>
              </div>
            </div>
            <!-- 로딩 중일 때 skeleton -->
            <div v-if="isLoading" class="flex">
              <div v-for="n in 3" :key="n" class="mb-3">
                <!-- width/height는 필요에 맞게 조정 -->
                <Skeleton shape="circle" size="0.5rem" class="mr-0.5" />
              </div>
            </div>
          </div>
        </div>

        <!-- 입력창 (모든 화면에서 하단 고정) -->
        <form
          v-if="chatStage === 'free'"
          @submit.prevent="sendFreePrompt"
          class="chatbot-footer h-16"
        >
          <input v-model="userInput" class="chatbot-input" placeholder="메시지를 입력해주세요" />
          <button type="submit" class="chatbot-send">
            <i class="pi pi-search"></i>
          </button>
        </form>
      </div>
    </transition>
    <!-- 챗봇 열기 버튼 -->
    <button
      v-if="!isOpen"
      @click="chatbot.openChatbot()"
      class="fixed bottom-6 right-6 z-50 chatbot-x-button"
    >
      💬 챗봇 열기
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick, watch, computed, reactive } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Select from 'primevue/select'
import Skeleton from 'primevue/skeleton'
import Button from 'primevue/button'
import chatbotIcon from '@/assets/imgs/img_chatbot.png'

const router = useRouter()

const chatBody = ref(null) // chatBody 엘리먼트 참조
const isCompletedSurvey = ref(false)
const chatbot = useChatbotStore()
// +// reactive한 state만 뽑아 쓰고, action은 chatbot.openChatbot() 형태로 호출
const { isOpen, chatStage, messages, userInput, form, formDetails, isLoading } =
  storeToRefs(chatbot)

const ageOptions = ['20대', '30대', '40대', '50대 이상']
const jobOptions = ['직장인', '프리랜서', '공무원', '학생', '자영업자']
const interestOptions = ['안정적인 자산관리', '고수익 투자', '단기 예금', '장기 적금']

// 추가 설문용 reactive 객체
// const formDetails = reactive({
//   purpose: '',
//   period: '',
//   amount: '',
// })

// 각 옵션 배열
const purposeOptions = ['비상금 마련', '여행/가전 등 단기 목표', '자산 형성 (내 집 마련, 결혼 등)']
const periodOptions = ['6개월 미만', '6개월 ~ 1년', '1년 ~ 3년', '3년 이상']
const amountOptions = ['10만 원 이하', '10~30만 원', '30~50만 원', '50만 원 이상']

// Select에 넘길 { label, value } 형태로 변환
const purposeOptionsObj = computed(() => purposeOptions.map((v) => ({ label: v, value: v })))
const periodOptionsObj = computed(() => periodOptions.map((v) => ({ label: v, value: v })))
const amountOptionsObj = computed(() => amountOptions.map((v) => ({ label: v, value: v })))

// Select 에 넘길 { label, value } 배열로 변환
const ageOptionsObj = computed(() => ageOptions.map((item) => ({ label: item, value: item })))
const jobOptionsObj = computed(() => jobOptions.map((item) => ({ label: item, value: item })))
const interestOptionsObj = computed(() =>
  interestOptions.map((item) => ({ label: item, value: item })),
)

// const openChatbot = () => {
//   isOpen.value = true
//   chatStage.value = 'welcome'
//   messages.value = [{ role: 'assistant', content: '안녕하세요. 무엇을 도와드릴까요?' }]
// }
const goBack = () => {
  chatStage.value = 'welcome'
  userInput.value = ''
}
const goNextSurvey = () => {}
const selectRecommendation = () => {
  chatStage.value = 'recommend-form'
  form.value = { age: '', job: '', interest: '' } //
}
const selectFreePrompt = () => {
  chatStage.value = 'free'
  messages.value = [
    { role: 'assistant', content: '무엇이든 물어보세요! \n예) 적금과 예금의 차이가 뭐야?' },
  ]
}
const msg = { age: '30대', job: '공무원', interest: '단기 예금' }
// parameter: mode: "default" || "free_text" || "dict"
const sendPrompt = async (param) => {
  if (!param.hasOwnProperty('purpose')) {
    // 추가 설문 아닌 경우, 즉 초기설문단계. [fix]조건 명확히 수정 필요
    isCompletedSurvey.value = false
  }

  isLoading.value = true // 시작 시 로딩 ON
  const { age, job, interest } = form.value
  let content = `${age} ${job}, 관심사: ${interest}`
  if ('purpose' in param) {
    const { purpose, period, amount } = param
    content = `${content}, 목적: ${purpose}, 기간: ${period}, 매달: ${amount}`
  }
  messages.value.push({ role: 'user', content: content })
  try {
    const { data } = await axios.post('http://localhost:8000/api/chat/', {
      age,
      job,
      interest,
      ...param,
    })
    isLoading.value = false
    messages.value.push({ role: 'assistant', content: data.reply, mode: data.mode }) // mode로 이후에 카드인지 구분한다.
    chatStage.value = 'chat'
  } catch {
    messages.value.push({ role: 'assistant', content: '❗ 추천 중 오류가 발생했습니다.' })
  }
  // form.value = { age: '', job: '', interest: '' }
}
const sendFreePrompt = async () => {
  if (!userInput.value.trim()) return
  isLoading.value = true // 시작 시 로딩 ON
  messages.value.push({ role: 'user', content: userInput.value })
  try {
    const { data } = await axios.post('http://localhost:8000/api/chat/', {
      free_text: userInput.value,
      mode: 'free_text',
    })
    isLoading.value = false
    messages.value.push({ role: 'assistant', content: data.reply, mode: data.mode })
  } catch {
    messages.value.push({ role: 'assistant', content: '❗ 오류가 발생했습니다.' })
  }
  userInput.value = ''
}

const parseCards = (text) => {
  return text
    .split(/\n(?=\d+\.\s)/)
    .map((chunk, idx) => {
      const lines = chunk.trim().split('\n')
      const titleLine = lines[0] || ''
      const title = titleLine.replace(/^\d+\.\s*/, '')
      const typeLine = lines.find((line) => line.includes('상품유형='))
      const type = typeLine?.split('=')[1]?.trim() || 'deposit'
      const idLine = lines.find((line) => line.includes('productId='))
      const id = idLine?.split('=')[1]?.trim()
      const rawDescription = lines
        .filter((l) => l !== titleLine) // 제목 줄 제외
        .join('\n')
        .trim()
      const description = rawDescription.replace(/productId=\d+/g, '').trim()

      return {
        id,
        type,
        title: `${idx + 1}. ${title}`,
        description,
      }
    })
    .filter((card) => card.id && card.title && card.description)
}

const submitSurvey = () => {
  isCompletedSurvey.value = true
  sendPrompt(formDetails.value)
}

const surveyDetail = () => {
  chatStage.value = 'recommend-form-detail'
  // isCompletedSurvey.value = true
  // messages.value.push({ role: 'assistant', content: 'userInput.value' })
}

const goToDetail = (card) => {
  if (!card?.id) return
  const base = card.type === 'saving' ? 'savings' : 'deposits'
  router.push(`/${base}/${Number(card.id)}`)
}

const isStructuredResponse = (text) => {
  // 예: "1. 상품명 ..." 형식으로 시작하는 응답일 때 true
  return /\d+\.\s.+/g.test(text)
}

const highlightImportant = (text) => {
  return text
    .replace(/(\d+\.?\d*%)|(\d+개월)/g, '<span class="text-red-500 font-semibold">$&</span>') // 퍼센트, 개월 강조
    .replace(/(금리|기간)/g, '<strong>$&</strong>') // 금리, 기간 텍스트 강조
}

const highlightBold = (text) => {
  // **강조할 텍스트** 패턴을 찾아 <span>으로 감싸줍니다.
  return text.replace(/\*\*(.+?)\*\*/g, '<span class="font-semibold text-blue-500">$1</span>')
}

// 2) messages 배열이 바뀔 때마다(새 메시지 푸시될 때) 스크롤 아래로
// watch(messages, async () => {
//   // DOM 업데이트가 끝날 때까지 기다렸다가
//   await nextTick()
//   const el = chatBody.value
//   console.log(el)
//   if (el) {
//     // 스크롤을 맨 아래로
//     el.scrollTop = el.scrollHeight
//     console.log('EL')
//   }
// })
</script>

<style scoped>
.recommend-chat-float {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 999;
}
.chatbot-container {
  display: flex;
  flex-direction: column;
  height: 36rem;
  width: 24rem;
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
.chatbot-header {
  background-color: #000000;
  color: white;
  font-weight: bold;
  padding: 0.75rem 1rem;
  display: flex;
  /* justify-content: space-between; */
  align-items: center;
}
.chatbot-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #ffffff;
  overflow-y: scroll;
  /* Firefox */
  scrollbar-width: none;
  /* IE, Edge */
  -ms-overflow-style: none;
}
/* 스크롤바 안보이게 하기 */
.chatbot-body::-webkit-scrollbar {
  width: 0;
  height: 0;
}
.chatbot-footer {
  /* border-top: 1px solid #e5e5e5; */
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: white;
}
.chatbot-input {
  flex: 1;
  border: 1px solid #ccc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}
.chatbot-send {
  background-color: #000000;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}
.chatbot-x-button {
  background-color: #000000;
  color: white;
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
.bubble-assistant {
  background-color: #f3f4f6;
  color: #111827;
  padding: 0.5rem 0.75rem;
  border-radius: 1rem;
  max-width: 80%;
  display: inline-block;
  text-align: left;
  white-space: pre-line;
}
.bubble-user {
  background-color: white;
  color: #111827;
  padding: 0.5rem 0.75rem;
  border-radius: 1rem;
  max-width: 80%;
  display: inline-block;
  text-align: left; /* ✅ 왼쪽 정렬로 변경 */
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}
</style>
