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

@api_view(['POST','PUT','DELETE'])
def handle_friend_request(request):
    if request.method=='POST':
        Notification.create_notification(sender=request.user, recipient_uuid=request.data['recipient_uuid'],type=request.data['type'],text=request.data['text'])
        return Response(status=status.HTTP_200_OK)
    elif request.method=='PUT':
        print('nooo')
    elif request.method=='DELETE':
        if 'notification_uuid' in request.data:
            Notification.get_by_uuid(request.data['notification_uuid']).delete()
            return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
