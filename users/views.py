from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

# Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    profile_serializer = CreateProfileSerializer(data=request.data)
    if profile_serializer.is_valid(raise_exception=True):
        profile_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(profile_serializer.errors)
