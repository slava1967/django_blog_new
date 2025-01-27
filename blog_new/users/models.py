from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    email = models.EmailField(unique=True)


    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class NewsletterUser(models.Model):
    email = models.EmailField()
    # email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', auto_now_add=True)


    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.email
