<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icons/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(()=>props.photo,newVal=>{
  myPhoto.value = newVal
})

const FileInputRef = useTemplateRef('file-input-ref')
const modalRef  = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo){
  modalRef.value.showModal()
  await nextTick() //等待所以元素渲染完成后
  if(!croppie){
    croppie = new Croppie(croppieRef.value,{
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }
  croppie.bind({
    url: photo,
  })
}
async function crop(){
    if (!croppie) return
    myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })
  modalRef.value.close()
}

// 监听事件函数
async function onFileChange(e){
    // 取出目标文件后置空
    const file = e.target.files[0]
    e.target.value = ''
    if (!file) return
    const reader = new FileReader()
    //文件加载完后打开一个模态框
    reader.onload = () => {
      openModal(reader.result)
  }
    //转化文件格式为base64
    reader.readAsDataURL(file)
}

onBeforeUnmount(() => {
  croppie?.destroy()
})
defineExpose({
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar  relative">
      <div class="w-28 rounded-full">
        <img :src="myPhoto" alt="">
      </div>
      <div @click="FileInputRef.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon />
      </div>
    </div>
  </div>
  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange">
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