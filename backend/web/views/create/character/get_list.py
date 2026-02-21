from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.character import Character
from web.models.user import UserProfile


class GetListCharacterAPIView(APIView):
    def get(self, request):
        try:
            item_counts = int(request.query_params.get('item_counts'))
            user_id = request.query_params.get('user_id')
            user = User.objects.get(id=user_id)
            userprofile = UserProfile.objects.get(user=user)
            character_raw = Character.objects.filter(author=userprofile).order_by('-id')[item_counts:item_counts+10]
            characters = []
            for character in character_raw:
                author = character.author
                characters.append({
                    'id': character.id,
                    'name':character.name,
                    'profile':character.profile,
                    'photo':character.photo.url,
                    'background_image':character.background_image.url,
                    'author':{
                        'user_id':author.user.id,
                        'username':author.user.username,
                        'photo':author.photo.url,
                    }
                })
            return Response({
                'result':'success',
                'characters':characters,
                'user_profile':{
                    'id':user.id,
                    'username':user.username,
                    'photo':userprofile.photo.url,
                    'profile':userprofile.profile,
                }
            })
        except:
            return Response({
                'result','系统异常，请稍后再试',
            })