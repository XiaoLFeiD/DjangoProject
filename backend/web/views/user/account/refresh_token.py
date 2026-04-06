from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class RefreshTokenAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES['refresh_token']
            if not refresh_token:
                return Response({
                    'result': 'refresh token不存在'
                }, status=401)  # 必须加401
            refresh = RefreshToken(refresh_token) # 检验refresh是否过期，过期爆异常
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                refresh.set_jti()
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    # secure=True,
                    secure=False,
                    max_age=86400 * 7,
                )
                return response
            return Response({
                'result': 'success',
                'access': str(refresh.access_token),
            })
        except:
            return Response({
                'result': "refresh token已过期",
            }, status=401)