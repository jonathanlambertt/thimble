from celery import shared_task

from .models import Group

from users.RedisHelper import add_post_to_feed

@shared_task
def distribute_users_post_to_feeds(user_uuid, group_uuid, post_uuid):
    current_group = Group.get_by_uuid(group_uuid)
    [add_post_to_feed(post_uuid, str(group_member.uuid)) for group_member in current_group.members.all()]
    notify_group_members_of_post.delay(group_uuid,user_uuid)


@shared_task
def notify_group_members_of_post(group_uuid, posting_user):
    current_group = Group.get_by_uuid(group_uuid)
    for member in current_group.members.all():
        if member.user.username != posting_user:
            member.send_notification(f'{posting_user} posted in {current_group.name}')
