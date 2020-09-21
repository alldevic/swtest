from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class PostInviteSerializer(serializers.Serializer):
    """
    Приглашенеие пользователю
    """

    user_id = serializers.IntegerField(label="user_id",
                                       help_text="ID Пользователя")

    class Meta:
        fields = (
            'user_id'
        )
