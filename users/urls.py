from django.urls import path
from . import views
from rest_framework.authtoken import views as rest_views

app_name = 'users'
urlpatterns = [
    path('', views.register),
    path('login', rest_views.obtain_auth_token),
    path('friends', views.friends_list),
    path('search/<search_query>', views.search),
]
