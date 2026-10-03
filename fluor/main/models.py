from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=150, blank=True)
    icon = models.ImageField(
        upload_to='profile_icons/',
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': self.user.id})