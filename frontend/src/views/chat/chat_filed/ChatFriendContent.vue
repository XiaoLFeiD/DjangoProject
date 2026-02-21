<script setup>
import {nextTick, ref, watch} from 'vue'
import {useChatStore} from "@/stores/chat.js";
import {useUserStore} from "@/stores/user.js";

const chat = useChatStore()
const user = useUserStore()
const messageText = ref("")
const scrollRef = ref(null)
const textareaRef = ref(null) // 用于操作光标位置

// 控制表情面板显示
const showEmojiPicker = ref(false)

// 常用表情列表
const emojis = [
  "😊", "😂", "🤣", "😍", "😘", "🙌", "👍", "👌", "🤔", "🙄",
  "😎", "😭", "😡", "🥳", "✨", "🎉", "🔥", "❤️", "💔", "🙏",
  "👀", "🌟", "🎈", "🍔", "🍦", "🌈", "💻", "🎨", "🚀", "🌙"
]

// 插入表情到光标位置
const addEmoji = (emoji) => {
  const el = textareaRef.value

  if (!el) {
    messageText.value += emoji;
    showEmojiPicker.value = false; // 即使没找到元素也关闭面板
    return;
  }

  const start = el.selectionStart
  const end = el.selectionEnd
  const text = messageText.value

  // 在光标处切开字符串并插入表情
  messageText.value = text.substring(0, start) + emoji + text.substring(end)

  //选择完表情后关闭面板
  showEmojiPicker.value = false

  // 重新聚焦并把光标移到表情后面
  nextTick(() => {
    el.focus()
    const newCursorPos = start + emoji.length
    el.setSelectionRange(newCursorPos, newCursorPos)
  })
}

// 点击外部关闭面板 (可选优化)
const toggleEmoji = (e) => {
  e.stopPropagation()
  showEmojiPicker.value = !showEmojiPicker.value
}


// 自动滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (scrollRef.value) {
      scrollRef.value.scrollTop = scrollRef.value.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动
watch(() => chat.messages.length, scrollToBottom)

// 模拟发送消息
const handleSend = () => {
  if (!messageText.value.trim()) return
  chat.sendMessage(messageText.value)
  messageText.value = ""
}

</script>

<template>
  <div class="h-full overflow-hidden">
      <!-- 如果选中了好友，显示聊天框 -->
  <div v-if="chat.activeChat" class="flex flex-col h-full bg-white">
    <!-- 头部：好友名 -->
    <div class="h-14 border-b flex items-center px-6">
      <h2 class="text-lg font-bold text-gray-800">{{ chat.activeChat.username }}</h2>
    </div>

    <!-- 中间：消息列表 -->
    <div ref="scrollRef" class="flex-1 overflow-y-auto p-4 bg-[#f3f3f3] space-y-4">
      <div v-for="msg in chat.messages" :key="msg.id"
           :class="['flex', msg.sender_id === user.id ? 'flex-row-reverse' : 'flex-row']">

           <!-- 头像展示 -->
          <img
            :src="msg.sender_id === user.id ? user.photo : chat.activeChat.photo"
            class="w-9 h-9 rounded-full object-cover shrink-0 shadow-sm"
            alt=""
          />

        <!-- 消息气泡 -->
        <div :class="['max-w-[70%] px-3 py-2 rounded-lg text-sm shadow-sm',
                     msg.sender_id === user.id ? 'bg-[#95ec69] text-black' : 'bg-white text-black']">
          {{ msg.content }}
        </div>
      </div>
    </div>

    <!-- 底部：输入框 -->
    <div class="h-44 border-t flex flex-col relative bg-white">
          <!-- 表情面板 (绝对定位在工具栏上方) -->
      <div v-if="showEmojiPicker"
           class="absolute bottom-44 left-4 w-64 h-48 bg-white shadow-xl border rounded-lg p-2 overflow-y-auto grid grid-cols-6 gap-2 z-50">
        <button
          v-for="emoji in emojis"
          :key="emoji"
          @click="addEmoji(emoji)"
          class="hover:bg-gray-100 p-1 rounded text-xl transition"
        >
          {{ emoji }}
        </button>
      </div>

      <div class="flex items-center px-4 py-2 gap-4 text-gray-500 text-xl shrink-0">
        <button @click="toggleEmoji" class="hover:text-primary transition">😊</button>
      </div>

      <textarea
        ref="textareaRef"
        v-model="messageText"
        @keyup.enter.exact.prevent="handleSend"
        class="flex-1 w-full px-4 py-2 resize-none outline-none border-none bg-transparent"
        placeholder="请输入消息..."
      ></textarea>

      <div class="flex justify-end p-3">
        <button @click="handleSend" class="btn btn-sm px-5">发送(S)</button>
      </div>
    </div>
  </div>

  <!-- 如果没选中，显示占位图 -->
  <div v-else class="flex flex-col items-center justify-center h-full bg-gray-50 text-gray-400">
     <svg class="w-20 h-20 mb-4 opacity-20" fill="currentColor" viewBox="0 0 20 20">
       <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
       <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.59.233.918.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
     </svg>
     <p>未选择聊天</p>
  </div>
  </div>
</template>

<style scoped>

</style>