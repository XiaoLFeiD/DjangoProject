import uuid
from django.db import models
from django.utils.timezone import now, localtime

from web.models.conversation import Conversation
from web.models.user import UserProfile


class ConversationMember(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='conversations'
    )

    last_read_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    join_time = models.DateTimeField(default=now())

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f'{self.user.user.username} in {self.conversation.id}'