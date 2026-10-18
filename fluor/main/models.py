from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # привязка к пользователю
    description = models.CharField(max_length=150, blank=True)  # описание профиля
    icon = models.ImageField(                                   # заготовка для иконок пользователей
        upload_to='profile_icons/',
        blank=True,
        null=True
    )

    def get_absolute_url(self): # в админке позволяет перейти на страницу профиля
        return reverse('profile', kwargs={'id': self.user.id})



class Post(models.Model):
    author = models.ForeignKey(                             # Автор поста
    User,
    on_delete=models.CASCADE,
    related_name='posts'
    )
    title = models.CharField(max_length=200)                # Заголовок поста
    text = models.TextField()                               # Текст поста
    created_at = models.DateTimeField(auto_now_add=True)    # Когда был создан пост

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'id': self.id})