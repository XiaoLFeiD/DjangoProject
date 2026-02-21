<script setup>

import UserInfoFied from "@/views/user/space/components/UserInfoFied.vue";
import Character from "@/components/character/Character.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef} from "vue";
import api from "@/js/http/api.js";
import {useRoute} from "vue-router";

const userProfile = ref(null)
const route = useRoute()
const characters = ref([])
const hasCharacter = ref(true)
const isLoading = ref(false)
const sentinelRef = useTemplateRef('sentinel-ref')

async function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore(){
  if (isLoading.value || !hasCharacter.value) return
  isLoading.value = true

  let newCharacter = []
  try {
    const res = await api.get('api/create/character/get_list/',{
      params:{
        'item_counts':characters.value.length,
        'user_id':route.params.user_id,
      }
    })
    const data = res.data
    if (data.result === 'success'){
      userProfile.value = data.user_profile
      newCharacter = data.characters
    }
  }catch (e){

  }finally {
    isLoading.value = false
    if (newCharacter.length === 0 ){
      hasCharacter.value = false
    }else{
      characters.value.push(...newCharacter)
      await nextTick()

      if (await checkSentinelVisible()){
        await loadMore()
      }
    }
  }
}
let observe = null
onMounted(async ()=>{
  await loadMore()

  observe = new IntersectionObserver(
      entries => {
        entries.forEach(entry=>{
          if (entry.isIntersecting){
            loadMore()
          }
        })
      },
  {root:null, rootMargin:'2px', threshold:0}
  )
  //监听哨兵
  observe.observe(sentinelRef.value)
})

async function removeCharacter(characterId){
   characters.value = characters.value.filter(c => c.id !== characterId)
}


onBeforeUnmount(()=>{
  observe?.disconnect()
})
</script>

<template>
<div class="flex flex-col items-center mb-12">
  <UserInfoFied  :userprofile="userProfile"/>
  <!--  可以根据屏幕宽度自动决定每行的元素数量，并将元素均匀排列在屏幕上；当最后一行元素不足时会左对齐。-->
  <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
    <Character
      v-for="character in characters"
      :key="character.id"
      :character="character"
      :canEdit="true"
      @remove="removeCharacter"
    />
  </div>
  <div ref="sentinel-ref" class="h-2 mt-8 w-100"></div>
  <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
  <div v-else-if="!hasCharacter" class="text-gray-500 mt-4">没有更多角色了</div>
</div>

</template>

<style scoped>

</style>