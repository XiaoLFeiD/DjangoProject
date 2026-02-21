<script setup>

import NavBar from "@/components/navbar/NavBar.vue";
import {onMounted} from "vue";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
import {useRoute, useRouter} from "vue-router";
import {useChatStore} from "@/stores/chat.js";

const user = useUserStore()
const chat = useChatStore()
const route = useRoute()
const router = useRouter()
// 组件第一次挂载时候执行
onMounted( async () => {
  try {
    const res = await api.get('/api/user/account/get_user_info/')
    const data = res.data
    if(data.result === 'success'){
      user.setUserInfo(data)
    }
  }catch (err){

  }finally {
      user.setHasPulledUserInfo(true)
      if(route.meta.needLogin && !user.isLogin()){
        await router.replace({
          name: "user-account-login-index"
        })
      }
  }
})
</script>

<template>
  <NavBar>
    <RouterView />
  </NavBar>
</template>

<style scoped>

</style>
