from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Ticket(models.Model):
    id: int
    first_name: str = models.CharField('Имя', max_length=50)
    email: str = models.EmailField('Email')
    phone: str = PhoneNumberField('Номер телефона')
    theme: str = models.CharField('Тема обращения', max_length=50)
    message: str = models.TextField('Сообщение')
    processed: bool = models.BooleanField('Обработано', default=False)

    class Meta:
        db_table = "tickets"
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
