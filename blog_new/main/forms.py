from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm, ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe


from users.models import NewsletterUser

class NewsletterUserSignUpForm(forms.ModelForm):
    email = forms.EmailField(label='')

    class Meta:
        model = NewsletterUser
        fields = ('email',)

        # def clean(self):
        #     if NewsletterUser.objects.filter(email=self.cleaned_data['email'].lower()).exists():
        #         raise forms.ValidationError('Label exists!')
        #
        #     return self.cleaned_data

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'max_length': 64,
            'placeholder': 'Имя'
        }))
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ваш e-mail'
        }))
    subject = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Тема'
        }))
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Текст'
        }))

    def send_email(self):
        pass
