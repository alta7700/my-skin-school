from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class RegexUsernameValidator(RegexValidator):
    regex = r'^(?!user-)(?=.*[a-zA-Z])[\w+.+-]+$'
    message = 'Логин может содержать только буквы, цифры и знаки .+-_. Минимум 1 буква, не может начинаться с "user-"'
    flags = 0


def validate_svg(file):
    from main.utils.images import is_svg
    if file._file and not is_svg(file._file):
        raise ValidationError("File not svg")
