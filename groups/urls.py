from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.create),
    path('<group_type>', views.group_view),
    path('<group_id>/<action>/<profile_id>', views.perform_action),
    #path('<group_id>/add/<profile_id>', views.add_member),
    #path('<group_id>/remove/<profile_id>', views.remove_member),
    path('<group_id>/members', views.list_members),
    path('<group_id>/leave', views.leave_group),
]