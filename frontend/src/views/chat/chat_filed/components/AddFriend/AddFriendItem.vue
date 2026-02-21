<script setup>
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
import {useChatStore} from "@/stores/chat.js";
import {ref} from "vue";

const props = defineProps(['user_friend'])
const emit = defineEmits(['added'])
const user = useUserStore()
const chat = useChatStore()
const is_Add = ref(props.user_friend.is_friend)
async function handelAdd(){
    if (is_Add.value){
      alert("已添加");
      return
    }
    try {
      const res = await api.post('api/friend/add_friend/',{
        friend_id: props.user_friend.id,
        id:user.id
      })
      const data = res.data
      if (data.result === "success"){
        chat.addNewFriend(data.friend_data)
        chat.selectFriend(data.friend_data)

        alert("添加成功！")
        emit('added')
        is_Add.value = true
      }else {
      alert("添加失败");
    }
    }catch (e){

    }
}
</script>

<template>
<div @click="handelAdd" class="flex flex-col items-center w-28 cursor-pointer hover:scale-105 transition">

    <img
      :src="user_friend.photo"
      class="w-20 h-20 rounded-full object-cover border"
      alt=""
    />

    <div class="mt-2 text-sm text-center truncate w-full">
      {{ user_friend.username }}
    </div>

    <div v-if="is_Add" class="left-4 right-4 top-54 text-black line-clamp-4 break-all">
      <span>已添加</span>
    </div>
    <div v-else class="left-4 right-4 top-54 text-black line-clamp-4 break-all">
      <span>添加好友</span>
    </div>

</div>
</template>

<style scoped>

</style>