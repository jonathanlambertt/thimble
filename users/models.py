from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.URLField()
    uuid = models.UUIDField()
    friends = models.ManyToManyField('self')

    def get_by_uuid(uuid):
        return Profile.objects.get(uuid=uuid)

    def get_profile(user):
        return Profile.objects.get(user=user)

    def profile_page_info(self):
        return {'posts':self.posts, 'groups':self.joined_groups, 'friends':self.friends, 'profile_picture': self.profile_picture}
      