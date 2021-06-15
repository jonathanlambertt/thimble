from django.db import models

from datetime import datetime

import uuid

from posts.PhotoHelper import upload_photo, update_photo
from users.RedisHelper import delete_post_from_feed

class Group(models.Model):
    creator = models.ForeignKey('users.profile', related_name='my_groups', on_delete=models.PROTECT)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=150, blank=True)
    members = models.ManyToManyField('users.profile', related_name='joined_groups')
    date = models.DateTimeField(default=datetime.now)
    banner = models.URLField(blank=True)
    uuid = models.UUIDField()

    def create_group(**kwargs):
        new_group = Group.objects.create(creator=kwargs['creator'], name=kwargs['name'], uuid=uuid.uuid4())
        new_group.edit_attributes(**kwargs)
        new_group.add_member(kwargs['creator'])
        new_group.save()
        return new_group

    def edit_attributes(self, **kwargs):
        for attribute in kwargs:
            if hasattr(self, attribute):
                if attribute == 'banner':
                    if self.banner:
                        update_photo(self.banner, kwargs['banner'])
                    else: 
                        self.__setattr__('banner', kwargs['banner'])
                else:
                    self.__setattr__(attribute, kwargs[attribute])
        self.save()

    def add_member(self, profile):
        self.members.add(profile)

    def remove_member(self, profile):
        self.members.remove(profile)

    def get_by_uuid(uuid):
        return Group.objects.filter(uuid=uuid).first()