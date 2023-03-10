from django.contrib.auth.models import User, Group
from cloudmusic.models import Song, UserAccounts
from rest_framework import serializers

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'duration', 'created_by', 'public']


class SongUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'duration', 'created_by', 'public', 'created_timestamp', 'last_updated_timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccounts
        fields = ['email', 'password']