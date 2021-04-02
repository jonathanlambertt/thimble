from django.urls import path
from . import views
from rest_framework.authtoken import views as rest_views

app_name = 'users'
urlpatterns = [
    path('', views.register),
]
