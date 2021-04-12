from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.create),
    path('<group_type>', views.group_view),
]