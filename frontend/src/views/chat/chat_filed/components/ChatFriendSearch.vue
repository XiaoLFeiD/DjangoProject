<script setup>

import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import AddIcon from "@/components/navbar/icons/AddIcon.vue";
import {ref, useTemplateRef} from "vue";
import ChatFriendAdd from "@/views/chat/chat_filed/components/AddFriend/ChatFriendAdd.vue";


const searchKey = ref('')
import { useUserStore } from "@/stores/user";
const userStore = useUserStore();

const friendAddRef = useTemplateRef('friend-add-ref')

async function handleSearch(){
  friendAddRef.value.showModal()
}
</script>

<template>
  <div class="p-3 flex gap-2 border-b">

    <input
      v-model="searchKey"
      class="input input-sm flex-1"
      placeholder="搜索用户ID/昵称"
    />
    <button class="btn btn-sm btn-square">
      <SearchIcon />
    </button>
    <button @click="handleSearch" class="btn btn-sm btn-square">
      <AddIcon />
    </button>
  </div>
    <ChatFriendAdd :key="userStore.id" ref="friend-add-ref"/>
</template>

<style scoped>

</style>