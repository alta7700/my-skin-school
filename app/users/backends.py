from django.contrib.auth.backends import ModelBackend
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from .models import User


class AuthBackend(ModelBackend):

    def user_can_authenticate(self, user: "User"):
        return user.is_active

    def authenticate(self, request, password=None, **kwargs):
        login: str = kwargs.get(User.USERNAME_FIELD) or kwargs.get(User.EMAIL_FIELD) or kwargs.get(User.PHONE_FIELD)

        if login is None or password is None:
            return

        login = login.strip()
        auth_field = 'username'
        if '@' in login:
            auth_field = 'email'
        else:
            try:
                number = PhoneNumber.from_string(login)
                if number.is_valid():
                    login = number.as_e164
                    auth_field = 'phone'
            except NumberParseException:
                pass
        user = User.objects.get_by(auth_field, login)
        if user is None:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
            return
        if self.user_can_authenticate(user) and user.check_password(password):
            return user