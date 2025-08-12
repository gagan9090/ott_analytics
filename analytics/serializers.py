from rest_framework import serializers
from .models import User, Video, WatchSession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class WatchSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchSession
        fields = '__all__'
