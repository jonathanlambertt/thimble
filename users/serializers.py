from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from .models import Profile

import uuid

class UsernameField(serializers.Field):
    def to_representation(self, value):
        return value.username

class ProfileSerializer(serializers.ModelSerializer):
    user = UsernameField()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture']

class CreateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=50)
    password = serializers.CharField(min_length=6)
    email = serializers.CharField(allow_blank=False)
    full_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['full_name','username','password','email']

    # Check if username is taken
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use")
        else:
            return value

    # Check if email is taken
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        else:
            return value

    # Create new user, profile and auth token
    def create(self, validated_data):
        new_user = User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'])
        new_profile = Profile.objects.create(user=new_user, full_name=validated_data['full_name'], uuid=uuid.uuid4())
        Token.objects.create(user=new_user)
        return new_profile
