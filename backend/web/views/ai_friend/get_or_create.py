from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.aifriend import AIFriend
from web.models.user import UserProfile


class GetOrCreaterAiFriendsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            character_id = request.data['character_id']
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            ai_friends = AIFriend.objects.filter(character_id=character_id, me=user_profile)
            if ai_friends.exists():
                ai_friend = ai_friends.first()
            else:
                ai_friend = AIFriend.objects.create(character_id=character_id, me=user_profile)

            character = ai_friend.character
            author = character.author
            return Response({
                "result":'success',
                'ai_friend': {
                    'id': ai_friend.id,
                    'character': {
                        'id': character.id,
                        'name': character.name,
                        'profile': character.profile,
                        'photo': character.photo.url,
                        'background_image': character.background_image.url,
                        'author': {
                            'user_id': author.user_id,
                            'username': author.user.username,
                            'photo': author.photo.url,
                        }
                    }
                }

            })
        except:
            return Response({
                'result':'系统异常，请稍后重试'
            })