from django.conf import settings
import redis

class RedisHelper:
    def __init__(self, redis_instance, section):
        self.instance = redis_instance
        self.project_name = settings.REDIS_SETTINGS['REDIS_PROJECT_NAME']
        self.section = section

    def get_value(self, key):
        return self.instance.get(f'{self.project_name}:{self.section}:{key}')

    def set_value(self, key, value):
        return self.instance.set(f'{self.project_name}:{self.section}:{key}', value)

    def push_value(self, key, value):
        return self.instance.lpush(key, value)
