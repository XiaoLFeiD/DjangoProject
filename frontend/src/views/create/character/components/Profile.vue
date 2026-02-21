<script setup>
import {ref, watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

watch(()=>props.profile,newValue=>{
  myProfile.value = newValue
})

defineExpose({
  myProfile,
})
</script>

<template>
<fieldset class="fieldset">
  <label class="label text-base">简介</label>
  <input v-model="myProfile" rows="6" class="textarea w-108">
</fieldset>
</template>

<style scoped>

</style>