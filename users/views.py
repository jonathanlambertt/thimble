from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

from notifications.models import Notification

# Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    profile_serializer = CreateProfileSerializer(data=request.data)
    if profile_serializer.is_valid(raise_exception=True):
        profile_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(profile_serializer.errors)

@api_view(['GET'])
def search(request, search_query):
    user_results = User.objects.filter(username__icontains=search_query)
    user_profile = Profile.get_profile(request.user)
    search_results = []
    for user_result in user_results:
        current_profile = Profile.objects.get(user=user_result)
        friendship = user_profile.friends.all().filter(user=user_result).exists() if user_profile != current_profile else True
        pending = user_profile.sent_notifications.filter(recipient=current_profile).exists()
        search_results.append(ProfileSearchResultSerializer({'profile':current_profile, 'are_friends':friendship, 'pending_friend_request':pending}).data)
        
    return Response(search_results)

@api_view(['GET'])
def friends(request):
    user_friends = Profile.get_profile(request.user).friends.all()
    serialized_result = FriendsListResultSerializer(user_friends, many=True)
    return Response(data=serialized_result.data)