from django.db import models

from datetime import datetime

import uuid

class Group(models.Model):
    creator = models.ForeignKey('users.profile', related_name='my_groups', on_delete=models.PROTECT)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=150, blank=True)
    members = models.ManyToManyField('users.profile', related_name='joined_groups')
    date = models.DateTimeField(default=datetime.now)
    banner = models.URLField(blank=True)
    uuid = models.UUIDField()

    def create_group(**kwargs):
        return Group.objects.create(creator=kwargs['creator'], name=kwargs['name'], description=kwargs['description'] if 'description' in kwargs else '', uuid=uuid.uuid4())

    def add_member(self, profile):
        self.members.add(profile)

    def remove_member(self, profile):
        self.members.remove(profile)

    def get_group_by_uuid(uuid):
        return Group.objects.filter(uuid=uuid).first()