from django.db import models
from polymorphic.models import PolymorphicModel

import uuid
from datetime import datetime

class PostType(models.IntegerChoices):
    TEXT = 0
    LINK = 1
    PHOTO = 2
    

class Post(PolymorphicModel):
    owner = models.ForeignKey('users.profile', related_name='posts', on_delete=models.PROTECT)
    group = models.ForeignKey('groups.group', related_name='posts', on_delete=models.PROTECT)
    title = models.CharField(max_length=140, blank=True, null=True)
    post_type = models.IntegerField(PostType.choices)
    timestamp = models.DateTimeField(default=datetime.now)
    uuid = models.UUIDField()

    def get_by_uuid(uuid):
        return Post.objects.filter(uuid=uuid).first()


class TextPost(Post):
    text = models.CharField(max_length=140)

class PhotoPost(Post):
    photo = models.URLField()

class LinkPost(Post):
    link = models.URLField(max_length=500)
