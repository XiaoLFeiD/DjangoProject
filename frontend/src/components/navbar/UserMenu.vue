<script setup>
import {useUserStore} from "@/stores/user.js";
import UserSpaceIcon from "@/components/navbar/icons/UserSpaceIcon.vue";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import api from "@/js/http/api.js";
import {useRouter} from "vue-router";
import {useChatStore} from "@/stores/chat.js";

const router = useRouter()
const user = useUserStore()
const chat = useChatStore()

function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}
async function logout(){
  try {
    const res = await api.post('/api/user/account/logout/')
    if(res.data.result === "success"){
      user.logout()
      chat.clearChatData()
     await router.push({
        name:"home-index"
      })
    }

  }catch (err){

  }
}
</script>

<template>
<div class="dropdown dropdown-end">
    <div tabindex="0" role="button" class="avatar btn btn-circle w-8 h-8 mr-6">
      <div class="w-8 rounded-full">
        <img  :src="user.photo" alt=""/>
      </div>
    </div>
    <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-lg">
      <li>
        <router-link @click="closeMenu" :to="{name:'user-space-index', params:{user_id : user.id}}">
          <div class="avatar">
           <div class="w-10 rounded-full">
             <img  :src="user.photo" alt=""/>
           </div>
          </div>
          <span class="text-base font-bold line-clamp-1 ml-4">{{user.username}}</span>
        </router-link>
      </li>
      <li>
        <router-link @click="closeMenu" :to="{name:'user-space-index', params:{user_id:user.id}}">
          <UserSpaceIcon/>
          <span class="text-base font-bold line-clamp-1 ml-4">个人空间</span>
        </router-link>
      </li>
      <li>
        <router-link @click="closeMenu" :to="{name:'user-profile-index'}">
          <UserProfileIcon/>
          <span class="text-base font-bold line-clamp-1 ml-4">编辑资料</span>
        </router-link>
      </li>
      <li>
      </li>
      <li>
        <a @click="logout" class="text-sm font-bold py-3">
          <UserLogoutIcon />
          <span class="text-base font-bold line-clamp-1 ml-4">退出登录</span>
        </a>
      </li>
    </ul>
  </div>

</template>

<style scoped>

</style>