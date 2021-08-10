from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.create_post),
    path('test', views.test),
]
