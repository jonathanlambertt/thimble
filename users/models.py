from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.contrib.auth.models import User

from posts.PhotoHelper import upload_photo, update_photo

from .RedisHelper import *

from posts.models import Post

from exponent_server_sdk import (DeviceNotRegisteredError, PushClient, PushMessage, PushServerError, PushTicketError)
from requests.exceptions import ConnectionError, HTTPError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.URLField()
    uuid = models.UUIDField()
    friends = models.ManyToManyField('self')
    notification_token = models.CharField(max_length=100, blank=True)
    
    def send_notification(self, notification, extra=None):
        if self.notification_token != '':
            try:
                response = PushClient().publish(PushMessage(to=self.notification_token, body=notification, data=extra, title=""))
            except PushServerError as exc:
                print('Error sending notification: info<',exc,'>')
                raise
            except (ConnectionError, HTTPError) as exc:
                print('Error with notification connection: info<',exc,'>')
                raise self.retry(exc=exc)

            try:
                response.validate_response()
            except DeviceNotRegisteredError:
                self.notification_token = ''
                self.save()
            except PushTicketError as exc:
                print('Error pushing notification: info<',exc,'>')
                raise self.retry(exc=exc)

    def get_feed(self, last_post):
        total_posts_to_send = 10
        profile_feed = [post.decode('utf-8') for post in get_recent_posts(str(self.uuid))]
        last_post_index = profile_feed.index(last_post)+1 if last_post else 0
        return [Post.objects.filter(uuid=post_uuid).first() for post_uuid in profile_feed[last_post_index:last_post_index+total_posts_to_send]]

    def get_by_uuid(uuid):
        return Profile.objects.get(uuid=uuid)

    def get_profile(user):
        return Profile.objects.get(user=user)

    def profile_page_info(self):
        return {'posts':self.posts, 'groups':self.joined_groups, 'friends':self.friends, 'profile_picture': self.profile_picture, 'full_name': self.full_name, 'username': self.user.username}

    def edit_attributes(self, **kwargs):
        for attribute in kwargs:
            if hasattr(self, attribute):
                if attribute == 'profile_picture':
                    if type(kwargs['profile_picture'])==InMemoryUploadedFile:
                        if self.profile_picture:
                            self.__setattr__('profile_picture', update_photo(self.profile_picture, kwargs['profile_picture']))
                        else:
                            self.__setattr__('profile_picture', upload_photo(kwargs['profile_picture']))
                    else:
                        self.__setattr__('profile_picture', kwargs['profile_picture'])
                else:
                    self.__setattr__(attribute, kwargs[attribute])
        self.save()