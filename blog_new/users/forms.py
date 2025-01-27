from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm, ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe


from users.models import NewsletterUser, User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password"]

    username = forms.CharField(label='Email / Имя пользователя')
    password = forms.CharField(label=("Пароль"), widget=forms.PasswordInput)

    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={"autofocus": True,
    #                                   'class': 'form-control',
    #                                   'placeholder': 'Введите ваше имя пользователя'}))
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                   'class': 'form-control',
    #                                   'placeholder': 'Введите ваш пароль'})
    # )

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "Имя",
            "Фамилия",
            "username",
            "email",
            "password1",
            "password2",
        )

    Имя = forms.CharField(max_length=20, required=False)
    Фамилия = forms.CharField(max_length=20, required=False)
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "image",
            "Имя",
            "Фамилия",
            "username",
            "email",
        )

    image = forms.ImageField(required=False)
    Имя = forms.CharField(max_length=20, required=False)
    Фамилия = forms.CharField(max_length=20, required=False)
    username = forms.CharField()
    email = forms.EmailField()
    # password = ReadOnlyPasswordHashField(
    #     label=("Пароль"),
    #     help_text=mark_safe(
    #         'Пароли хранятся в зашифрованном виде,'
    #         'поэтому нет возможности посмотреть пароль этого пользователя, но вы можете изменить его, '
    #         'используя <a href="{% url "users:password_change" %}">эту форму</a>.'
    #     ),
    # )

class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


# class NewsletterUserSignUpForm(forms.ModelForm):
#     email = forms.EmailField(label='')

#     class Meta:
#         model = NewsletterUser
#         fields = ('email',)

#         # def clean(self):
#         #     if NewsletterUser.objects.filter(email=self.cleaned_data['email'].lower()).exists():
#         #         raise forms.ValidationError('Label exists!')
#         #
#         #     return self.cleaned_data

#         def clean_email(self):
#             email = self.cleaned_data.get('email')

#             return email

