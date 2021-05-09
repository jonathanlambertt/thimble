from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.test),
    path('holy', views.holy_moly),
]
