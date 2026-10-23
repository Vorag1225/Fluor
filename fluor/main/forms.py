from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django import forms
from .models import Post, Comment


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Отображаемое имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('username','first_name', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', max_length=200)
    text = forms.CharField(label='Текст', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Комментарий', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)
