<script setup>
import { ref } from "vue"
import ChatFriendList from "@/views/chat/chat_filed/components/chat_friend_info_list/ChatFriendList.vue";
import ChatGroupList from "@/views/chat/chat_filed/components/chat_friend_info_list/ChatGroupList.vue";

const active = ref("friend")
</script>

<template>
  <div class="flex text-sm border-b">
    <button
      class="flex-1 py-2"
      :class="active==='friend' ? 'text-green-500 border-b-2 border-green-500' : ''"
      @click="active='friend'"
    >
      好友
    </button>

    <button
      class="flex-1 py-2"
      :class="active==='group' ? 'text-green-500 border-b-2 border-green-500' : ''"
      @click="active='group'"
    >
      群聊
    </button>
  </div>
  <ChatFriendList v-if="active==='friend'" class="flex-1 overflow-y-auto" />
  <ChatGroupList v-else-if="active==='group'"/>
</template>

<style scoped>

</style>