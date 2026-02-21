<script setup>

import {onBeforeUnmount, onMounted, useTemplateRef, watch} from "vue";
import ChatFriendNavbar from "@/views/chat/chat_filed/ChatFriendNavbar.vue";
import ChatFriendContent from "@/views/chat/chat_filed/ChatFriendContent.vue";
import ChatFriendInfo from "@/views/chat/chat_filed/ChatFriendInfo.vue";
import {useChatStore} from "@/stores/chat.js";
import {useUserStore} from "@/stores/user.js";
import api from "@/js/http/api.js";

const modalRef = useTemplateRef('chat-modal-ref')
const chat = useChatStore()
let isDragging = false
let offsetX = 0
let offsetY = 0

function showModal(){
  modalRef.value.showModal()
  modalRef.value.style.left = "300px"
  modalRef.value.style.top = "100px"
  //刷新好友列表
  chat.fetchFriendsFromServer();

  //如果当前已经选中了某个好友，顺便刷新他的历史消息
  if (chat.activeChat) {
      chat.selectFriend(chat.activeChat);
  }
}

function closeModal(){
  modalRef.value.close()
}

function startDrag(e) {
  if (e.button !== 0) return

  const dialog = modalRef.value

  isDragging = true
  offsetX = e.clientX - dialog.offsetLeft
  offsetY = e.clientY - dialog.offsetTop
}

function handleMouseMove(e) {
  if (!isDragging) return

  const dialog = modalRef.value

  dialog.style.left = e.clientX - offsetX + "px"
  dialog.style.top = e.clientY - offsetY + "px"
}

function stopDrag() {
  isDragging = false
}


defineExpose({
  showModal,
  closeModal
})

const userStore = useUserStore();

// 提取初始化逻辑为一个函数
async function initializeChat() {
  if (userStore.accessToken) {
    // 如果没有 id，先拉取用户信息
    if (!userStore.id) {
        try {
            const res = await api.get('/api/user/account/get_user_info/')
            if(res.data.result === 'success'){
                userStore.setUserInfo(res.data)
            }
        } catch(e) { console.error(e); }
    }

    // 有了 ID 后，开始拉取好友和连 WS
    if (userStore.id) {
      await chat.fetchFriendsFromServer();
      await chat.initWebSocket();
    }
  }
}

onMounted(async ()=>{
  document.addEventListener("mousemove", handleMouseMove)
  document.addEventListener("mouseup", stopDrag)

  // 尝试初始化（针对刷新页面已经登录的情况）
  await initializeChat();
})

watch(async () => userStore.id, async (newId) => {
  if (newId) {
    console.log("检测到登录，开始连接...");
    await initializeChat();
  }
})

onBeforeUnmount(() => {
  document.removeEventListener("mousemove", handleMouseMove)
  document.removeEventListener("mouseup", stopDrag)
})
</script>

<template>
  <dialog ref="chat-modal-ref" class="fixed m-0 p-0 bg-transparent border-none">
    <div class="w-[800px] h-[600px] bg-base-100 shadow-2xl rounded-xl overflow-hidden flex flex-col">
      <ChatFriendNavbar @close="closeModal" @start_dialog="startDrag"/>
      <div class="flex flex-1 overflow-hidden">
        <ChatFriendInfo />
        <ChatFriendContent class="flex-1" />
      </div>
    </div>
  </dialog>
</template>

<style scoped>
dialog::backdrop {
  background: none;
}
</style>