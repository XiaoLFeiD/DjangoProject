import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, localtime


class Conversation(models.Model):
    CONVERSATION_TYPE = (
        ('private', 'Private'),
        ('group', 'Group'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=CONVERSATION_TYPE, default='private')
    name = models.CharField(max_length=100, blank=True, null=True)  # 群聊才需要
    create_time = models.DateTimeField(default=now())
    update_time = models.DateTimeField(default=now())

    def __str__(self):
        return f'{self.type}-{self.id}-{localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}'