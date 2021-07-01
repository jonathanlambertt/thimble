from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Reaction

from utilities.serializers import CountItemsSerializer

from users.serializers import ProfilePictureSerializer

class CreateReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['reaction']

class ReactionSerializer(serializers.ModelSerializer):
    owner = ProfilePictureSerializer()

    class Meta:
        model = Reaction
        fields = ['reaction', 'owner']

class NewestThreeSerializer(serializers.Field):
    def to_representation(self, value):
        return ReactionSerializer(sorted(value.all(), key=lambda reaction: reaction.id, reverse=True)[:3], many=True).data

class ReactionInfoSerializer(serializers.Serializer):
    total_reactions = CountItemsSerializer()
    newest_three = NewestThreeSerializer()

