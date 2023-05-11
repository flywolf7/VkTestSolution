from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class UserFriend(models.Model):
    first_id = models.ForeignKey('User.User', related_name='user_friendship_first_id', on_delete=models.DO_NOTHING)
    second_id = models.ForeignKey('User.User', related_name='user_friendship_second_id', on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_id', 'second_id'], name='user_friend_12_unique_con'),
            models.UniqueConstraint(fields=['second_id', 'first_id'], name='user_friend_21_unique_con'),
        ]


class FriendRequest(models.Model):
    from_id = models.ForeignKey('User.User', related_name='friend_request_from_user_id', on_delete=models.DO_NOTHING)
    to_id = models.ForeignKey('User.User', related_name='friend_request_to_user_id', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255)
