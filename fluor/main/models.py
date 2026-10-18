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

class Vote(models.Model):
    class Value(models.IntegerChoices):                       # Варианты голосов
        UPVOTE = 1, "UP"
        DOWNVOTE = -1, "DOWN"


    post = models.ForeignKey( Post, on_delete=models.CASCADE) # К какому посту привязан
    user = models.ForeignKey( User, on_delete=models.CASCADE) # К какому пользователю привязан
    value = models.SmallIntegerField(choices=Value.choices)   # Какой голос выбрал(вверх или вниз)
    created_at = models.DateTimeField(auto_now_add=True)      # Когда голос создан

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],                      # Органичивает создание нескольких голосов от
                name='unique_vote'                            # одного пользователя к одному посту
            ),
            models.CheckConstraint(                           # Запрещает хранить недопустимые значения в поле
                condition=models.Q(value__in=[1, -1]),        # на уровне БД
                name="value_must_be_valid",
            )
        ]