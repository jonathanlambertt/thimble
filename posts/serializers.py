from rest_framework import serializers

from .models import PhotoPost, LinkPost, TextPost

from users.serializers import PostInfoSerializer
from notifications.serializers import TimeSerializer

class CreatePhotoPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoPost
        fields = ['post_type','title','photo']

class CreateTextPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextPost
        fields = ['post_type','title','text']

class CreateLinkPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkPost
        fields = ['post_type','title','link']

class GroupField(serializers.Field):
    def to_representation(self, value):
        return value.name

class PhotoPostSerializer(serializers.ModelSerializer):
    owner = PostInfoSerializer()
    group = GroupField()
    timestamp = TimeSerializer()

    class Meta:
        model = PhotoPost
        exclude = ['id', 'polymorphic_ctype']

class TextPostSerializer(serializers.ModelSerializer):
    owner = PostInfoSerializer()
    group = GroupField()
    timestamp = TimeSerializer()

    class Meta:
        model = TextPost
        exclude = ['id', 'polymorphic_ctype']

class LinkPostSerializer(serializers.ModelSerializer):
    owner = PostInfoSerializer()
    group = GroupField()
    timestamp = TimeSerializer()

    class Meta:
        model = LinkPost
        exclude = ['id', 'polymorphic_ctype']