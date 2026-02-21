from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from web.models.aifriend import AIFriend


class RemoveAiFriendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            ai_friend_id = request.data['ai_friend_id']
            AIFriend.objects.filter(id=ai_friend_id, me__user=request.user).delete()
            return Response({
                'result': 'success',
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })



