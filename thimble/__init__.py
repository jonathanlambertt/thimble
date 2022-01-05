#Makes sure that app is loaded when project starts
#Also makes it so we can use @shared_task
from .celery import app as celery_app
__all__ = ('celery_app',)
