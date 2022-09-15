from django.db import models
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    audio_base64 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overriding save method so that when new data encounters new data is transferred to all clients"""
        channel_layer = get_channel_layer()
        records = Audio.objects.filter(is_sent=False).count()
        data = {'device_name':self.device_name,  'audio':self.audio_base64}

        # can be sent to multile groups
        async_to_sync(channel_layer.group_send)(
            'test_audio_group',
            {
                'type':'audio_messages',
                'data':json.dumps(data)
            }
        )
        async_to_sync(channel_layer.group_send)(
            'test_audio_group2',
            {
                'type':'messages',
                'data':json.dumps({'hello':'world'})
            }
        )
        self.is_sent = True
        super(Audio, self).save(*args, **kwargs)

class DeviceStatus(models.Model):
    device_name = models.CharField(max_length=150)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_req_time = models.DateTimeField(auto_now=False, null=True)
    # device_id = models.CharField(max_length=200)  # add later