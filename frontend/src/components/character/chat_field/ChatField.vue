<script setup>

import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import {computed, useTemplateRef} from "vue";

const props = defineProps(['ai_friend'])
const modalRef = useTemplateRef('modal-ref')

function showModal(){
  modalRef.value.showModal()
}

const modalStyle = computed(() => {
  if(props.ai_friend){
      return {
      backgroundImage: `url(${props.ai_friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  }else{
        return {}
    }
})
defineExpose({
  showModal,
})
</script>

<template>
<dialog ref="modal-ref" class="modal">
    <div class="modal-box w-90 h-150" :style="modalStyle">
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">✕</button>
      <InputField />
      <CharacterPhotoField v-if="ai_friend" :character="ai_friend.character" />
    </div>
  </dialog>
</template>

<style scoped>

</style>