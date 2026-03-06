import uuid
from django.db import models
from django.utils.timezone import now, localtime

from web.models.conversation import Conversation
from web.models.user import UserProfile

class Message(models.Model):
    MESSAGE_TYPE = (
        ('text', 'Text'),
        ('image', 'Image'),
    )

    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    mtype = models.CharField(max_length=20, choices=MESSAGE_TYPE, default='text')
    content = models.TextField()

    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['conversation', 'create_time']),
        ]

    def __str__(self):
        return f'{self.sender.user.username} - {self.create_time.strftime("%Y-%m-%d %H:%M:%S")}'