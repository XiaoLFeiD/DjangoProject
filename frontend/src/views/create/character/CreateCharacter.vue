<script setup>

import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import {ref, useTemplateRef} from "vue";
import {useUserStore} from "@/stores/user.js";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import {useRouter} from "vue-router";

const user = useUserStore()
const router = useRouter()
const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')

async function handleCreate(){
  const photo = photoRef.value.myPhoto
  const name = nameRef.value.myName
  const profile = profileRef.value.myProfile
  const backgroundImage = backgroundImageRef.value.myBackgroundImage
  errorMessage.value = ''

  if (!photo) {
    errorMessage.value = '头像不能为空'
  } else if (!name) {
    errorMessage.value = '名字不能为空'
  } else if (!profile) {
    errorMessage.value = '角色介绍不能为空'
  } else if (!backgroundImage) {
    errorMessage.value = '聊天背景不能为空'
  }else{
    const formdata = new FormData()
    formdata.append('name',name)
    formdata.append('profile',profile)
    formdata.append('photo',base64ToFile(photo,'photo.png'))
    formdata.append('background_image',base64ToFile(backgroundImage,'background_image.png'))
    try {
      const res = await api.post('api/create/character/create/',formdata)
      const data = res.data
      if (data.result === 'success'){
        await router.push({
          name:'user-space-index',
          params:{
            user_id:user.id,
          }
        })
      }else{
        errorMessage.value = data.result
      }
    }catch (e){

    }
  }

}

</script>

<template>
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-16">
      <div class="card-body p-2">
         <h3 class="text-lg font-bold my-4">创建角色</h3>
        <photo ref="photo-ref"/>
        <name ref="name-ref"/>
        <profile ref="profile-ref"/>
        <background-image ref="background-image-ref"/>

        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>

        <div class="flex justify-center">
          <button @click="handleCreate" class="btn btn-neutral w-60 mt-2">创建</button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>

</style>