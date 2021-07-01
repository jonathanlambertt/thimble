from rest_framework import serializers
from django.core.exceptions import ValidationError


class CountItemsSerializer(serializers.Field):
    def to_representation(self, value):
        return len(value.all())