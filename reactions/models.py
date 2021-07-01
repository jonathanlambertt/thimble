from django.db import models

class Reaction(models.Model):
    owner = models.ForeignKey('users.profile', related_name='reactions', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.post', related_name='reactions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=128)
