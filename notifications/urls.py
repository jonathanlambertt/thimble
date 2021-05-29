from django.urls import path
from . import views

app_name = 'notifications'
urlpatterns = [
    path('inbox', views.inbox),
    path('send', views.send),
    path('friend-request/<request_id>',views.handle_friend_request),
]
