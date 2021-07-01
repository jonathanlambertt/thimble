from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post

from users.models import Profile

from .serializers import CreateReactionSerializer, ReactionInfoSerializer
from .models import Reaction

@api_view(['GET', 'POST'])
def handle_reaction(request, post_uuid):
    if request.method == 'POST':
        if CreateReactionSerializer(data=request.data).is_valid(raise_exception=True):
            Reaction.objects.create(owner=Profile.get_profile(request.user), post=Post.get_by_uuid(post_uuid), reaction=request.data['reaction'])
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        current_post = Post.get_by_uuid(post_uuid)
        if current_post:
            return Response(data=ReactionInfoSerializer({'total_reactions': current_post.reactions.all(), 'newest_three':current_post.reactions.all()}).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)