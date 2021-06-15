from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PhotoPost
from .serializers import *

from users.models import Profile
from groups.models import Group
from posts.models import Post

import uuid
from users.RedisHelper import add_post_to_feed, delete_post_from_feed

@api_view(['POST'])
def create_post(request):
    post_serializers = {'0':CreateTextPostSerializer, '1': CreateLinkPostSerializer, '2':  CreatePhotoPostSerializer}
    if 'post_type' in request.data:
        if request.data['post_type'] in post_serializers:
            post_serializer = post_serializers[request.data['post_type']](data=request.data)
            if post_serializer.is_valid(raise_exception=True):
<<<<<<< HEAD
                post_serializer.save(owner=Profile.get_profile(request.user), group=Group.get_by_uuid(request.data['group']), uuid=uuid.uuid4())
=======
                post_uuid = uuid.uuid4()
                current_group = Group.get_by_uuid(request.data['group'])
                post_serializer.save(owner=Profile.get_profile(request.user), group=current_group, uuid=post_uuid)
                [add_post_to_feed(str(post_uuid), str(group_member.uuid)) for group_member in current_group.members.all()]
>>>>>>> feed

    return Response(status=status.HTTP_201_CREATED)
