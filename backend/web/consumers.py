import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import localtime, now

from web.models.conversation import Conversation
from web.models.conversion_member import ConversationMember
from web.models.message import Message
from web.models.user import UserProfile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.conversation_id = self.scope['url_route']['kwargs']['conv_id']
        # self.room_group_name = f'chat_{self.conversation_id}'

        self.my_user_profile_id = self.scope['url_route']['kwargs']['conv_id']
        self.room_group_name = f'user_{self.my_user_profile_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender_id')  # 此时应为发送者的 UserProfile ID
        conversation_id = data.get('conversation_id')

        # 1. 存入数据库
        await self.save_message(sender_id, message, conversation_id)

        # 2. 找到接收者 (UserProfile ID)
        recipient_id = await self.get_recipient_id(conversation_id, sender_id)

        # 3. 构造要分发的载荷
        payload = {
            'type': 'chat_message_handler',  # 必须对应下方函数名
            'content': message,
            'sender_id': sender_id,
            'conversation_id': conversation_id,
            'create_time': localtime(now()).strftime('%H:%M')
        }

        # 4. 同时推送给发送者和接收者的个人频道
        # 即使接收者没打开该会话，只要他连了 WS 就能收到这个包，从而刷新他的侧边栏
        await self.channel_layer.group_send(f'user_{sender_id}', payload)
        if recipient_id:
            await self.channel_layer.group_send(f'user_{recipient_id}', payload)

    # 逻辑分发器
    async def chat_message_handler(self, event):
        # 将数据推回前端浏览器
        await self.send(text_data=json.dumps({
            'content': event['content'],
            'sender_id': event['sender_id'],
            'conversation_id': event['conversation_id'],
            'create_time': event['create_time'],
            'id': None
        }))


    @database_sync_to_async
    def get_recipient_id(self, conv_id, my_id):
        # 查找会话中的对方
        member = ConversationMember.objects.filter(conversation_id=conv_id).exclude(user_id=my_id).first()
        return member.user_id if member else None

    @database_sync_to_async
    def save_message(self, sender_id, content, conv_id):
        try:
            sender = UserProfile.objects.get(id=sender_id)
            # conv = Conversation.objects.get(id=self.conversation_id)
            conv = Conversation.objects.get(id=conv_id)
            Message.objects.create(
                conversation=conv,
                sender=sender,
                content=content,
                # mtype='text'
            )
            # 更新会话时间
            conv.update_time = now()
            conv.save()
        except Exception as e:
            print(f"保存消息失败: {e}")