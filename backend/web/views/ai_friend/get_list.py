from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.aifriend import AIFriend


class GetListAiFriendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count',0))
            ai_friends_raw = AIFriend.objects.filter(
                me__user=request.user,
            ).order_by('-update_time')[items_count:items_count+20]
            ai_friends = []
            for ai_friend in ai_friends_raw:
                character = ai_friend.character
                author = character.author
                ai_friends.append({
                    'id':ai_friend.id,
                    'character':{
                        'id':character.id,
                        'name':character.name,
                        'profile':character.profile,
                        'photo':character.photo.url,
                        'background_image':character.background_image.url,
                        'author':{
                            'user_id':author.user_id,
                            'username':author.user.username,
                            'photo':author.photo.url,
                        }
                    }
                })
            return Response({
                'result':'success',
                'ai_friends':ai_friends,
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试',
            })