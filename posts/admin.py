from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(PhotoPost)
admin.site.register(TextPost)
admin.site.register(LinkPost)
