from django.contrib.auth.forms import UserCreationForm, UsernameField

from users.models import User


class NullUsernameField(UsernameField):
    def to_python(self, value):
        if not value:
            return None
        return super().to_python(value)


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = User.LOGIN_FIELDS
        field_classes = {User.USERNAME_FIELD: NullUsernameField,}
