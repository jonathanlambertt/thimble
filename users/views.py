from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

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
    query = search_query
    results = User.objects.filter(username__icontains=query)
    print(results)
    # searcher_profile = Profile.get_profile(request.user)
    # result_profiles = []
    # if results.count() != 0:
    #     for result in results:
    #         result_user = User.objects.get(username=result)
    #         result_user_profile = Profile.objects.get(user=result_user)
    #
    #         if searcher_profile.friends.all().filter(user=result_user).exists():
    #             result_profiles.append({"status": "friends", "profile": ResultProfileSerializer(result_user_profile).data})
    #         elif searcher_profile == result_user_profile:
    #             result_profiles.append({"status": "you", "profile": ResultProfileSerializer(result_user_profile).data})
    #         else:
    #             result_profiles.append({"profile": ResultProfileSerializer(result_user_profile).data})
    #     return Response(result_profiles)
    # else:
    return Response({'innit':ProfileSerializer(results, many=True)})
