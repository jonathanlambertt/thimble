from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PhotoPost
from .serializers import *

from users.models import Profile
from groups.models import Group

import uuid

##testing


@api_view(['POST'])
def test(request):
    print('incoming', request.data)
    post_serializers = {'0':CreateTextPostSerializer, '1': CreatePhotoPostSerializer, '2':CreateLinkPostSerializer}
    if 'post_type' in request.data:
        if request.data['post_type'] in post_serializers:
            post_serializer = post_serializers[request.data['post_type']](data=request.data)
            if post_serializer.is_valid(raise_exception=True):
                post_serializer.save(owner=Profile.get_profile(request.user), group=Group.get_group_by_uuid(request.data['group']), uuid=uuid.uuid4())

    return Response('banana shits')

@api_view(['GET'])
def holy_moly(request):
    post_serializers = {0:TextPostSerializer, 1: PhotoPostSerializer, 2:LinkPostSerializer}
    cur = Group.get_group_by_uuid(request.data['group'])
    info = []
    for post in cur.posts.all():
        info.append(post_serializers[post.post_type](post).data)
    return Response(info)