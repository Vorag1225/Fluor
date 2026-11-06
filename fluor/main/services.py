from django.db import transaction
from django.urls import reverse
from django.db.models import Sum
import base64
import binascii
from datetime import datetime
from django.conf import settings
from django.db.models import Q
from .models import *

@transaction.atomic
def post_vote(user,post_id,value):
    if value not in (-1,1):
        raise ValueError("Недопустимое значение для оценки")

    post = Post.objects.select_for_update().get(pk=post_id)

    vote = VotePost.objects.filter(
        post=post,
        user=user
    ).first()

    if vote is None:
        VotePost.objects.create(
            post=post,
            user=user,
            value=value
        )
    elif vote.value == value:
        vote.delete()
    else:
        vote.value = value
        vote.save(update_fields=["value"])

    score = VotePost.objects.filter(post=post).aggregate(
        score=Sum('value')
    )["score"] or 0
    current_value = VotePost.objects.filter(
        post=post,
        user=user
    ).values_list("value", flat=True).first() or 0

    return {
        "score": score,
        "value": current_value,
    }





class InvalidCursor(ValueError):
    """Курсор повреждён или подделан."""


def encode_cursor(post):
    raw = f"{post.created_at.isoformat()}|{post.pk}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_cursor(cursor):
    try:
        raw = base64.urlsafe_b64decode(cursor.encode()).decode()
        created_at_str, pk_str = raw.rsplit('|', 1)
        created_at = datetime.fromisoformat(created_at_str)
        if created_at.tzinfo is None:
            raise ValueError("naive datetime")
        return created_at, int(pk_str)
    except (ValueError, UnicodeError, binascii.Error):
        raise InvalidCursor("Некорректный курсор")


def get_page_size(raw_limit=None):
    """Размер порции: из ?limit= (если передан), иначе FEED_PAGE_SIZE; не больше FEED_MAX_PAGE_SIZE."""
    default = getattr(settings, 'FEED_PAGE_SIZE', 20)
    maximum = getattr(settings, 'FEED_MAX_PAGE_SIZE', 50)
    if raw_limit in (None, ''):
        return default
    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        raise ValueError("limit должен быть целым числом")
    if limit < 1:
        raise ValueError("limit должен быть больше 0")
    return min(limit, maximum)


def get_feed_page(user, cursor=None, limit=None, queryset=None):
    """Возвращает одну порцию ленты: {'posts': [Post, ...], 'next_cursor': str | None, 'has_more': bool}"""
    limit = limit or get_page_size()
    if queryset is None:
        queryset = Post.objects.get_user_vote(user)
    queryset = queryset.select_related('author').order_by('-created_at', '-id')

    if cursor:
        created_at, pk = decode_cursor(cursor)
        queryset = queryset.filter(
            Q(created_at__lt=created_at) | Q(created_at=created_at, id__lt=pk)
        )

    posts = list(queryset[:limit + 1])
    has_more = len(posts) > limit
    posts = posts[:limit]

    return {
        'posts': posts,
        'has_more': has_more,
        'next_cursor': encode_cursor(posts[-1]) if has_more else None,
    }


def serialize_post(post):
    """Пост в виде словаря для JSON (поля те же, что использует feed.html)."""
    return {
        'id': post.pk,
        'title': post.title,
        'text': post.text,
        'url': post.get_absolute_url(),
        'author': {
            'id': post.author_id,
            'first_name': post.author.first_name,
            'url': reverse('profile', kwargs={'id': post.author_id}),
        },
        'created_at': post.created_at.isoformat(),
        'score': post.score,
        'user_vote': post.user_vote,
        'comments_count': post.comments_count,
    }
