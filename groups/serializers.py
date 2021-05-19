from rest_framework import serializers

from .models import Group
from users.serializers import ProfileSerializer

class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        exclude = ['id']

class CreateGroupSerializer(GroupSerializer):
    name = serializers.CharField(max_length=60)
    description = serializers.CharField(max_length=150, required=False)
    
    class Meta(GroupSerializer.Meta):
        exclude = ['members', 'uuid', 'creator']

    def create(self, validated_data):
        return Group.create_group(**validated_data)

class MemberCountField(serializers.Field):
    def to_representation(self, value):
        return value.count()

class GroupViewSerializer(GroupSerializer):
    members = MemberCountField()
    #posts = count posts
    
    class Meta(GroupSerializer.Meta):
        exclude = ['id', 'date', 'creator']
