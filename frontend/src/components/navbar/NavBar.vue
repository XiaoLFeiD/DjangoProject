<script setup>

import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomePageIcon from "@/components/navbar/icons/HomePageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import {useUserStore} from "@/stores/user.js";
import UserMenu from "@/components/navbar/UserMenu.vue";
import {ref, useTemplateRef, watch} from "vue";
import {useRoute, useRouter} from "vue-router";
import ChatIcon from "@/views/chat/icons/ChatIcon.vue";
import ChatFriendIndex from "@/views/chat/ChatFriendIndex.vue";

const user = useUserStore()
const searchQuery = ref('')
const router = useRouter()
const route = useRoute()


watch(() => route.query.q, newQ => {
  searchQuery.value = newQ || ''
})

function handleSearch() {
  router.push({
    name: 'home-index',
    query: {
      q: searchQuery.value.trim(),
    }
  })
}

const chatFiledRef = useTemplateRef('chat-filed-ref')
async function handleChat(){
  if(!user.isLogin()){
    await router.push({
      name: 'user-account-login-index',
    })
  }else{
      chatFiledRef.value.showModal()
  }
}
</script>

<template>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content">
      <!-- Navbar -->
      <nav class="navbar w-full bg-base-100 shadow-sm">
        <div class="navbar-start">
          <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">
          <MenuIcon />
          </label>
        </div>


        <div class="navbar-center w-4/5 max-w-180 flex justify-center">
          <form @submit.prevent="handleSearch" class="join w-4/5 flex justify-center">
            <input v-model="searchQuery" class="input join-item rounded-l-full w-4/5" placeholder="搜索你感兴趣的内容" />
            <button class="btn join-item rounded-r-full gap-0">
              <SearchIcon />
              搜索
            </button>
          </form>
        </div>
        <div class="navbar-end">
<!--          <button class="btn btn-ghost text-base">登录</button>-->
          <RouterLink v-if="user.isLogin()" :to="{name: 'create-index'}" active-class="btn-active" class="btn btn-ghost text-base mr-6">
            <CreateIcon />
            创作
          </RouterLink>
          <RouterLink v-if="user.hasPulledUserInfo && !user.isLogin()" :to="{name: 'user-account-login-index'}" active-class="btn-active" class="btn btn-ghost text-base">
            登录
          </RouterLink>
          <UserMenu v-else-if="user.isLogin()" />
        </div>
      </nav>
      <slot></slot>
    </div>

    <div class="drawer-side is-drawer-close:overflow-visible">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
      <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-14 is-drawer-open:w-64">
        <!-- Sidebar content here -->
        <ul class="menu w-full grow">
          <li>
<!--            <button class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="首页">-->
            <RouterLink :to="{name: 'home-index'}"  active-class="menu-focus" class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="首页">
              <span class="inline-flex w-10 justify-center">
                <HomePageIcon class="w-5 h-5" />
              </span>
              <span class="is-drawer-close:hidden text-base whitespace-nowrap">首页</span>
             </RouterLink>
<!--            </button>-->
          </li>
           <li>
<!--            <button class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="好友">-->
               <RouterLink :to="{name: 'friend-index'}"  active-class="menu-focus" class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="好友">
              <span class="inline-flex w-10 justify-center">
                <FriendIcon class="w-5 h-5" />
              </span>
              <span class="is-drawer-close:hidden text-base whitespace-nowrap">好友</span>
             </RouterLink>
<!--            </button>-->
          </li>
           <li>
<!--            <button class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="创作">-->
             <RouterLink :to="{name: 'create-index'}"  active-class="menu-focus" class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="创作">
              <span class="inline-flex w-10 justify-center">
                <CreateIcon class="w-5 h-5" />
              </span>
              <span class="is-drawer-close:hidden text-base whitespace-nowrap">创作</span>
              </RouterLink>
<!--            </button>-->
          </li>
          <li>
             <button class="flex items-center w-full mt-2 px-2 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="聊天" @click="handleChat">
              <span class="inline-flex w-10 justify-center">
                <ChatIcon class="w-5 h-5"/>
              </span>
              <span class="is-drawer-close:hidden text-base whitespace-nowrap">聊天</span>
              </button>
          </li>
        </ul>
      </div>
    </div>
      <div class="flex flex-col items-center mb-12">
        <ChatFriendIndex ref="chat-filed-ref"/>
      </div>
  </div>
</template>

<style scoped>

</style>