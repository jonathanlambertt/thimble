from django.db import models

from datetime import datetime

from users.models import Profile

import uuid

class NotificationType(models.IntegerChoices):
    DEFAULT = 0
    FRIEND_REQUEST = 1

class Notification(models.Model):
    notification_type = models.IntegerField(NotificationType)
    sender = models.ForeignKey(Profile, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, related_name='notifications', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=datetime.now)
    uuid = models.UUIDField()

    def create_notification(**kwargs):
        recipient = Profile.get_by_uuid(kwargs['recipient_uuid'])
        sender = Profile.get_profile(user=kwargs['sender'])
        Notification.objects.create(notification_type=kwargs['notification_type'], sender=sender,recipient=recipient,
        text=kwargs['text'],uuid=uuid.uuid4())

    def get_by_uuid(uuid):
        return Notification.objects.get(uuid=uuid)
