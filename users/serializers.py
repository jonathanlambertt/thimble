from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from .models import Profile

import uuid

from django.core.validators import validate_email as django_validate_email


def check_email_format(value):
    try:
        django_validate_email(value)
    except:
        raise serializers.ValidationError("Invalid email")

class UsernameField(serializers.Field):
    def to_representation(self, value):
        return value.username

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class ProfileSerializer(serializers.ModelSerializer):
    user = UsernameField()

    class Meta:
        model = Profile
        exclude = ['friends', 'id', 'notification_token']

class ProfileSearchResultSerializer(serializers.Serializer):
    are_friends = serializers.BooleanField()
    pending_friend_request = serializers.BooleanField()
    profile = ProfileSerializer()

class CreateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=50)
    password = serializers.CharField(min_length=6)
    email = serializers.CharField(required=True, validators=[check_email_format])
    full_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['full_name','username','password','email']

    # Check if username is taken if not return lowercased username
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use")
        else:
            return value.lower()

    # Check if email is taken
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        else:
            return value

    # Create new user, profile and auth token
    def create(self, validated_data):
        new_user = User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'])
        new_profile = Profile.objects.create(user=new_user, full_name=(validated_data['full_name'] if 'full_name' in validated_data else ''), uuid=uuid.uuid4())
        Token.objects.create(user=new_user)
        return new_profile

class PostInfoSerializer(serializers.ModelSerializer):
    user = UsernameField()

    class Meta:
        model = Profile
        exclude = ['full_name', 'friends', 'id', 'uuid']

class FriendsListResultSerializer(serializers.ModelSerializer):
    user = UsernameField()

    class Meta:
        model = Profile
        exclude = ['id', 'friends', 'notification_token']

class CountField(serializers.Field):
    def to_representation(self, value):
        return value.count()

class ProfileTabSerializer(serializers.Serializer):
    posts = CountField()
    groups = CountField()
    friends = CountField()
    profile_picture = serializers.CharField()
    full_name = serializers.CharField()
    username = serializers.CharField()