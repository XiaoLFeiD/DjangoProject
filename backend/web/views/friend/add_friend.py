from django.utils.timezone import now, localtime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.conversation import Conversation
from web.models.conversion_member import ConversationMember
from web.models.friend import Friend
from web.models.user import UserProfile


class AddFriendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            friend_id = request.data.get('friend_id')
            me_id = request.data.get('id')
            friend_user = UserProfile.objects.get(id=friend_id)
            me = UserProfile.objects.get(id=me_id)

            # 1. 创建好友关系 (双向)
            Friend.objects.get_or_create(user=me, friend=friend_user)
            Friend.objects.get_or_create(user=friend_user, friend=me)

            # 2. 检查或创建私聊会话 (Conversation)
            # 逻辑：查找是否存在一个 type='private' 且成员包含这两个人的会话
            conv = Conversation.objects.filter(type='private', members__user=me).filter(
                members__user=friend_user).first()
            if not conv:
                conv = Conversation.objects.create(type='private')
                ConversationMember.objects.create(conversation=conv, user=me)
                ConversationMember.objects.create(conversation=conv, user=friend_user)

            return Response({
                "result": "success",
                "friend_data":{
                    "id": friend_user.id,
                    "username": friend_user.user.username,
                    "photo": friend_user.photo.url,
                    "lastMsg": "已添加好友",
                    "conversation_id": str(conv.id),
                    "time": localtime(now()).strftime('%m-%d %H:%M:%S'),
                }
            })
        except:
            return Response({
                'result': "系统异常，请稍后重试",
            })