from rest_framework import serializers

from .models import Group
from users.serializers import ProfileSerializer

from posts.PhotoHelper import upload_photo

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ['id']

class CreateBannerSerializer(serializers.Field):
    def to_internal_value(self, value):
        if value:
            return upload_photo(value)

class CreateGroupSerializer(GroupSerializer):
    name = serializers.CharField(max_length=60)
    description = serializers.CharField(max_length=150, required=False)
    banner = CreateBannerSerializer(required=False)

    class Meta(GroupSerializer.Meta):
        exclude = ['members', 'uuid', 'creator']

    def create(self, validated_data):
        return Group.create_group(**validated_data)

class MemberCountField(serializers.Field):
    def to_representation(self, value):
        return value.count()

class PostCountField(serializers.Field):
    def to_representation(self, value):
        return value.count()

class AdvancedGroupSerializer(GroupSerializer):
    members = MemberCountField()
    posts = PostCountField()
    
    class Meta(GroupSerializer.Meta):
        exclude = ['id', 'date', 'creator']

class GroupViewSerializer(serializers.Serializer):
    group = AdvancedGroupSerializer()
    user_status = serializers.CharField(max_length=25)