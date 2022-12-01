from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group as OrigGroup
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from main.validators import RegexUsernameValidator
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id: int
    username_validator = RegexUsernameValidator()
    username = models.CharField(
        "Логин",
        max_length=30,
        unique=True, null=True, blank=True,
        help_text=RegexUsernameValidator.message,
        validators=[username_validator, MinLengthValidator(3)],
        error_messages={
            "unique": "Пользователь с таким логином уже существует",
        },
    )
    email = models.EmailField("Email", unique=True, null=True, blank=True)
    phone = PhoneNumberField('Номер телефона', max_length=20, unique=True, null=True, blank=True)

    last_name = models.CharField("Фамилия", max_length=40, blank=True)
    first_name = models.CharField("Имя", max_length=40, blank=True)
    fathers_name = models.CharField("Отчество", max_length=40, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    PHONE_FIELD = "phone"
    REQUIRED_FIELDS = [EMAIL_FIELD, PHONE_FIELD]

    objects = UserManager()

    LOGIN_FIELDS = NULLABLE_UNIQUE_CHARFIELDS = (USERNAME_FIELD, EMAIL_FIELD, PHONE_FIELD)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.fathers_name}'.strip() or self.username

    def __str__(self) -> str:
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def set_username_if_empty(self):
        if not self.username:
            self.username = f'user-{self.id}'
            self.save(force_update=True, update_fields=['username'])

    def save(self, *args, **kwargs):
        for field in self.NULLABLE_UNIQUE_CHARFIELDS:
            if getattr(self, field) == '':
                setattr(self, field, None)
        super().save(*args, **kwargs)


class Group(OrigGroup):
    class Meta:
        proxy = True
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
