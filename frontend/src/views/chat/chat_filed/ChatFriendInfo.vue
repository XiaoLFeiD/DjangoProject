<script setup>

import ChatFriendUserCard from "@/views/chat/chat_filed/components/ChatFriendUserCard.vue";
import ChatFriendSearch from "@/views/chat/chat_filed/components/ChatFriendSearch.vue";
import ChatFriendTab from "@/views/chat/chat_filed/components/ChatFriendTab.vue";
</script>

<template>
<div class="w-[260px] h-full bg-base-200 flex flex-col border-r">
    <ChatFriendUserCard />
    <ChatFriendSearch />
    <ChatFriendTab />
  </div>
</template>

<style scoped>

</style>