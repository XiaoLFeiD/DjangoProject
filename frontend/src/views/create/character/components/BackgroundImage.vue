<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/create/character/components/icons/CameraIcon.vue";
import Croppie from "croppie";
import 'croppie/croppie.css'

const props = defineProps(['background_image'])
const myBackgroundImage = ref(props.background_image)
const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

watch(()=>props.background_image,newValue=>{
  myBackgroundImage.value = newValue
})


async function crop(){
  if(!croppie) return
  myBackgroundImage.value = await croppie.result({
    type:'base64',
    size:'viewport'
  })
  modalRef.value.close()
}

async function openModal(photo){
    modalRef.value.showModal()
    await nextTick()
    if(!croppie){
      croppie = new Croppie(croppieRef.value,{
        viewport: {width: 200, height: 200, type: 'square'},
        boundary: {width: 300, height: 300},
        enableOrientation: true,
        enforceBoundary: true,
      })
    }
    croppie.bind({
      url:photo,
    })
}

async function onChangeFile(e){
    const file = e.target.files[0]
    e.target.value = ''
    if(!file) return
    const reader = new FileReader()
    reader.onload = ()=>{
      openModal(reader.result)
    }

    reader.readAsDataURL(file)
}

onBeforeUnmount(()=>{
  croppie?.destroy()
})

defineExpose({
  myBackgroundImage,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">聊天背景</label>
    <div class="avatar relative">
      <div v-if="myBackgroundImage" class="w-15 h-25 rounded-box">
        <img :src="myBackgroundImage" alt="">
      </div>
      <div v-else class="w-15 h-25 rounded-box bg-base-300"></div>
      <div @click="fileInputRef.click()" class="w-15 h-25 rounded-box absolute left-0 top-0 bg-black/20 flex justify-center items-center cursor-pointer">
        <CameraIcon />
      </div>
    </div>
  </fieldset>

  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onChangeFile">
  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-circle btn-sm btn-ghost absolute right-2 top-2">✕</button>
      <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>
      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">取消</button>
        <button @click="crop" class="btn btn-neutral">确定</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>