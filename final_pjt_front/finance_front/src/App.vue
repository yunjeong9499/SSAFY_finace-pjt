<template>
  <div class="layout-wrapper">
    <header>
      <NavBar />
    </header>
    <main class="main-content max-w-screen-xl my-0 mx-auto">
      <div ref="textContainer" @mouseup="handleSelection">
        <RouterView />
      </div>
      <Chatbot />
      <TextBlockTooltip
        :visible="showTooltip"
        :left="tooltipPos.left"
        :top="tooltipPos.top"
        @translate="translate"
      />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, onBeforeUnmount } from 'vue'
import { storeToRefs } from 'pinia'
import NavBar from '@/components/common/NavBar.vue'
import Chatbot from './components/Chatbot.vue'
import TextBlockTooltip from '@/components/TextBlockTooltip.vue'
import Footer from '@/components/common/Footer.vue'

// 툴팁 기능
import { useChatbotStore } from '@/stores/chatbot'
const chatbot = useChatbotStore()
const { chatStage } = storeToRefs(chatbot)

const showTooltip = ref(false)
const tooltipPos = reactive({ left: 0, top: 0 })
const textContainer = ref(null)
const TOOLTIP_OFFSET_X = 8
const TOOLTIP_OFFSET_Y = 8
const selectedText = ref(null)

function handleSelection() {
  const selection = window.getSelection()
  if (selection && selection.rangeCount > 0) {
    const range = selection.getRangeAt(0)
    selectedText.value = selection.toString()
    if (!range.collapsed && textContainer.value.contains(selection.anchorNode)) {
      const rect = range.getBoundingClientRect()
      const containerRect = textContainer.value.getBoundingClientRect()
      tooltipPos.left = rect.right - containerRect.left + TOOLTIP_OFFSET_X
      tooltipPos.top = rect.bottom - containerRect.top + TOOLTIP_OFFSET_Y
      showTooltip.value = true
      return
    }
  }
  showTooltip.value = false
}

function handleScroll() {
  showTooltip.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

function translate() {
  chatStage.value = 'dict'
  chatbot.openChatbot()
  chatbot.postPrompt({
    text: selectedText.value,
    mode: 'dict',
  })
  showTooltip.value = false
}
</script>

<style scoped>
/* Flexbox 기반 레이아웃 */
.layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 메인 콘텐츠가 남은 공간을 모두 차지하게 함 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  min-width: 960px;
}

/* 푸터 스타일 예시 (필요에 따라 조정) */
footer {
  background: #f8f9fa;
  color: #333;
  padding: 16px 0;
  text-align: center;
  font-size: 14px;
}

/* 추천 챗봇 플로팅 버튼 등 */
.recommend-bot-float {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 50;
}
</style>
