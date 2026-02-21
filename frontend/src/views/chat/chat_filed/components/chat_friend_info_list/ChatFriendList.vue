<script setup>
import { ref } from "vue"
import {useChatStore} from "@/stores/chat.js";

const chat = useChatStore()

</script>

<template>
   <div class="divide-y divide-base-300">
    <div
      v-for="friend in chat.friends"
      :key="friend.id"
      @click="chat.selectFriend(friend)"
      :class="['flex items-center gap-3 px-4 py-3 hover:bg-base-300 cursor-pointer transition',
                chat.activeChat?.id === friend.id ? 'bg-base-300' : '']"
    >
      <img :src="friend.photo" class="w-10 h-10 rounded-full" alt=""/>
      <div class="flex-1 min-w-0">
        <div class="flex justify-between text-sm font-medium">
          <span class="truncate">{{ friend.username }}</span>
          <span class="text-xs text-gray-400">{{ friend.time }}</span>
        </div>
        <div class="text-xs text-gray-500 truncate">{{ friend.lastMsg }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>