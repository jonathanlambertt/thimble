from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import PhotoPost, LinkPost, TextPost

from users.serializers import PostInfoSerializer
from notifications.serializers import TimeSerializer

from .PhotoHelper import upload_photo

class PhotoField(serializers.Field):
    def to_internal_value(self, value):
        if value:
            return upload_photo(value)
        raise ValidationError('Please choose a photo.')

class CreatePhotoPostSerializer(serializers.ModelSerializer):
    photo = PhotoField()

    class Meta:
        model = PhotoPost
        fields = ['post_type','title','photo']
        extra_kwargs = {'photo': {'required' : True}}

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
        return {'name': value.name, 'uuid': value.uuid}

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