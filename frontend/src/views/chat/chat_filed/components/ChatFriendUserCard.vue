<script setup>
import {useUserStore} from "@/stores/user.js";

const user = useUserStore()
</script>

<template>
  <div class="h-14 border-b flex items-center px-6">
    <div class="relative">
      <img
        :src="user.photo"
        class="w-12 h-12 rounded-full object-cover"
      />
      <span
        class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"
      ></span>
    </div>
    <div>
      <div class="font-semibold ml-4">{{user.username}}</div>
    </div>
  </div>
</template>

<style scoped>

</style>