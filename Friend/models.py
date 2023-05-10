from django.db import models


class FriendRequest(models.Model):
    from_id = models.ForeignKey('User.User', related_name='friend_request_from_user_id', on_delete=models.DO_NOTHING)
    to_id = models.ForeignKey('User.User', related_name='friend_request_to_user_id', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_id'], name='friend_request_from_id_unique_con'),
            models.UniqueConstraint(fields=['to_id'], name='friend_request_to_id_unique_con'),
        ]
