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
    print(user_results)
    user_profile = Profile.get_profile(request.user)
    search_results = []
    for user_result in user_results:
        current_profile = Profile.objects.get(user=user_result)
        if user_profile.friends.all().filter(user=user_result).exists():
            search_results.append(ProfileSearchResultSerializer({'profile':current_profile, 'are_friends':True, 'pending_friend_request':False}).data) #need to implement friend request status
        elif user_profile != user_result:
            search_results.append(ProfileSearchResultSerializer({'profile':current_profile, 'are_friends':False, 'pending_friend_request':False}).data)
        
    return Response(search_results)

