<script setup>

import AddFriendNavbar from "@/views/chat/chat_filed/components/AddFriend/components/AddFriendNavbar.vue";
import {useTemplateRef} from "vue";
import AddFrinedInput from "@/views/chat/chat_filed/components/AddFriend/components/AddFrinedInput.vue";

const addFriendModalRef = useTemplateRef('add-friend-modal-ref')

function closeModal(){
  addFriendModalRef.value.close()
}

function showModal(){
  addFriendModalRef.value.showModal()
}

defineExpose({
  showModal,
  closeModal
})
</script>

<template>
  <dialog ref="add-friend-modal-ref" class="modal">
    <div class="modal-box w-150 h-150 p-0 flex flex-col">
      <AddFriendNavbar @close="closeModal"/>
      <AddFrinedInput @close="closeModal"/>
    </div>
  </dialog>
</template>

<style scoped>

</style>