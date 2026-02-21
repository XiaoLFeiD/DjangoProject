<script setup>

import {ref, watch} from "vue";
import AddFriendItem from "@/views/chat/chat_filed/components/AddFriend/AddFriendItem.vue";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";

const emit = defineEmits(['close'])
const users = ref([])
const searchKey = ref('')
const user = useUserStore()

async function handleSearch(){
    const keyword = searchKey.value.trim()

    // 如果为空，直接清空列表
    if (!keyword) {
      users.value = []
      return
    }
    try {
      const res = await api.get('api/friend/search_list/',{
        params:{
          keyword: searchKey.value.trim(),
          id: user.id
        }
      })
    const data = res.data
    if (data.result === 'success') {
      users.value = data.all_users
    }
    }catch (e){
    }
}

watch(searchKey,async (newVal)=>{
  const keyword = newVal.trim()
  if (!keyword){
    users.value = []
    return
  }
  await handleSearch()
})

</script>

<template>
<div class="flex items-center justify-center mt-5">
   <span class="text-bg text-xl font-bold">找人</span>
</div>
<div class="flex justify-center mt-6 top-30 left-4 h-12 ">
<label class="input input-lg w-110">
  <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g
      stroke-linejoin="round"
      stroke-linecap="round"
      stroke-width="2.5"
      fill="none"
      stroke="currentColor"
    >
      <circle cx="11" cy="11" r="8"></circle>
      <path d="m21 21-4.3-4.3"></path>
    </g>
  </svg>
  <input v-model="searchKey" @keyup.enter="handleSearch" type="search" required placeholder="Search" />
</label>
</div>
<div class="flex flex-col items-center mb-12">
  <div class="grid grid-cols-[repeat(auto-fill,minmax(120px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
    <AddFriendItem
        v-for="user_friend in users"
        :key="user_friend.id"
        :user_friend="user_friend"
        @added="emit('close')"
    />
  </div>
</div>
</template>

<style scoped>

</style>