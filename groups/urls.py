from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.create),
    path('<group_type>', views.group_view),
    path('<group_id>/members/<option>', views.list_members),
    path('<group_id>/<action>/<profile_id>', views.perform_action),
    path('<group_id>/edit', views.edit_group),
    path('<group_id>/leave', views.leave_group),
    path('<group_id>/user-status', views.user_status),
    path('<group_id>/potential-members', views.potential_members),
    path('<group_id>/posts', views.posts),
]
