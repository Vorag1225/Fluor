from django.db import transaction
from django.db.models import Sum

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