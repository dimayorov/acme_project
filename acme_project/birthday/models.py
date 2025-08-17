from django.db import models
from django.contrib.auth import get_user_model
# Импортируется функция-валидатор.
from .validators import real_age
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse


# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()

class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    constraints = (models.UniqueConstraint(
        # имя ограничения
        fields=('first_name', 'last_name', 'birthday'),
        name='Unique person constraint',),)

    class Meta:
        pass

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
