import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, localtime

def photo_upload_to(instance, filename): # instance为当前存储实例
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}' # 如"a1b2c3d4e5.jpg"
    return f'user/photos/{instance.user_id}_{filename}'  # 如"user/photos/42_a1b2c3d4e5.jpg"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #与用户一一对应 删除用户时候删除对应Profile
    photo = models.ImageField(default='user/photos/default.png', upload_to=photo_upload_to)
    profile = models.TextField(default='谢谢你的关注', max_length=500)
    create_time = models.DateTimeField(default=now) #now为当前时区 使用localtime转换为当前时区的时间
    update_time = models.DateTimeField(default=now)
    def __str__(self):
        return f'{self.user.username} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}'