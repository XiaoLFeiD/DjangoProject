from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend
from web.models.user import UserProfile


class SearchListFriendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 搜索用户
    def get(self, request):
       try:
           keyword = request.query_params.get('keyword', '').strip()
           id = request.query_params.get('id')
           me = User.objects.get(id=id)
           users = UserProfile.objects.filter(user__username__icontains=keyword).exclude(user=me)
           # 2. 获取当前用户所有好友的 ID 集合，用于快速比对
           meProfile = UserProfile.objects.get(user=me)
           my_friend_ids = set(Friend.objects.filter(user=meProfile).values_list('friend_id', flat=True))
           all_users = []
           for user in users:
             all_users.append({
                 'id': user.id,
                 'username': user.user.username,
                 'photo': user.photo.url,
                 'is_friend': user.id in my_friend_ids
             })
           # 返回序列化后的用户列表
           return Response({
               'result': 'success',
               'all_users': all_users,
           })
       except:
           return Response({
               'result':'系统异常，请稍侯重试'
           })
