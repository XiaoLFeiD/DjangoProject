from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import responses, Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username').strip()
            password = request.data.get('password').strip()
            if not username or not password:
                return Response({
                        'result': "用户名或密码为空",
                    })
            user = authenticate(username=username, password=password) #验证用户
            if user:
                user_profile = UserProfile.objects.get(user=user)
                refresh = RefreshToken.for_user(user) #生产jwt
                response = Response({
                    'result': 'success',
                    'access_token': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.get_username(),
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            return Response({
                'result': "用户名或密码不正确",
            })
        except:
            import traceback
            traceback.print_exc()
            return Response({
                    'result': "系统异常，请稍后重试",
                })
