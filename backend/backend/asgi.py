"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
#
# from web.routing import websocket_urlpatterns
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
# })


import os
import django
from django.core.asgi import get_asgi_application

# ================= 极其重要的顺序 =================

# 1. 必须最先设置环境变量，告诉程序配置文件在哪
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# 2. 立刻初始化 Django！(解决报错的核心就在这一行)
django.setup()

# 3. 等 Django 初始化完成后，再导入 Channels 组件和你自己的路由/模型
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from web.routing import websocket_urlpatterns

# ================================================

# 4. 定义 application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})