import uuid
from django.db import models
from django.utils.timezone import now, localtime

from web.models.user import UserProfile

class Friend(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='friends'
    )
    friend = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='friend_of'
    )

    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f'{self.user.user.username} - {self.create_time.strftime("%Y-%m-%d %H:%M:%S")}'