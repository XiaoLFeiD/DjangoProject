import {defineStore} from "pinia";
import {ref} from "vue";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";

export const useChatStore = defineStore('chat',()=>{
    const friends = ref([])
    const activeChat = ref(null)
    const messages = ref([])
    const socket = ref(null)
    const user = useUserStore()

    async function initWebSocket() {
        if (!user.id) {
        return;
    }
        // 如果已存在开启的连接，不要重复创建
        if (socket.value && (socket.value.readyState === WebSocket.OPEN || socket.value.readyState === WebSocket.CONNECTING)) return;

        const wsUrl = `ws://47.105.91.154/ws/chat/${user.id}/`;

        // 连向个人频道。请确保这里的 user.id 确实是 UserProfile 的 ID
        socket.value = new WebSocket(wsUrl);

        socket.value.onopen = () => {
        console.log("%cWebSocket 个人频道连接成功！", "color: green; font-weight: bold;");
    };

        socket.value.onmessage = (e) => {
            const data = JSON.parse(e.data);
            // 逻辑 A：全局更新左侧列表（谁发消息谁变最后一条并置顶）
            const friendIndex = friends.value.findIndex(f => f.conversation_id === data.conversation_id);
            if (friendIndex !== -1) {
                const friend = friends.value[friendIndex];
                friend.lastMsg = data.content;
                friend.time = data.create_time;
                // 移到数组第一项
                friends.value.splice(friendIndex, 1);
                friends.value.unshift(friend);
            }

            // 逻辑 B：更新右侧聊天展示
            // 只有当收到的消息属于当前点击的好友时，才 push 到 messages
            if (activeChat.value && activeChat.value.conversation_id === data.conversation_id) {
                messages.value.push(data);
            }
        };

        socket.value.onclose = () => { socket.value = null; };
        socket.value.onerror = () => { socket.value = null; };
    }

    async function sendMessage(text) {
        // 只有 Socket 开启且选中了好友才能发
        if (socket.value?.readyState === WebSocket.OPEN && activeChat.value && text) {
            socket.value.send(JSON.stringify({
                'message': text,
                'sender_id': user.id, // 这里必须传 UserProfile 的 ID
                'conversation_id': activeChat.value.conversation_id // 告诉后端发给哪个房间
            }));
        } else {
            // 如果正在连接中，提示用户稍等
        if (socket.value && socket.value.readyState === WebSocket.CONNECTING) {
            return;
        }
            await initWebSocket();
        }
    }


    async function selectFriend(friend){
        activeChat.value = {
            'id':friend.id,
            'username':friend.username,
            'photo':friend.photo,
            'lastMsg':friend.lastMsg,
            'time':friend.time,
            'conversation_id': friend.conversation_id
        }
        messages.value = []
         try {
            const res = await api.get(`api/friend/messages/`, {
                params: {
                    conversation_id: friend.conversation_id
                }
            });
            const data = res.data
            if (data.result === 'success') {
                messages.value = data.messages;
            }
        } catch (e) {
        }
    }

    function addNewFriend(newFriend) {
        // 防止重复添加
        if (!friends.value.find(f => f.id === newFriend.id)) {
            friends.value.unshift(newFriend)
        }
    }

    // 新增：初始化时从后端拉取好友列表 (你需要去写对应的后端GET接口)
    async function fetchFriendsFromServer() {
         try {
            const res = await api.get('api/friend/get_friend_list/',{
                params:{
                    id:user.id,
                }
            });
            const data = res.data
            if (data.result === 'success') {
                friends.value = data.friends;
            }
        } catch (e) {
        }
    }
    function clearChatData() {
        friends.value = [];
        activeChat.value = null;
        messages.value = [];
        if (socket.value) {
            socket.value.close();
            socket.value = null;
        }
    }

    return {
        friends,
        activeChat,
        messages,
        socket,
        selectFriend,
        // connectWebSocket,
        sendMessage,
        addNewFriend,
        fetchFriendsFromServer,
        initWebSocket,
        clearChatData,
    }
})