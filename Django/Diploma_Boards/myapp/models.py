from django.db import models
from django.contrib.auth.models import AbstractUser
from Diploma_Boards.settings import BOARD_STATUSES


class User(AbstractUser):
    ...


class Card(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_reports'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_cards'
    )
    status = models.CharField(
        max_length=20,
        choices=BOARD_STATUSES,
        default='new'
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set default assignee if not provided
        if not self.assignee_id:
            # You can replace this with your default assignee logic
            self.assignee = User.objects.get(username='not_assigned')

        super().save(*args, **kwargs)