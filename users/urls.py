from django.urls import path
from . import views
from rest_framework.authtoken import views as rest_views

app_name = 'users'
urlpatterns = [
    path('', views.register),
    path('profile', views.profile),
    path('edit', views.edit),
    path('login', rest_views.obtain_auth_token),
    path('search/<search_query>', views.search),
    path('friends', views.friends),
]
