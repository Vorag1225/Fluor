from django.db import transaction
from django.db.models import Sum

from .models import Post, Vote

@transaction.atomic
def post_vote(user,post_id,value):
    if value not in (-1,1):
        raise ValueError("Недопустимое значение для оценки")

    post = Post.objects.select_for_update().get(pk=post_id)

    vote = Vote.objects.filter(
        post=post,
        user=user
    ).first()

    if vote is None:
        Vote.objects.create(
            post=post,
            user=user,
            value=value
        )
    elif vote.value == value:
        vote.delete()
    else:
        vote.value = value
        vote.save(update_fields=["value"])

    score = Vote.objects.filter(post=post).aggregate(
        score=Sum('value')
    )["score"] or 0
    current_value = Vote.objects.filter(
        post=post,
        user=user
    ).values_list("value", flat=True).first() or 0

    return {
        "score": score,
        "value": current_value,
    }