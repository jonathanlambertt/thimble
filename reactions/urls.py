from django.urls import path

from . import views

app_name = 'reactions'

urlpatterns = [
    path('<post_uuid>', views.handle_reaction),
]
