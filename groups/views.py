from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status

from .serializers import *
from .models import Group

from users.models import Profile
from users.serializers import FriendsListResultSerializer

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
        serialized_groups = GroupViewSerializer(group_types[group_type].all().exclude(creator=current_profile), many=True)
        return Response(serialized_groups.data)

@api_view(['GET'])
def list_members(request, group_id):
    current_group = Group.get_group_by_uuid(group_id)
    serialized_data = FriendsListResultSerializer(current_group.members.all().exclude(uuid=Profile.get_profile(request.user).uuid), many=True)
    return Response(serialized_data.data)

@api_view(['PUT'])
def leave_group(request, group_id):
    return perform_action(request._request, group_id, 'remove', Profile.get_profile(request.user).uuid)

@api_view(['PUT'])
def perform_action(request, group_id, action, profile_id):
    current_group = Group.get_group_by_uuid(group_id)
    possible_actions = {'add':current_group.add_member, 'remove':current_group.remove_member}
    if action in possible_actions:
        possible_actions[action](Profile.get_by_uuid(profile_id))
    
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def user_status(request, group_id):    
    result = {'message':'member'}
    if Group.get_group_by_uuid(group_id).creator == Profile.get_profile(request.user):
        result['message'] = 'owner'
    return Response(result)
        
@api_view(['GET'])
def potential_members(request, group_id):
    the_group = Group.get_group_by_uuid(group_id)
    you = Profile.get_profile(request.user)
    possible_members = you.friends.exclude(uuid__in=[member.uuid for member in the_group.members.all()])
    return Response(FriendsListResultSerializer(possible_members, many=True).data)