from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriend
        fields = ['first_id', 'second_id']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['from_id', 'to_id', 'status']
