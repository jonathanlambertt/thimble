from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.URLField(default='https://bit.ly/3rEF965')
    uuid = models.UUIDField()
    friends = models.ManyToManyField('self')

    def get_by_uuid(uuid):
        return Profile.objects.get(uuid=uuid)

    def get_profile(user):
        return Profile.objects.get(user=user)

