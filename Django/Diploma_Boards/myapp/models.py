from django.db import models
from django.contrib.auth.models import AbstractUser
from Diploma_Boards.settings import BOARD_STATUSES


class User(AbstractUser):
    is_manager = False
    is_staff = True


class Card(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_reports'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_cards',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=20,
        choices=BOARD_STATUSES,
        default='new'
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Card {self.pk}, title "{self.title}"'

    def save(self, *args, **kwargs):
        if not self.assignee_id:
            self.assignee = None
            raise "You can assign card only to yourself"

        super().save(*args, **kwargs)