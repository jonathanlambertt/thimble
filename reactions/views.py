from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post

from users.models import Profile

from .serializers import CreateReactionSerializer, ReactionInfoSerializer
from .models import Reaction

@api_view(['GET', 'POST', 'DELETE'])
def handle_reaction(request, post_uuid):
    current_post = Post.get_by_uuid(post_uuid)
    if request.method == 'POST':
        if CreateReactionSerializer(data=request.data).is_valid(raise_exception=True):
            current_profile = Profile.get_profile(request.user)
            profiles_reaction = current_post.reactions.filter(owner=current_profile).first()
            if profiles_reaction:
                profiles_reaction.reaction = request.data['reaction']
                profiles_reaction.save()
            else:
                Reaction.objects.create(owner=current_profile, post=current_post, reaction=request.data['reaction'])
            return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        if current_post:
            return Response(data=ReactionInfoSerializer({'total_reactions': current_post.reactions.all(), 'newest_three':current_post.reactions.all()}).data)
    elif request.method == 'DELETE':
        profiles_reaction = current_post.reactions.filter(owner=Profile.get_profile(request.user)).first()
        if profiles_reaction:
            profiles_reaction.delete()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)