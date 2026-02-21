<script setup>
const props = defineProps(['userprofile'])
</script>

<template>
<div v-if="props.userprofile" class="flex justify-center mt-12 gap-8">
  <div class="avatar">
    <div class="w-44 rounded-full">
        <img :src="props.userprofile.photo" alt="">
      </div>
  </div>
  <div class="flex flex-col justify-center w-64 h-44">
    <div class="text-2xl font-bold line-clamp-1 break-all">{{props.userprofile.username}}</div>
<!--    <div class="text-sm text-gray-500 mt-2">{{props.userprofile.id}}</div>-->
    <div class="text-sm h-20 mt-4 line-clamp-4 break-all">{{props.userprofile.profile}}</div>
  </div>
</div>
</template>

<style scoped>

</style>