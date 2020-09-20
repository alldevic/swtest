from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

User = get_user_model()


class Invite(models.Model):
    """Model definition for Invite."""

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user',
        verbose_name='Отправитель')

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user',
        verbose_name='Получатель')

    confirmed = models.BooleanField(
        "Подтвержден",
        default=False)

    date_created = models.DateTimeField("Дата создания")
    date_confirmed = models.DateTimeField(
        "Дата подтверждения",
        null=True,
        blank=True)

    def clean(self):
        to_id = self.to_user_id
        from_id = self.from_user_id

        if to_id == from_id:
            raise ValidationError({
                'from_user': ValidationError(
                    'Пользователи совпадают',
                    code='invalid'),
                'to_user': ValidationError(
                    'Пользователи совпадают',
                    code='invalid'),
            })

        invites_count = Invite.objects \
            .filter(from_user__id=from_id,
                    to_user__id=to_id) \
            .count()

        if invites_count:
            raise ValidationError({'to_user':
                                   f'Инвайт для {self.to_user} уже отправлен'})

        rev_invites_count = Invite.objects \
            .filter(from_user__id=to_id,
                    to_user__id=from_id) \
            .count()

        if rev_invites_count:
            raise ValidationError(
                {'from_user':
                 f'{self.to_user} уже отправил инвайт для {self.from_user}'})

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''

        if not self.id:
            self.date_created = timezone.now()

        if self.confirmed:
            self.date_confirmed = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        """Meta definition for Invite."""

        verbose_name = 'Invite'
        verbose_name_plural = 'Invites'

    def __str__(self):
        """Unicode representation of Invite."""
        return str(self.pk)
