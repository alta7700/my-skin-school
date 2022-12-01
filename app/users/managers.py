from typing import TYPE_CHECKING, Type, Literal, Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.phonenumber import PhoneNumber

if TYPE_CHECKING:
    from users.models import User


class UserManager(DefaultUserManager):

    model: Type["User"]

    def get_by(self, field: Literal['username', 'email', 'phone'], value: str | int) -> Optional["User"]:
        if field in ('username', 'email'):
            field = f'{field}__iexact'
            value = value.lower()
        return self.get_or_none(**{field: value})

    def get_or_none(self, *args, **kwargs) -> Optional["User"]:
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            pass

    def username_is_unique(self, username: str) -> bool:
        return self.get_by('username', username) is None

    def email_is_unique(self, email: str) -> bool:
        return self.get_by('email', email) is None

    def phone_is_unique(self, phone: PhoneNumber) -> bool:
        return self.get_by('phone', str(phone)) is None

    def _create_user(self, username=None, email=None, phone=None, password=None, **extra_fields) -> "User":
        """
        Create and save a user with the given username, email, phone, and password.
        Username, email, phone must be valid and unique.
        """
        if not (email or phone or username):
            raise ValueError("The given email/phone must be set")

        if email:
            email = self.normalize_email(email)
            if not username:
                maybe_username, *_ = email.rsplit("@", 1)
                if not User.objects.filter(username=maybe_username):
                    username = maybe_username

        if username:
            username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save()
        user.set_username_if_empty()
        return user

    def create_client(self, username=None, email=None, phone=None, password=None, **extra_fields) -> "User":
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        return self._create_user(username=username, email=email, phone=phone, password=password, **extra_fields)

    def create_superuser(self, username=None, email=None, phone=None, password=None, **extra_fields) -> "User":
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self._create_user(username=username, email=email, phone=phone, password=password, **extra_fields)
