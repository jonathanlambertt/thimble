from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status

from .serializers import *
from .models import Group

from users.models import Profile

@api_view(['POST'])
def create(request):
    group_serializer = CreateGroupSerializer(data=request.data)
    if group_serializer.is_valid(raise_exception=True):
        group_serializer.save(creator=Profile.get_profile(request.user))
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def group_view(request, group_type):
    current_profile = Profile.get_profile(request.user)
    group_types = {'joined':current_profile.joined_groups, 'created':current_profile.my_groups}
    if group_type in group_types:
        serialized_groups = GroupViewSerializer(group_types[group_type].all(), many=True)
        return Response(serialized_groups.data)

@api_view(['PUT'])
def add_member(request, group_id, profile_id):
    current_group = Group.get_group_by_uuid(group_id)
    current_group.add_member(Profile.get_by_uuid(profile_id))
    return Response(status=status.HTTP_200_OK)
