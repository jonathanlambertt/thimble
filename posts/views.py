from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PhotoPost
from .serializers import *

from users.models import Profile
from groups.models import Group
from groups.tasks import distribute_users_post_to_feeds
from posts.models import Post

import uuid
from users.RedisHelper import add_post_to_feed

@api_view(['POST'])
def create_post(request):
    post_serializers = {'0':CreateTextPostSerializer, '1': CreateLinkPostSerializer, '2':  CreatePhotoPostSerializer}
    if 'post_type' in request.data:
        if request.data['post_type'] in post_serializers:
            post_serializer = post_serializers[request.data['post_type']](data=request.data)
            if post_serializer.is_valid(raise_exception=True):
                post_uuid = uuid.uuid4()
                current_group = Group.get_by_uuid(request.data['group'])
                post_serializer.save(owner=Profile.get_profile(request.user), group=current_group, uuid=post_uuid)
                # Distributes and then notifies users of new post
                distribute_users_post_to_feeds.delay(request.user.username, request.data['group'], str(post_uuid))

                return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST) # needs to eventually return data to say why it 400
