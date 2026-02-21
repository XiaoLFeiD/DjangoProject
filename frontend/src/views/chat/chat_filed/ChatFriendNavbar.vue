<script setup>
const emit = defineEmits(['close','start_dialog'])

function closeChat(){
  emit('close')
}

function handleMouseDown(e) {
  emit("start_dialog", e)
}

</script>

<template>
  <div class="h-12 bg-base-200 flex items-center justify-between px-4 border-b select-none " @mousedown="handleMouseDown">
    <!-- 左侧 -->
    <div class="flex items-center gap-2">
      <svg
        width="24"
        height="24"
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="50" cy="50" r="50" fill="black" />
        <circle cx="35" cy="50" r="6" fill="white" />
        <circle cx="50" cy="50" r="6" fill="white" />
        <circle cx="65" cy="50" r="6" fill="white" />
      </svg>
      <span class="font-medium text-sm">Chat</span>
    </div>
    <!-- 右侧 -->
    <div class="flex items-center gap-2">
      <button
        class="btn btn-sm btn-circle btn-ghost hover:bg-red-500 hover:text-white" @click.stop="closeChat">
        ✕
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>