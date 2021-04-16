from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime

from .models import Notification

from users.serializers import ProfileSerializer

from datetime import datetime, timedelta

class TimeSerializer(serializers.Field):
    def to_representation(self, value):
<<<<<<< HEAD
        time_elapsed = datetime.now() - value
        time_difference = time_elapsed.total_seconds()
=======
        time_difference = (datetime.now() - value).total_seconds()
>>>>>>> 2a5518e41315d9bd53824a625f2c533c4b4c5e28

        if time_difference > 60: #time difference in total seconds
            if time_difference // 60 >= 60:
                if time_difference // 3600 >= 24:
                    if time_difference // 86400 >= 7:
                        if time_difference // 604800 > 4:
                            return value.strftime("%b %-d, %Y")
                        else:
                           elapsed_time = (time_difference // 604800, 'w') 
                    else:
                        elapsed_time = (time_difference // 86400, 'd')
                else:
                   elapsed_time = (time_difference // 3600, 'h') 
            else:
                elapsed_time = (time_difference // 60, 'm')
        else:
            elapsed_time = (time_difference, 's')  
        return f'{int(elapsed_time[0])}{elapsed_time[1]}'

class NotificationSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    timestamp = TimeSerializer()

    class Meta:
        model =  Notification
        exclude = ['id', 'recipient']
