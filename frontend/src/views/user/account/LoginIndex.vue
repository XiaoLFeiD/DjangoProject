<script setup>

import {ref} from "vue";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";

const username = ref('')
const password = ref('')
const errormessage = ref('')
const user = useUserStore()
const router = useRouter()

// 异步请求函数 可以等待
// await 只能用在 async 函数内部 等待结果返回
async function handleLogin(){
   errormessage.value = ''
  if(!username.value.trim()){
    errormessage.value = "用户名为空"
  }else if(!password.value.trim()){
    errormessage.value = "密码为空"
  }else{
    try {
    const res = await api.post("/api/user/account/login/",{
      username: username.value,
      password:password.value,
    })
    const data = res.data
    if(data.result === "success"){
      user.setAccessToken(data.access_token)
      user.setUserInfo(data)
      await router.push({
        name: 'home-index'
      })
    }else{
      errormessage.value = data.result
    }
    }catch (err){
    }
  }
}
</script>

<template>
  <div class="flex justify-center mt-40">
    <form @submit.prevent="handleLogin" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
      <span class="fieldset-legend">登录</span>

      <label class="label">用户名</label>
      <input v-model="username" type="text" class="input" placeholder="用户名" />

      <label class="label">密码</label>
      <input v-model="password" type="password" class="input" placeholder="密码" />
      <p v-if="errormessage" class="text-sm text-red-500 mt-1">{{errormessage}}</p>
      <button class="btn btn-neutral mt-4">登录</button>
      <div class="flex justify-end">
        <router-link :to="{name: 'user-account-register-index'}" class="btn btn-sm btn-ghost text-gray-500">注册</router-link>
      </div>
    </form>
  </div>

</template>

<style scoped>

</style>