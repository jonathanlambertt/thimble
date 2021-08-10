# lpush(feed, post_id)
# lrange(feed, start, end)
import redis
import os

redis_instance = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

def add_post_to_feed(post_uuid, profile_uuid):
    redis_instance.lpush(f'{profile_uuid}:feed', post_uuid)


def get_recent_posts(profile_uuid):
    return redis_instance.lrange(f'{profile_uuid}:feed', 0, -1)

def delete_post_from_feed(post_uuid, profile_uuid):
    redis_instance.lrem(f'{profile_uuid}:feed', 1, post_uuid)