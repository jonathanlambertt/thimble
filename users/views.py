from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

# Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    cps = CreateProfileSerializer(data=request.data)
    if cps.is_valid(raise_exception=True):
        cps.save()
    return Response('good')
