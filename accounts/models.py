from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    
    THEME_CHOICES = [
        ('system', 'Системная'),
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='system'
    )

    class Meta:
        db_table = 'server_users'

    def __str__(self):
        return self.username
