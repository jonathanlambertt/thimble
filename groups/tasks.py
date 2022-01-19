from celery import shared_task

from .models import Group

from users.RedisHelper import add_post_to_feed

@shared_task
def post_and_notify_group(username, post_uuid, group_uuid):
    current_group = Group.get_by_uuid(group_uuid)
    [add_post_to_feed(post_uuid, str(group_member.uuid)) for group_member in current_group.members.all()]
    send_group_notification.delay(group_uuid, username, f'{username} posted in {current_group.name}.')

@shared_task
def send_group_notification(group_uuid, username, notification_text):
    current_group = Group.get_by_uuid(group_uuid)
    for member in current_group.members.all():
        if member.user.username != username:
            member.send_notification(notification_text)
