from django import forms

from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Напишите что-нибудь...'
        }))

    class Meta:
        model = Comment
        fields = ['content']


class CommentReplyForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Напишите что-нибудь...'
        }))

    class Meta:
        model = Reply
        fields = ['content']


# class NestedReplyForm(forms.ModelForm):
#     class Meta:
#         model = Reply
#         fields = ['content']
#         widgets = {
#             'content' : forms.TextInput(attrs={'autofocus': True, 'class': "!text-sm bg-gray-200 !p-0 !pl-2 !h-8"})
#         }
#         labels = {
#             'body': ''
#         }
