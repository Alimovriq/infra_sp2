from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError

from users.models import User

username_validator = RegexValidator(
    r"^[\w.@+-]+\Z",
    'Введите иное имя пользователя')


def validate_username(value):
    """
    Проверка логинов пользователей при регистрации.
    Пользователь не может использовать уже зарегистрированный логин.
    Запрещено использовать имя "me".
    """

    if User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже существует')
    if value is None:
        raise ValidationError('Поле должно быть заполнено')
    if value == 'me':
        raise ValidationError('Запрещено использовать me в качестве имени!')


def validate_email(value):
    """
    Проверка email пользователей при регистрации.
    Пользователь не может использовать уже зарегистрированный email.
    """

    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже существует')
    if value is None:
        raise ValidationError('Поле должно быть заполнено')
