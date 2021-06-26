from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

from users.models import Profile
from .models import Notification

@api_view(['GET'])
def inbox(request):
    profile = Profile.get_profile(request.user)
    notifs = profile.notifications.all()
    notifs_serializer = NotificationSerializer(notifs, many=True)
    return Response(notifs_serializer.data)

@api_view(['POST'])
def send(request):
    sender = Profile.get_profile(request.user)
    recipient = Profile.get_by_uuid(request.data['recipient_uuid'])
    formats = {'1': f'{sender.user.username} wants to be friends'}
    Notification.create_notification(sender=request.user, recipient=recipient, notification_type=request.data['notification_type'],text=request.data['text'])
    recipient.send_notification(formats[request.data['notification_type']])
    return Response(status=status.HTTP_201_CREATED)

@api_view(['PUT','DELETE'])
def handle_friend_request(request, request_id):
    if request.method=='PUT':
        current_notification = Notification.get_by_uuid(request_id)
        current_notification.sender.friends.add(current_notification.recipient)
        current_notification.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method=='DELETE':
        Notification.get_by_uuid(request_id).delete()
        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
