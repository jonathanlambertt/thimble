from rest_framework import serializers

from .models import Notification

from users.serializers import ProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()

    class Meta:
        model =  Notification
        exclude = ['id', 'recipient']
