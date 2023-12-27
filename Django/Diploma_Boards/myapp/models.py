from django.db import models
from django.contrib.auth.models import AbstractUser
from Diploma_Boards.settings import BOARD_STATUSES


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)


class Card(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_cards'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_cards',
        null=True,
        blank=True,
        default=None
    )
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=20,
        choices=BOARD_STATUSES,
        default='new',
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Card {self.pk}, title "{self.title}"'

    def get_next_status(self):
        current_index = [status[0] for status in BOARD_STATUSES].index(self.status)
        if current_index + 1 < len(BOARD_STATUSES):
            return BOARD_STATUSES[current_index + 1][0]
        else:
            return None

    def get_previous_status(self):
        current_index = [status[0] for status in BOARD_STATUSES].index(self.status)
        if current_index - 1 >= 0:
            return BOARD_STATUSES[current_index - 1][0]
        else:
            return None

    def set_next_status(self):
        self.status = self.get_next_status()
        self.save()

    def set_previous_status(self):
        self.status = self.get_previous_status()
        self.save()

    def user_can_move_to_next_status(self):
        return self.status in ('new', 'in_progress', 'in_QA')

    def user_can_move_to_previous_status(self):
        return self.status in ('in_progress', 'in_QA', 'ready')

    def manager_can_move_to_next_status(self):
        return self.status == 'ready'

    def manager_can_move_to_previous_status(self):
        return self.status == 'done'
