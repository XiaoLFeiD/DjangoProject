from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.message import Message


class FriendMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            conv_id = request.query_params.get('conversation_id')
            # 查找该会话下的所有未删除消息，按时间排序
            messages_query = Message.objects.filter(
                conversation_id=conv_id,
                is_deleted=False
            ).order_by('create_time')

            results = []
            for msg in messages_query:
                results.append({
                    'id': msg.id,
                    'content': msg.content,
                    'mtype': msg.mtype,
                    'sender_id': msg.sender.id,
                    'create_time': msg.create_time.strftime('%Y-%m-%d %H:%M:%S')
                })

            return Response({
                "result": "success",
                "messages": results
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试',
            })