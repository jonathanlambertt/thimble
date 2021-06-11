from django.db import models

from django.contrib.auth.models import User

from posts.PhotoHelper import upload_photo, update_photo

from .RedisHelper import *

from posts.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.URLField()
    uuid = models.UUIDField()
    friends = models.ManyToManyField('self')
    
    def get_feed(self):
        return [Post.objects.filter(uuid=post_uuid.decode('utf-8')).first() for post_uuid in get_recent_posts(str(self.uuid))]

    def get_by_uuid(uuid):
        return Profile.objects.get(uuid=uuid)

    def get_profile(user):
        return Profile.objects.get(user=user)

    def profile_page_info(self):
        return {'posts':self.posts, 'groups':self.joined_groups, 'friends':self.friends, 'profile_picture': self.profile_picture, 'full_name': self.full_name}

    def edit_attributes(self, **kwargs):
        for attribute in kwargs:
            if hasattr(self, attribute):
                if attribute == 'profile_picture':
                    if self.profile_picture:
                        update_photo(self.profile_picture, kwargs['profile_picture'])
                    else:   
                        self.__setattr__('profile_picture', upload_photo(kwargs['profile_picture']))
                else:
                    self.__setattr__(attribute, kwargs[attribute])
        self.save()