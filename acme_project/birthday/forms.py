# birthday/forms.py
from django import forms
from django.core.exceptions import ValidationError
# Импортируем класс модели Birthday.
from .models import Birthday, Congratulation
from .validators import real_age

# Импорт функции для отправки почты.
from django.core.mail import send_mail

# Для использования формы с моделями меняем класс на forms.ModelForm.
# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):
    # Удаляем все описания полей.
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        validators=[real_age]
    )
    # Все настройки задаём в подклассе Meta.

    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        exclude = ('author',)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]

    def clean(self):
        # Вызов родительского метода clean.
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )

class CongratulationForm(forms.ModelForm):
    
    class Meta:
        model = Congratulation
        fields = ('text',) 
