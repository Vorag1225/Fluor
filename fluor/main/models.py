from django.db import models
from django.db.models.functions import Coalesce
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

class PostManager(models.Manager):
    def get_queryset(self):
        vote_sum = (
            VotePost.objects.filter(post_id=models.OuterRef('pk')).values('post_id').annotate(total=models.Sum('value'))
            .values('total')
        )
        return super().get_queryset().annotate(
            score=Coalesce(
                models.Subquery(vote_sum),
                models.Value(0),
            ),
            comments_count = models.Count('comments',distinct=True)
        )
    def get_user_vote(self,user):
        if not user.is_authenticated:
            return self.get_queryset().annotate(
                user_vote=models.Value(0),
            )
        else:
            request_vote = VotePost.objects.filter(
                post_id=models.OuterRef('pk'),
                user=user,
            ).values('value')[:1]

            return self.get_queryset().annotate(
                user_vote=Coalesce(
                    models.Subquery(request_vote),
                    models.Value(0)
                )
            )

class Post(models.Model):
    author = models.ForeignKey(                             # Автор поста
    User,
    on_delete=models.CASCADE,
    related_name='posts'
    )
    title = models.CharField(max_length=200)                # Заголовок поста
    text = models.TextField()                               # Текст поста
    created_at = models.DateTimeField(auto_now_add=True)    # Когда был создан пост

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'id': self.id})

class VotePost(models.Model):
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



class Comment(models.Model):
    post = models.ForeignKey(                               # К какому посту относится комментарий
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(                             # Автор комментария
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()                               # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)    # Когда был создан комментарий

    class Meta:
        ordering = ['created_at']                           # Старые сверху, новые снизу

    def __str__(self):
        return f'{self.author} → {self.post}: {self.text[:30]}'
