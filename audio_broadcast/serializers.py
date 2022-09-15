
from rest_framework import serializers
from .models import Audio, DeviceStatus


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"

class DeviceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceStatus
        fields = ['device_name', 'is_active']

class DeviceStatusSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = DeviceStatus
        fields = '__all__'