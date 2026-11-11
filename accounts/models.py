from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra information attached to Django's built-in User.

    We keep authentication (username/password) in Django's User model and store
    campus-specific details here. One User has exactly one Profile (OneToOne).
    """

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        PUBLISHER = 'publisher', 'Authorized Campus Publisher/Representative'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text='Determines what the user is allowed to publish/manage in later stages.',
    )
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_publisher(self):
        return self.role == self.Role.PUBLISHER
