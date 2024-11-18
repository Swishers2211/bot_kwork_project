from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, telegram_id, username=None, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("The Telegram ID must be provided")
        user = self.model(telegram_id=telegram_id, username=username, **extra_fields)
        user.set_password(password)  # Пароль будет `None`, если не указан
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(telegram_id, username=username, password=password, **extra_fields)


class User(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.telegram_id} - {self.username}'
