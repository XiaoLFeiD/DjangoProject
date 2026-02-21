from django.urls import path, re_path

from web.views.create.character.create import CreateCharacterApiView
from web.views.create.character.get_list import GetListCharacterAPIView
from web.views.create.character.get_single import GetSingleCharacterApiView
from web.views.create.character.remove import RemoveCharacterAPIView
from web.views.create.character.update import UpdateCharacterApiView
from web.views.ai_friend.get_list import GetListAiFriendAPIView
from web.views.ai_friend.get_or_create import GetOrCreaterAiFriendsAPIView
from web.views.ai_friend.remove import RemoveAiFriendAPIView
from web.views.friend.add_friend import AddFriendAPIView
from web.views.friend.get_friend_list import GetFriendListAPIView
from web.views.friend.messages import FriendMessagesAPIView
from web.views.friend.search_list import SearchListFriendAPIView
from web.views.homepage.index import HomepageIndexApiView
from web.views.index import index
from web.views.user.account.get_user_info import GetUserInfoAPIView
from web.views.user.account.login import LoginAPIView
from web.views.user.account.logout import LogoutAPIView
from web.views.user.account.refresh_token import RefreshTokenAPIView
from web.views.user.account.register import RegisterApiView
from web.views.user.profile.updateprofile import UpdateProfileAPIView

urlpatterns =[
    path('api/user/account/login/', LoginAPIView.as_view()),
    path('api/user/account/logout/', LogoutAPIView.as_view()),
    path('api/user/account/register/', RegisterApiView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenAPIView.as_view()),
    path('api/user/account/get_user_info/', GetUserInfoAPIView.as_view()),

    path('api/user/profile/updateprofile/', UpdateProfileAPIView.as_view()),
    path('api/create/character/create/', CreateCharacterApiView.as_view()),
    path('api/create/character/remove/', RemoveCharacterAPIView.as_view()),
    path('api/create/character/update/', UpdateCharacterApiView.as_view()),
    path('api/create/character/get_single/',GetSingleCharacterApiView.as_view()),
    path('api/create/character/get_list/',GetListCharacterAPIView.as_view()),
    path('api/homepage/index/',HomepageIndexApiView.as_view()),
    path('api/ai_friend/get_list/',GetListAiFriendAPIView.as_view()),
    path('api/ai_friend/get_or_create/',GetOrCreaterAiFriendsAPIView.as_view()),
    path('api/ai_friend/remove/',RemoveAiFriendAPIView.as_view()),
    path('api/friend/add_friend/', AddFriendAPIView.as_view()),
    path('api/friend/search_list/',SearchListFriendAPIView.as_view()),
    path('api/friend/get_friend_list/',GetFriendListAPIView.as_view()),
    path('api/friend/messages/',FriendMessagesAPIView.as_view()),
    path('', index),
    #匹配任意路由，即接受前端的任意路由
    #在前端任意路径下刷新时，django都自动路由到根路径下，剩下的路由交由前端处理。
    re_path(r'^(?!media/|static/|assets/).*$', index)
]