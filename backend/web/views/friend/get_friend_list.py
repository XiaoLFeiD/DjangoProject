from django.utils.timezone import localtime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.conversation import Conversation
from web.models.conversion_member import ConversationMember
from web.models.friend import Friend
from web.models.message import Message
from web.models.user import UserProfile


class GetFriendListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            id = request.query_params.get('id')
            me = UserProfile.objects.get(id=id)
            # 获取所有好友关系，并预加载关联的 User 和 UserProfile 信息
            # friend_relations = Friend.objects.filter(user=me).select_related('friend__user')

            # 获取当前用户加入的所有私聊会话成员记录
            # 按会话的 update_time 倒序排列（活跃的在前）
            my_memberships = ConversationMember.objects.filter(
                user=me,
                conversation__type='private'
            ).select_related('conversation').order_by('-conversation__update_time')

            friend_list = []
            for rel in my_memberships:
                conv  = rel.conversation

                # 找到这个会话里的“另一个人”即好友
                friend_member = ConversationMember.objects.filter(
                    conversation=conv
                ).exclude(user=me).select_related('user__user').first()

                if not friend_member:
                    continue

                friend_profile = friend_member.user

                # 为当前好友找到对应的私聊会话 ID
                # 逻辑：查找类型为 private 且成员包含我和该好友的会话
                # conv = Conversation.objects.filter(
                #     type='private',
                #     members__user=me
                # ).filter(
                #     members__user=friend_profile
                # ).first()

                # --- 新增：获取该会话最后一条消息 ---
                last_msg_obj = Message.objects.filter(conversation=conv).order_by('-create_time').first()

                last_content = "已添加好友,点击开始聊天"
                last_time = ""

                if last_msg_obj:
                    last_content = last_msg_obj.content
                    # 格式化时间：如果是今天的只显示时间，不是今天的显示日期
                    # 这里先简单处理为 HH:mm
                    last_time = localtime(last_msg_obj.create_time).strftime('%H:%M')

                friend_list.append({
                    "id": friend_profile.id,
                    "username": friend_profile.user.username,
                    "photo": friend_profile.photo.url,
                    "conversation_id": str(conv.id) if conv else None,
                    "lastMsg": last_content,  # 这里后续可以查 Message 表获取最后一条
                    "time": last_time
                })
            return Response({
                "result": "success",
                "friends": friend_list
            })
        except:
            return Response({
                "result": "系统异常，请稍后重试"
            })