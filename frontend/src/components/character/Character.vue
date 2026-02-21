<script setup>
import {ref, useTemplateRef} from "vue";
import UpdateIcon from "@/views/user/space/components/icons/UpdateIcon.vue";
import DeleteIcon from "@/views/user/space/components/icons/DeleteIcon.vue";
import {useUserStore} from "@/stores/user.js";
import api from "@/js/http/api.js";
import ChatField from "@/components/character/chat_field/ChatField.vue";
import {useRouter} from "vue-router";

const props = defineProps(['character', 'canEdit', 'aiFriendId', 'canRemoveFriend'])
const emit = defineEmits(['remove'])
const isHover = ref(false)
const user = useUserStore()
const router = useRouter()


async function handleRemoveCharacter() {
  try {
    const res = await api.post('/api/create/character/remove/', {
      'character_id': props.character.id,
    })
    if (res.data.result === 'success') {
      emit('remove', props.character.id)
    }
  } catch (err) {
  }
}

async function handleRemoveFriend() {
  try {
    const res = await api.post('/api/ai_friend/remove/', {
      'ai_friend_id': props.aiFriendId,
    })
    if (res.data.result === 'success') {
      emit('remove', props.aiFriendId)
    }
  } catch (err) {
  }
}


const charFiledRef = useTemplateRef('chat-filed-ref')
const ai_friend = ref(null)
async function openChatFiled(){
  if(!user.isLogin()){
   await router.push({
      name:'user-account-login-index',
    })
  }else{
    try {
      const res = await api.post('api/ai_friend/get_or_create/',
          {
              'character_id':props.character.id,
          })
      const data = res.data
      if(data.result === 'success'){
        ai_friend.value = data.ai_friend
        charFiledRef.value.showModal()
      }
    }catch (e){

    }
  }
}

</script>

<template>
<div>
  <div class="avatar cursor-pointer" @mouseout="isHover=false" @mouseover="isHover=true" @click="openChatFiled">
    <div class="w-60 h-100 rounded-2xl relative">
      <img :src="props.character.background_image"  class="transition-transform duration-300" :class="{'scale-120':isHover}" alt="">
       <div class="absolute left-0 top-50 w-60 h-50 bg-linear-to-t from-black/40 to-transparent"></div>
      <div v-if="canEdit && character.author.user_id === user.id" class="absolute right-0 top-48">
          <RouterLink @click.stop :to="{name: 'create-character-update-index', params: {character_id: character.id}}" class="btn btn-circle btn-ghost bg-transparent">
            <UpdateIcon />
          </RouterLink>
          <button @click.stop="handleRemoveCharacter" class="btn btn-circle btn-ghost bg-transparent">
            <DeleteIcon />
          </button>
      </div>
      <div v-if="canRemoveFriend" class="absolute right-0 top-50">
        <button @click.stop="handleRemoveFriend" class="btn btn-circle btn-ghost bg-transparent">
          <DeleteIcon />
        </button>
      </div>
        <div class="absolute left-4 top-48 avatar">
          <div class="w-16  rounded-full ring-3 ring-white ">
            <img :src="character.photo" alt="">
          </div>
        </div>
        <div class="absolute left-24 right-4 top-52 text-white font-bold line-clamp-1 break-all">
          {{ character.name }}
        </div>
        <div class="absolute left-4 right-4 top-66 text-white line-clamp-4 break-all">
          {{ character.profile }}
        </div>
    </div>
  </div>
  <RouterLink :to="{name: 'user-space-index', params: {user_id: character.author.user_id}}" class="flex items-center mt-4 gap-2 w-60">
      <div class="avatar">
        <div class="w-7 rounded-full">
          <img :src="character.author.photo" alt="">
        </div>
      </div>
      <div class="text-sm line-clamp-1 break-all">{{ character.author.username }}</div>
    </RouterLink>
   <ChatField ref="chat-filed-ref" :ai_friend="ai_friend"/>
</div>
</template>

<style scoped>

</style>